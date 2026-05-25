---
description: Investigate the codebase using Explore agents. Use when the user asks to explore, investigate, or research something in the code. Examples: "explore how auth works", "investigate the chat flow", "/explore where is X used".
---

Delegate the user's question to one or more **Explore** agents (`subagent_type: "Explore"`). Never search, grep, or read files directly — always spawn an agent.

- If the question has independent facets, spawn multiple Explore agents in parallel.
- Pass the user's question (plus any relevant context) as the agent prompt.
- After agents return, synthesize their findings into a concise answer for the user.
