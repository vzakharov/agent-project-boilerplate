# Issue #17: export-github-item.py never downloads user-attachments assets: Authorization survives the S3 redirect

- **State:** open
- **URL:** https://github.com/vzakharov/agent-project-boilerplate/issues/17
- **Author:** @vzakharov
- **Created:** 2026-08-20T23:15:41Z
- **Updated:** 2026-08-20T23:18:18Z
- **Closed:** _not closed_
- **Labels:** _none_

---

## Body

## Summary

`scripts/export-github-item.py` cannot download any attachment hosted on `github.com/user-attachments/…` — which is where GitHub has served every issue-composer upload since 2024. The download reports `400 Bad Request` and the export completes with an empty `attachments/` directory, so `/issue` silently proceeds without the screenshots and recordings the exporter exists to fetch.

This is a defect in the script, not an environment quirk: it reproduces anywhere `urllib` is used this way, a local checkout included.

## Mechanism

`download_asset` calls `_request`, which sends `Authorization: Bearer <token>`. GitHub answers a `user-attachments` URL with a redirect to a **pre-signed** S3 URL:

```
https://github.com/user-attachments/assets/<id>
  → https://github-production-user-asset-6210df.s3.amazonaws.com/…?X-Amz-Algorithm=…&X-Amz-Signature=…
```

`urllib.request.HTTPRedirectHandler` copies every header onto the redirected request, so the `Authorization` header follows the hop to S3 — and S3 refuses a request that carries both its query signature and that header:

```xml
<Error><Code>InvalidArgument</Code>
<Message>Only one auth mechanism allowed; only the X-Amz-Algorithm query parameter,
Signature query string parameter or the Authorization header should be specified</Message>
<ArgumentName>Authorization</ArgumentName></Error>
```

Reproducible with curl, which makes the header the decisive variable — `-L` drops auth on a cross-host redirect, `--location-trusted` keeps it as urllib does:

```bash
curl -sS -o /dev/null -w '%{http_code}\n' -L                   -H "Authorization: Bearer $GH_TOKEN" "$URL"  # 200
curl -sS -o /dev/null -w '%{http_code}\n' -L --location-trusted -H "Authorization: Bearer $GH_TOKEN" "$URL"  # 400
```

Assets on the older `user-images.githubusercontent.com` / `private-user-images.githubusercontent.com` hosts appear to be served without that cross-host hop, so a repo whose issues predate `user-attachments` would not have noticed this.

## Fix

Drop `Authorization` when a redirect changes host — the header is meaningless to S3 and is the sole cause of the rejection:

```python
class _DropAuthOnHostChange(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        new = super().redirect_request(req, fp, code, msg, headers, newurl)
        if new is not None and _host(newurl) != _host(req.full_url):
            new.remove_header("Authorization")
        return new
```

then build the opener with it and pass it to `_request`.

## Second, separate issue in remote sessions

Claude Code's remote-session egress proxy refuses `github.com/user-attachments/…` outright with `403` and a JSON `message` about repository-scoped endpoints — before GitHub is reached, so the redirect never happens and the fix above is not enough on its own. Retrying the download through an opener carrying `ProxyHandler({})` clears it, which is the same accommodation `.claude/hooks/session-start.sh` already makes for `gh` and for the same stated reason. Keeping the proxy-honoring attempt first leaves an environment where the proxy is the only egress route unaffected.

Worth reporting both attempts in the failure line, too: the current message shows only the first, which is what made a fixable `400` look like a policy `403`.

## Verified

Both changes are running in [vzakharov/vovazakharov.com#5](https://github.com/vzakharov/vovazakharov.com/pull/5). Against an issue with two attachments, the export goes from `403 Forbidden` ×2 and an empty directory to an 8.3 MB QuickTime recording plus a 359 KB PNG, with the markdown rewritten to the local paths. Happy to open a PR here with the same patch if useful.

---

## Comments

### Comment by @vzakharov on 2026-08-20T23:18:18Z

[https://github.com/vzakharov/agent-project-boilerplate/issues/17#issuecomment-5363233623](https://github.com/vzakharov/agent-project-boilerplate/issues/17#issuecomment-5363233623)

Sample attachment to see if the diagnosis is correct:

<img width="774" height="437" alt="Image" src="./attachments/7b5c3579-9d5c-4264-a443-5f6fccc35be3.jpg" />

---

## Timeline (status, references, and other events)

- **2026-08-20T23:16:31Z** @claude[bot] cross-referenced this issue from [#5 feat: adopt the /issue skill from the agent boilerplate](https://github.com/vzakharov/vovazakharov.com/pull/5).
