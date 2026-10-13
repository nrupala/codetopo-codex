---
name: codetopo
description: Answer structural questions about a codebase — what calls what, what breaks if a symbol changes, how two modules are connected — with codetopo's code-graph MCP tools. Use when the user asks about callers, dependents, impact or blast radius of a change, relationships between symbols or modules, or wants a verifiable snapshot of a repository's structure.
---

# codetopo

codetopo turns a source repository into a queryable code graph: symbols,
calls, imports, references, and structure, stored in a local graph database.
It answers structural questions as data. It is deliberately domain-blind —
no scores, no rankings, no opinions about what the code means — and it
parses code (Rust and TypeScript/JavaScript, via tree-sitter) without ever
executing it.

## The loop

1. **Index once.** Call `codetopo_index` with `repo_path` (the repository)
   and `db_path` (where the graph database lives). Pick one `db_path` per
   repository and reuse it for every later query in the session. The
   `package` argument defaults to the repository directory name.
2. **Discover ids.** Node ids look like `package::module::Type::method`,
   and the exact-id tools need exact ids. Call `codetopo_search_symbols`
   with a name substring first to get the real ids. Never guess an id.
3. **Query.** Use the exact-id tools below. List tools return at most
   `limit` entries (default 20); pass `expand: true` when you need full
   node objects instead of ids.
4. **Re-index after changes.** An index is a picture of the tree at index
   time. If the code has changed since indexing, run `codetopo_index`
   again against the same `db_path` before answering questions about the
   current state.

## The 12 tools

| Tool | Use it for |
| --- | --- |
| `codetopo_index` | Build or refresh the graph database for a repository. Required first step. |
| `codetopo_stats` | Node and edge totals with per-kind breakdowns. Cheap sanity check that an index exists and how big it is. |
| `codetopo_search_symbols` | Find symbols by name (case-insensitive substring of the label). The discovery step before exact-id queries. |
| `codetopo_get_symbol` | One node in full: kind, location, tier, defines and refs. Errors when the id is unknown — search first. |
| `codetopo_descendants` | Everything transitively reachable from a node over calls and imports: what it pulls in, what it can affect downstream. |
| `codetopo_ancestors` | Everything that can reach a node over calls and imports: its callers and dependents, transitively. |
| `codetopo_blast_radius` | What breaks if a node changes: dependents, overriders, and implementers. Ask this before proposing a change to a shared symbol. |
| `codetopo_neighborhood` | The subgraph within a few hops of a node, in both directions (contains/defines edges excluded). Good for "show me the area around X". |
| `codetopo_path` | The shortest typed path between two nodes, or the reason there is none. Answers "how are these two connected?". |
| `codetopo_snapshot` | Export the whole graph as a portable snapshot, bound to the audit head at export time. |
| `codetopo_verify` | Verify the tamper-evident audit chain of an index. Run it before trusting a snapshot or an index you did not just build. |
| `codetopo_describe_schema` | The schema the server speaks: node and edge kinds, tier rules, query vocabulary. Needs no database — call it whenever you are unsure what a kind or tier means. |

## Working rules

- Totals before lists: start with `codetopo_stats` or a capped query, and
  widen only when the user needs the full list.
- Quote node ids exactly as the tools return them. The package prefix is
  the repository directory name exactly as indexed, hyphens included.
- A snapshot is only as trustworthy as its audit chain: verify with
  `codetopo_verify`, and say so when you report snapshot-based results.
- Report what the graph says, including "no path exists" and empty
  results. Do not fill gaps with guesses about the code.
- codetopo reports structure only. It does not judge code quality, find
  vulnerabilities, or rank importance — do not present its output as a
  review verdict.
