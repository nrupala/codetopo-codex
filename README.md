# codetopo-codex

A self-hosted plugin marketplace for [Codex](https://developers.openai.com/codex)
that distributes one plugin: **codetopo**.

codetopo turns a source repository into a queryable code graph — symbols,
calls, imports, and structure — and answers structural questions (what calls
this function, what breaks if it changes, how two modules connect) as data
over MCP. This repository is only the packaging: a marketplace catalog plus
the plugin manifest, an MCP server entry, and a skill that teaches the agent
how to use codetopo's tools. The server itself lives in
[nrupala/codetopo](https://github.com/nrupala/codetopo).

There is no gatekeeper and no listing review for this route: adding the
marketplace is your choice, and Codex installs the plugin from this repo.

## Prerequisite

The plugin runs the `codetopo-mcp` binary locally over stdio. Install it
first (requires a stable Rust toolchain, e.g. via [rustup](https://rustup.rs)):

```sh
cargo install codetopo-mcp
```

## Install

```sh
codex plugin marketplace add nrupala/codetopo-codex
codex plugin add codetopo@codetopo-codex
```

Or add the marketplace the same way, then open `/plugins` inside Codex and
install **codetopo** from the Codetopo marketplace. Start a new Codex
session afterwards so the bundled skill and MCP tools load.

## What you get

- The `codetopo` MCP server (local stdio), with 12 tools: index, stats,
  search symbols, get symbol, descendants, ancestors, blast radius,
  neighborhood, path, snapshot, verify, and describe schema.
- A `codetopo` skill that walks the agent through the index → search →
  query loop and the working rules for trustworthy answers.

## License

codetopo is licensed under AGPL-3.0-or-later. See the
[codetopo repository](https://github.com/nrupala/codetopo) for the full
license text and source.

Owned by Nrupal Akolkar · Built with Muse by Meta

Support: info@nrupalakolkar.com · Project page: https://aimlds.org/codetopo
