# Changelog

All notable changes to the codetopo Codex marketplace are recorded here, per release, in plain language
a user can act on — never a raw commit log. Entries are added with the change itself
(see CONTRIBUTING), and any security fix names the CVE or similar identifier where
one exists.

## [Unreleased]

## [0.5.0] — 2026-11-06

First GitHub Release of the already-published marketplace, at the plugin version
declared in `plugins/codetopo/.codex-plugin/plugin.json` (0.5.0).

### Added

- Marketplace catalog (`.agents/plugins/marketplace.json`) distributing one
  plugin, codetopo, from a local source path in this repository.
- Plugin manifest (`.codex-plugin/plugin.json`) declaring the codetopo MCP
  server and interface metadata, plus the `.mcp.json` server definition
  (`codetopo-mcp` over stdio).
- Bundled skill (`plugins/codetopo/skills/codetopo/SKILL.md`) teaching the
  index → search → query loop.
- Project documentation set: CONTRIBUTING, SECURITY (private vulnerability
  reporting), TEST-PLAN, and a CI validation suite for the marketplace manifests.
