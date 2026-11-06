"""Validation suite for the codetopo Codex plugin marketplace.

This repository is a marketplace package: a catalog (marketplace.json), one
plugin manifest, an MCP server definition, and a skill document — there is no
compiled code. The suite validates the package the way Codex would read it:

- every JSON manifest parses and carries its required fields;
- every path a manifest references actually exists in the repo;
- the marketplace entry, the plugin manifest, the MCP definition, and the
  skill all name the same plugin and describe it the same way;
- the declared version is well-formed and the licence field agrees with the
  shipped LICENSE text.

Run from the repository root:  python3 -m unittest discover -s tests
"""

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKETPLACE_JSON = ROOT / ".agents" / "plugins" / "marketplace.json"
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")


def load_json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


class MarketplaceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.marketplace = load_json(MARKETPLACE_JSON)
        cls.entries = cls.marketplace["plugins"]
        # This marketplace ships exactly one plugin; the suite is written
        # against the first entry and asserts there is exactly one.
        assert len(cls.entries) == 1
        cls.entry = cls.entries[0]
        cls.plugin_dir = (ROOT / cls.entry["source"]["path"]).resolve()
        cls.plugin = load_json(cls.plugin_dir / ".codex-plugin" / "plugin.json")

    def test_marketplace_parses_and_has_required_fields(self):
        self.assertTrue(self.marketplace.get("name"))
        self.assertIn("interface", self.marketplace)
        self.assertTrue(self.marketplace["interface"].get("displayName"))
        for field in ("name", "description", "source", "policy", "category"):
            self.assertIn(field, self.entry, f"marketplace entry missing {field!r}")

    def test_entry_source_resolves_to_plugin_manifest(self):
        self.assertEqual(self.entry["source"]["source"], "local")
        manifest = self.plugin_dir / ".codex-plugin" / "plugin.json"
        self.assertTrue(manifest.is_file(), f"plugin manifest missing: {manifest}")

    def test_entry_and_plugin_agree(self):
        self.assertEqual(self.entry["name"], self.plugin["name"])
        self.assertEqual(self.entry["description"], self.plugin["description"])
        self.assertEqual(self.entry["category"],
                         self.plugin["interface"]["category"])

    def test_plugin_required_fields_and_version(self):
        for field in ("name", "version", "description", "author", "license",
                      "skills", "mcpServers", "interface"):
            self.assertIn(field, self.plugin, f"plugin.json missing {field!r}")
        self.assertRegex(self.plugin["version"], SEMVER)

    def test_license_field_matches_license_file(self):
        license_file = ROOT / "LICENSE"
        self.assertTrue(license_file.is_file(), "LICENSE file missing")
        self.assertTrue(self.plugin["license"].startswith("AGPL"))
        self.assertIn("GNU AFFERO GENERAL PUBLIC LICENSE",
                      license_file.read_text(encoding="utf-8"))

    def test_mcp_reference_resolves_and_names_plugin(self):
        ref = self.plugin["mcpServers"]
        mcp_path = (self.plugin_dir / ref).resolve()
        self.assertTrue(mcp_path.is_file(), f"referenced MCP file missing: {ref}")
        servers = load_json(mcp_path)["mcpServers"]
        self.assertIn(self.plugin["name"], servers)
        server = servers[self.plugin["name"]]
        self.assertTrue(server.get("command"), "MCP server command is empty")
        self.assertIsInstance(server.get("args"), list)

    def test_skills_reference_resolves(self):
        skills_dir = (self.plugin_dir / self.plugin["skills"]).resolve()
        self.assertTrue(skills_dir.is_dir(), f"skills dir missing: {skills_dir}")
        skill = skills_dir / self.plugin["name"] / "SKILL.md"
        self.assertTrue(skill.is_file(), f"skill file missing: {skill}")
        text = skill.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---"), "SKILL.md lacks frontmatter")
        self.assertIn(f"name: {self.plugin['name']}", text.split("---", 2)[1])

    def test_readme_install_names_this_marketplace(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(f"{self.plugin['name']}@{self.marketplace['name']}", readme,
                      "README install command names a different marketplace")


if __name__ == "__main__":
    unittest.main()
