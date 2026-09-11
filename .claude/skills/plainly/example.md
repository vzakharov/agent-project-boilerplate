# A worked pair

Two answers to the same question, in an invented billing system. The question:

> why did last night's export only include half the invoices?

## The thin answer

> The nightly export completed successfully — exit code 0, no errors logged,
> retry count 0. It wrote 412 of 806 invoices. The selection query filters on
> `updated_at >= now() - interval '24 hours'`, and the run began at 02:00 UTC as
> scheduled. The 50% alert threshold is what fired the page; that threshold is a
> default and has not been tuned for this job.

Every sentence is true, and it answers nothing. The headline is a status the
system emitted (**symptom-as-finding**); the counts, the window and the note
about the threshold arrive before any conclusion (**buried lede**); it is
written in `updated_at` and `interval` where *invoice* and *edited* were
available and exact (**untranslated nouns**); and it stops at the filter without
saying why the filter excluded anything (**broken chain**). A reader who wanted
to know what happened has to ask again.

## The full answer

> The export only takes invoices that were edited in the last day, and most of
> last night's invoices had not been edited in weeks.
>
> They were *finalized* last night, which is a different thing. The finalizer
> flips an invoice from draft to final, and it sets only the status field — it
> does not touch the edited-at timestamp. So an invoice drafted three weeks ago
> and finalized at 01:00 still looks, to the export, like a three-week-old
> invoice, and the export skips it. The 412 that did go out were the ones that
> happened to be edited yesterday as well as finalized.
>
> This gets worse as the backlog ages, not better: the longer an invoice sits in
> draft, the more certainly it misses its own export.
>
> The fix is for the export to select on finalized-at rather than edited-at,
> which is the date it actually cares about. Changing the finalizer to bump
> edited-at instead would work tonight and be wrong — it would report every
> finalized invoice as freshly edited to everything else that reads that field.

## What the second answer had read

The first answer stopped at the export's own query and the job's own logs, which
is where the symptom is. The second one opened the finalizer beside it and
compared the two — one writes `status`, the other reads `updated_at` — which is
where the cause is. Nothing about that was expensive or clever; it was one file
further out, and the first answer had already decided it was finished.

That is the general shape. The cause of a report like this is usually in the
thing that ran *next to* the thing that failed, and a report that never leaves
the failing component can only ever restate the failure.
