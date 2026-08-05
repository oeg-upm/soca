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


class TestResquiQualityPortal(unittest.TestCase):
    def test_resqui_report_is_loaded_and_scored_for_current_repository(self):
        with tempfile.TemporaryDirectory() as tmp:
            outputs_dir = Path(tmp) / "outputs"
            metadata_dir = outputs_dir / "soca" / "demo-project" / "metadata"
            metadata_dir.mkdir(parents=True)

            resqui_dir = outputs_dir / "resqui" / "demo-project" / "owner_repo"
            resqui_dir.mkdir(parents=True)
            (resqui_dir / "resqui_report.md").write_text(
                "# RESQUI report\n\nDetails",
                encoding="utf-8",
            )
            (resqui_dir / "resqui_summary.json").write_text(
                json.dumps(
                    {
                        "checks": [
                            {
                                "output": "secure",
                                "checkingSoftware": {"name": "GitLeaks"},
                            },
                            {
                                "output": "invalid",
                                "checkingSoftware": {"name": "CFFConvert"},
                            },
                            {
                                "output": "true",
                                "checkingSoftware": {"name": "RSFC"},
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )

            metadata = Metadata(
                str(metadata_dir),
                {
                    "code_repository": [
                        {
                            "result": {
                                "value": "https://github.com/owner/repo",
                            }
                        }
                    ]
                },
            )

            self.assertEqual(metadata.resqui_report_score(), (1, 2))

            report_html = metadata.resqui_report_html()
            self.assertIn("Quality:", report_html)
            self.assertIn("1/2 checks", report_html)
            self.assertIn("Show RESQUI report", report_html)
            self.assertIn("RESQUI report", report_html)


if __name__ == "__main__":
    unittest.main()
