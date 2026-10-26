from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "art-directing-visuals" / "SKILL.md"
README = ROOT / "README.md"


class PublicPackageTests(unittest.TestCase):
    def test_release_contains_a_neutral_skill_and_onboarding(self):
        skill = SKILL.read_text(encoding="utf-8")
        readme = README.read_text(encoding="utf-8")
        self.assertIn("name: art-directing-visuals", skill)
        self.assertIn("Use when", skill)
        self.assertIn("Do not invent facts", skill)
        self.assertIn("rights", skill.lower())
        self.assertIn("hermes skills install pavelnasuta/art-directing-visuals-skill/skills/art-directing-visuals", readme)

    def test_release_has_no_personal_or_private_source_markers(self):
        package = "\n".join(
            path.read_text(encoding="utf-8")
            for path in ROOT.rglob("*")
            if path.is_file() and ".git" not in path.parts and path.suffix in {".md", ".txt"}
        ).lower()
        forbidden = ["нии мозги", "menhausen", "pavelnasuta.github.io", "/root/", "nasuta.ru"]
        for marker in forbidden:
            self.assertNotIn(marker, package)

    def test_skill_frontmatter_is_complete(self):
        skill = SKILL.read_text(encoding="utf-8")
        frontmatter = skill.split("---", 2)[1]
        self.assertIn("name: art-directing-visuals", frontmatter)
        description = next(line for line in frontmatter.splitlines() if line.startswith("description:"))
        self.assertGreaterEqual(len(description.removeprefix("description:").strip()), 40)


if __name__ == "__main__":
    unittest.main()
