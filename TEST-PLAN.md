# Test plan — codetopo-codex

## Scope

This repository is a marketplace package — JSON manifests and a skill document;
it contains no compiled or interpreted product code. Testing covers the package
surface Codex reads when installing the plugin: the marketplace catalog
(`.agents/plugins/marketplace.json`), the plugin manifest
(`plugins/codetopo/.codex-plugin/plugin.json`), the MCP server definition
(`plugins/codetopo/.mcp.json`), and the bundled skill
(`plugins/codetopo/skills/codetopo/SKILL.md`). The codetopo server itself is
tested in its own repository (nrupala/codetopo) and is out of scope here.

## Suites

| Suite | Covers | Run it | Runs in CI |
|---|---|---|---|
| Marketplace validation (`tests/test_marketplace.py`) | JSON validity and required fields; referenced-path existence (plugin dir, MCP definition, skills dir, LICENSE); name/description/category agreement between the marketplace entry and the plugin manifest; MCP server name/command shape; version shape; licence-field vs LICENSE-text agreement; README install command naming this marketplace | `python3 -m unittest discover -s tests` | Yes — CI workflow |

## CI gates

- Full validation suite green on every push and pull request to `main`.
- Lint step: every `*.json` file in the repo must parse (`python3 -m json.tool`).
- No merge with a red CI run (per CONTRIBUTING).

## Cadence

- Every pull request: the full suite + JSON lint.
- Nightly / weekly: none — the package changes only with a codetopo release.
- Every release candidate: the release-readiness run (checker + evidence reads),
  per the house Release-Readiness Standard.

## Coverage bar

No numeric floor; new package content (a new manifest field, plugin, or skill)
lands with validation coverage per CONTRIBUTING.
