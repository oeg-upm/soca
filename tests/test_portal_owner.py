import json
import sys
import tempfile
import types
import unittest
from pathlib import Path


SOCA_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOCA_ROOT))


def install_portal_dependency_stubs():
    mistune = types.ModuleType("mistune")
    mistune.html = lambda markdown: f"<p>{markdown}</p>"
    sys.modules.setdefault("mistune", mistune)

    pygments = types.ModuleType("pygments")
    pygments.highlight = lambda *args, **kwargs: ""
    sys.modules.setdefault("pygments", pygments)

    lexers = types.ModuleType("pygments.lexers")
    sys.modules.setdefault("pygments.lexers", lexers)

    scdoc = types.ModuleType("pygments.lexers.scdoc")
    scdoc.ScdocLexer = object
    sys.modules.setdefault("pygments.lexers.scdoc", scdoc)

    formatters = types.ModuleType("pygments.formatters")
    formatters.HtmlFormatter = object
    sys.modules.setdefault("pygments.formatters", formatters)


install_portal_dependency_stubs()

from src.soca.commands.portal.metadata import Metadata  # noqa: E402


class TestPortalOwner(unittest.TestCase):
    def test_owner_falls_back_to_github_repository_url(self):
        metadata = {
            "code_repository": [
                {
                    "result": {
                        "value": "https://github.com/morph-kgc/morph-kgc",
                    }
                }
            ]
        }

        with tempfile.TemporaryDirectory() as tmp:
            md = Metadata(tmp, metadata)

            self.assertEqual(md.owner(), "morph-kgc")

    def test_owner_ignores_literal_none_values(self):
        metadata = {
            "owner": [{"result": {"value": "None"}}],
            "code_repository": [
                {
                    "result": {
                        "value": "https://github.com/lincedu/example",
                    }
                }
            ],
        }

        with tempfile.TemporaryDirectory() as tmp:
            md = Metadata(tmp, metadata)

            self.assertEqual(md.owner(), "lincedu")


if __name__ == "__main__":
    unittest.main()
