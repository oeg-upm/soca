import json
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


SOCA_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOCA_ROOT / "src"))

from linkeddata_portal.builder import build  # noqa: E402
from linkeddata_portal.builder import DEFAULT_ASSETS_DIR, DEFAULT_TEMPLATES_DIR  # noqa: E402
from linkeddata_portal.builder import build_config_with_dynamic_tools  # noqa: E402
from linkeddata_portal.builder import linkeddata_tool_card_from_metadata  # noqa: E402
from soca.__main__ import cli  # noqa: E402


class TestLinkedDataPortalBuilder(unittest.TestCase):
    def test_build_writes_resolved_yaml_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config_path = root / "linkeddata.base.yml"
            templates_dir = root / "templates"
            assets_dir = root / "assets"
            output_dir = root / "generates"
            project_metadata_dir = root / "project_metadata"
            linkeddata_metadata_dir = root / "linkeddata_metadata"
            generated_config_path = root / "linkeddata.generated.yml"
            tools_file = root / "linkeddata_tools.yml"

            templates_dir.mkdir()
            assets_dir.mkdir()
            project_metadata_dir.mkdir()
            (assets_dir / "starter-template.css").write_text("", encoding="utf-8")
            (templates_dir / "cards_page.html").write_text(
                "{{ page.title }}{% for item in items %}{{ item.name }}{% endfor %}",
                encoding="utf-8",
            )

            config_path.write_text(
                yaml.safe_dump(
                    {
                        "site": {"title": "LinkedData"},
                        "navigation": [],
                        "pages": {
                            "tools": {
                                "title": "Tools",
                                "output": "tools.html",
                                "collection": "tools",
                            }
                        },
                        "tools": [
                            {
                                "id": "base-only",
                                "name": "Base only",
                                "homepage": "https://example.org/base",
                            }
                        ],
                    },
                    sort_keys=False,
                ),
                encoding="utf-8",
            )
            tools_file.write_text(
                yaml.safe_dump(
                    {
                        "tools": [
                            {
                                "id": "manual-only",
                                "name": "Manual only",
                                "homepage": "https://example.org/manual",
                            },
                            {
                                "id": "soca-curated",
                                "url": "https://github.com/SergioZSZ/soca",
                                "name": "SOCA curated",
                                "category": None,
                                "homepage": None,
                                "image": None,
                                "description": None,
                            },
                        ]
                    },
                    sort_keys=False,
                ),
                encoding="utf-8",
            )
            (project_metadata_dir / "SergioZSZ_soca_2026-07-14.json").write_text(
                json.dumps(
                    {
                        "name": [
                            {
                                "technique": "GitHub_API",
                                "result": {"value": "SOCA"},
                            }
                        ],
                        "description": [
                            {
                                "technique": "code_parser",
                                "result": {"value": "Software catalog creator."},
                            }
                        ],
                        "application_domain": [
                            {
                                "result": {"value": "Catalog generation"},
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            build(
                output_dir=output_dir,
                config_path=config_path,
                templates_dir=templates_dir,
                assets_dir=assets_dir,
                metadata_dir=project_metadata_dir,
                linkeddata_metadata_dir=linkeddata_metadata_dir,
                tools_file=tools_file,
                generated_config_path=generated_config_path,
            )

            generated_config = yaml.safe_load(
                generated_config_path.read_text(encoding="utf-8")
            )

            self.assertEqual(
                [tool["id"] for tool in generated_config["tools"]],
                ["manual-only", "soca-curated"],
            )
            self.assertEqual(generated_config["tools"][1]["name"], "SOCA curated")
            self.assertEqual(generated_config["tools"][1]["category"], "Catalog generation")
            self.assertEqual(
                generated_config["tools"][1]["homepage"],
                "https://github.com/SergioZSZ/soca",
            )

    def test_card_titles_can_wrap_long_repository_names(self):
        cards_template = (DEFAULT_TEMPLATES_DIR / "cards_page.html").read_text(
            encoding="utf-8"
        )
        stylesheet = (DEFAULT_ASSETS_DIR / "starter-template.css").read_text(
            encoding="utf-8"
        )

        self.assertIn("linkeddata-card-title", cards_template)
        self.assertIn(".linkeddata-card-title", stylesheet)
        self.assertIn("overflow-wrap: anywhere", stylesheet)

    def test_static_html_lead_and_description_are_rendered_as_links(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config_path = root / "linkeddata.base.yml"
            templates_dir = root / "templates"
            assets_dir = root / "assets"
            output_dir = root / "generates"

            templates_dir.mkdir()
            assets_dir.mkdir()
            (assets_dir / "starter-template.css").write_text("", encoding="utf-8")
            (templates_dir / "cards_page.html").write_text(
                (DEFAULT_TEMPLATES_DIR / "cards_page.html").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            (templates_dir / "base.html").write_text(
                (DEFAULT_TEMPLATES_DIR / "base.html").read_text(encoding="utf-8"),
                encoding="utf-8",
            )

            config_path.write_text(
                yaml.safe_dump(
                    {
                        "site": {"title": "LinkedData", "description": "Test"},
                        "navigation": [],
                        "pages": {
                            "index": {
                                "title": "LinkedData",
                                "output": "index.html",
                                "heading": "LinkedData.es",
                                "lead": 'See <a href="tools.html">tools</a>.',
                                "collection": "initiatives",
                            }
                        },
                        "initiatives": [
                            {
                                "id": "datos-ign",
                                "name": "datos.ign.es",
                                "category": "Geographical domain",
                                "homepage": "https://datos.ign.es",
                                "image": None,
                                "description": "Plain fallback description.",
                                "description_html": (
                                    '<a href="https://datos.ign.es" target="_blank">'
                                    "datos.ign.es</a> linked description."
                                ),
                            }
                        ],
                    },
                    sort_keys=False,
                ),
                encoding="utf-8",
            )

            build(
                output_dir=output_dir,
                config_path=config_path,
                templates_dir=templates_dir,
                assets_dir=assets_dir,
            )

            html = (output_dir / "index.html").read_text(encoding="utf-8")

            self.assertIn('<a href="tools.html">tools</a>', html)
            self.assertIn(
                '<a href="https://datos.ign.es" target="_blank">datos.ign.es</a>',
                html,
            )
            self.assertNotIn("&lt;a href=", html)

    def test_static_award_html_is_rendered_as_original_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config_path = root / "linkeddata.base.yml"
            templates_dir = root / "templates"
            assets_dir = root / "assets"
            output_dir = root / "generates"

            templates_dir.mkdir()
            assets_dir.mkdir()
            (assets_dir / "starter-template.css").write_text("", encoding="utf-8")
            (templates_dir / "awards.html").write_text(
                (DEFAULT_TEMPLATES_DIR / "awards.html").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            (templates_dir / "base.html").write_text(
                (DEFAULT_TEMPLATES_DIR / "base.html").read_text(encoding="utf-8"),
                encoding="utf-8",
            )

            config_path.write_text(
                yaml.safe_dump(
                    {
                        "site": {"title": "LinkedData", "description": "Test"},
                        "navigation": [],
                        "pages": {
                            "awards": {
                                "title": "Awards",
                                "output": "awards.html",
                                "heading": "Awards",
                                "lead": "Award <b>lead</b>",
                                "collection": "awards",
                            }
                        },
                        "awards": [
                            {
                                "year": 2017,
                                "text": "Fallback award.",
                                "text_html": (
                                    'Award in the <a href="https://example.org" '
                                    'target="_blank">Aporta Challenge</a>.'
                                ),
                            }
                        ],
                    },
                    sort_keys=False,
                ),
                encoding="utf-8",
            )

            build(
                output_dir=output_dir,
                config_path=config_path,
                templates_dir=templates_dir,
                assets_dir=assets_dir,
            )

            html = (output_dir / "awards.html").read_text(encoding="utf-8")

            self.assertIn("Award <b>lead</b>", html)
            self.assertIn(
                '<a href="https://example.org" target="_blank">Aporta Challenge</a>',
                html,
            )
            self.assertNotIn("Fallback award.", html)

    def test_tools_file_repo_preserves_repository_dots_from_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config_path = root / "linkeddata.base.yml"
            metadata_dir = root / "metadata"
            linkeddata_metadata_dir = root / "linkeddata_metadata"
            tools_file = root / "linkeddata_tools.yml"

            metadata_dir.mkdir()
            config_path.write_text(
                yaml.safe_dump(
                    {
                        "site": {"title": "LinkedData"},
                        "navigation": [],
                        "pages": {},
                        "tools": [],
                    },
                    sort_keys=False,
                ),
                encoding="utf-8",
            )
            (metadata_dir / "lincedu_lincedu-github-io_2026-07-14.json").write_text(
                json.dumps(
                    {
                        "name": [{"result": {"value": "lincedu.github.io"}}],
                        "code_repository": [
                            {
                                "result": {
                                    "value": "https://github.com/lincedu/lincedu.github.io",
                                }
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            tools_file.write_text(
                yaml.safe_dump(
                    {
                        "tools": [
                            {
                                "url": "https://github.com/lincedu/lincedu.github.io",
                            }
                        ]
                    },
                    sort_keys=False,
                ),
                encoding="utf-8",
            )

            config = build_config_with_dynamic_tools(
                config_path=config_path,
                metadata_dir=metadata_dir,
                linkeddata_metadata_dir=linkeddata_metadata_dir,
                tools_file=tools_file,
            )

            self.assertEqual(
                config["tools"][0]["homepage"],
                "https://github.com/lincedu/lincedu.github.io",
            )

    def test_dynamic_card_uses_description_and_logo_from_metadata(self):
        card = linkeddata_tool_card_from_metadata(
            "https://github.com/dgarijo/WIDOCO",
            {
                "logo": [
                    {
                        "result": {
                            "value": "https://example.org/widoco-logo.png",
                        }
                    }
                ],
                "homepage": [
                    {
                        "technique": "code_parser",
                        "confidence": 1,
                        "result": {
                            "value": "https://low-priority.example.org/widoco",
                        },
                    },
                    {
                        "technique": "GitHub_API",
                        "confidence": 0.5,
                        "result": {
                            "value": "https://official.example.org/widoco",
                        },
                    },
                ],
                "description": [
                    {
                        "technique": "README",
                        "result": {
                            "value": "Long README description."
                        },
                    },
                    {
                        "technique": "GitHub API",
                        "result": {
                            "value": [
                                "Short WIDOCO description.",
                                "Extended WIDOCO description.",
                            ]
                        }
                    }
                ],
                "application_domain": [
                    {
                        "result": {
                            "value": "Ontology services",
                        }
                    }
                ],
            },
        )

        self.assertEqual(
            card["description"],
            "Short WIDOCO description.",
        )
        self.assertEqual(
            card["category"],
            "Ontology services",
        )
        self.assertEqual(
            card["image"],
            "https://example.org/widoco-logo.png",
        )
        fallback_card = linkeddata_tool_card_from_metadata(
            "https://github.com/dgarijo/WIDOCO",
            {},
        )
        self.assertEqual(
            fallback_card["image"],
            "img/github-default.svg",
        )
        self.assertEqual(
            card["homepage"],
            "https://official.example.org/widoco",
        )

    def test_metadata_lookup_uses_existing_file_when_repository_case_differs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config_path = root / "linkeddata.base.yml"
            metadata_dir = root / "metadata"
            linkeddata_metadata_dir = root / "linkeddata_metadata"
            tools_file = root / "linkeddata_tools.yml"

            metadata_dir.mkdir()
            config_path.write_text(
                yaml.safe_dump(
                    {
                        "site": {"title": "LinkedData"},
                        "navigation": [],
                        "pages": {},
                        "tools": [],
                    },
                    sort_keys=False,
                ),
                encoding="utf-8",
            )
            (metadata_dir / "dgarijo_Widoco_2026-07-14.json").write_text(
                json.dumps(
                    {
                        "name": [{"result": {"value": "Widoco"}}],
                        "code_repository": [
                            {
                                "result": {
                                    "value": "https://github.com/dgarijo/Widoco",
                                }
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            tools_file.write_text(
                yaml.safe_dump(
                    {
                        "tools": [
                            {
                                "url": "https://github.com/dgarijo/WIDOCO",
                            }
                        ]
                    },
                    sort_keys=False,
                ),
                encoding="utf-8",
            )

            config = build_config_with_dynamic_tools(
                config_path=config_path,
                metadata_dir=metadata_dir,
                linkeddata_metadata_dir=linkeddata_metadata_dir,
                tools_file=tools_file,
            )

            self.assertEqual(
                config["tools"][0]["homepage"],
                "https://github.com/dgarijo/WIDOCO",
            )
            self.assertTrue(
                (linkeddata_metadata_dir / "dgarijo_Widoco_2026-07-14.json").exists()
            )

    def test_cli_exposes_tools_file_and_not_repo_or_org_discovery(self):
        from click.testing import CliRunner

        result = CliRunner().invoke(cli, ["linkeddata-portal", "--help"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("--tools-file", result.output)
        self.assertNotIn("--add-repos", result.output)
        self.assertNotIn("--linkeddata-orgs", result.output)
        self.assertNotIn("--linkeddata-repos", result.output)
        self.assertNotIn("--linkeddata-extra-repos", result.output)


if __name__ == "__main__":
    unittest.main()
