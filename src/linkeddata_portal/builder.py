from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape


LINKEDDATA_DIR = Path(__file__).resolve().parent
DEFAULT_CONFIG_PATH = LINKEDDATA_DIR / "linkeddata.base.yml"
DEFAULT_TEMPLATES_DIR = LINKEDDATA_DIR / "templates"
DEFAULT_ASSETS_DIR = LINKEDDATA_DIR / "assets"


def default_outputs_root() -> Path:
    for parent in LINKEDDATA_DIR.parents:
        if parent.name == "containers":
            return parent / "outputs" / "linkeddata_portal"

    return Path("/app/outputs/linkeddata_portal")


DEFAULT_OUTPUTS_ROOT = default_outputs_root()
DEFAULT_METADATA_DIR = DEFAULT_OUTPUTS_ROOT / "metadata"
DEFAULT_OUTPUT_DIR = DEFAULT_OUTPUTS_ROOT / "generates"
DEFAULT_GENERATED_CONFIG_PATH = DEFAULT_OUTPUTS_ROOT / "linkeddata.generated.yml"
METADATA_FILE_PATTERN = re.compile(
    r"^(?P<owner>[^_]+)_(?P<repository>.+)_\d{4}-\d{2}-\d{2}\.json$"
)


def load_config(config_path: Path) -> dict[str, Any]:
    with config_path.open(encoding="utf-8") as stream:
        data = yaml.safe_load(stream)

    if not isinstance(data, dict):
        raise ValueError(f"Expected a YAML mapping in {config_path}")

    return data


def load_tools_file(tools_file: Path) -> list[str]:
    with tools_file.open(encoding="utf-8") as stream:
        data = yaml.safe_load(stream)

    if isinstance(data, dict):
        tools = data.get("tools")
    else:
        tools = data

    if not isinstance(tools, list):
        raise ValueError(f"Expected a 'tools' list in {tools_file}")

    repository_urls = []
    for tool in tools:
        if not isinstance(tool, str):
            raise ValueError(
                f"Expected every tool in {tools_file} to be a GitHub URL string"
            )

        repository_url = normalize_repository_url(tool)
        parse_github_repository(repository_url)
        repository_urls.append(repository_url)

    return repository_urls


def normalize_repository_url(repository_url: str) -> str:
    repository_url = str(repository_url or "").strip().rstrip("/")

    if repository_url.endswith(".git"):
        repository_url = repository_url[:-4]

    return repository_url


def parse_github_repository(repository_url: str) -> tuple[str, str]:
    parsed_url = urlparse(normalize_repository_url(repository_url))
    path_parts = [part for part in parsed_url.path.split("/") if part]

    if parsed_url.netloc.lower() != "github.com" or len(path_parts) != 2:
        raise ValueError(f"Invalid GitHub repository URL: {repository_url}")

    return path_parts[0], path_parts[1]


def repository_slug(repository_name: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", repository_name).strip("-")
    return slug.lower()


def dedupe_preserving_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    deduped_values: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        deduped_values.append(value)

    return deduped_values


def repository_url_from_metadata_file(metadata_path: Path) -> str | None:
    try:
        repository_url = repository_url_from_metadata(load_metadata(metadata_path))
        if repository_url:
            return repository_url
    except (OSError, json.JSONDecodeError, ValueError):
        pass

    match = METADATA_FILE_PATTERN.match(metadata_path.name)
    if not match:
        return None

    return (
        "https://github.com/"
        f"{match.group('owner')}/{match.group('repository')}"
    )


def find_metadata_file_for_repository(
    metadata_dir: Path,
    repository_url: str,
) -> Path | None:
    owner, repository = parse_github_repository(repository_url)
    matches = sorted(metadata_dir.glob(f"{owner}_{repository}_*.json"))
    if matches:
        return matches[-1]

    expected_repository_url = normalize_repository_url(repository_url).lower()
    for metadata_path in sorted(metadata_dir.glob(f"{owner}_*.json")):
        candidate_repository_url = repository_url_from_metadata_file(metadata_path)
        if candidate_repository_url is None:
            continue

        if normalize_repository_url(candidate_repository_url).lower() == expected_repository_url:
            return metadata_path

    return None


def metadata_file_for_repository(metadata_dir: Path, repository_url: str) -> Path:
    owner, repository = parse_github_repository(repository_url)
    metadata_path = find_metadata_file_for_repository(metadata_dir, repository_url)

    if metadata_path is None:
        raise FileNotFoundError(
            "Missing SOCA metadata for linkeddata repository: "
            f"{repository_url}. Expected metadata file matching "
            f"'{owner}_{repository}_*.json' in {metadata_dir}"
        )

    return metadata_path


def extract_repository_metadata(repository_url: str, metadata_dir: Path) -> None:
    from soca.commands import extract_metadata

    metadata_dir.mkdir(parents=True, exist_ok=True)
    existing_paths = {path.resolve() for path in metadata_dir.iterdir()}
    extract_metadata.extract_1_repo(
        normalize_repository_url(repository_url),
        str(metadata_dir),
        verbose=False,
    )
    metadata_path = find_metadata_file_for_repository(metadata_dir, repository_url)
    cleanup_fallback_extraction_artifacts(metadata_dir, existing_paths, metadata_path)


def cleanup_fallback_extraction_artifacts(
    metadata_dir: Path,
    existing_paths: set[Path],
    metadata_path: Path | None,
) -> None:
    metadata_path = metadata_path.resolve() if metadata_path is not None else None
    for path in metadata_dir.iterdir():
        resolved_path = path.resolve()
        if resolved_path in existing_paths or resolved_path == metadata_path:
            continue

        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()


def copy_project_metadata_to_linkeddata_metadata(
    project_metadata_dir: Path | None,
    linkeddata_metadata_dir: Path,
    linkeddata_repos: list[str],
) -> None:
    if project_metadata_dir is None:
        return

    linkeddata_metadata_dir.mkdir(parents=True, exist_ok=True)
    for repository_url in linkeddata_repos:
        metadata_path = find_metadata_file_for_repository(
            project_metadata_dir,
            repository_url,
        )
        if metadata_path is None:
            continue

        target_path = linkeddata_metadata_dir / metadata_path.name
        if metadata_path.resolve() != target_path.resolve():
            shutil.copy2(metadata_path, target_path)


def ensure_metadata_for_repositories(
    project_metadata_dir: Path | None,
    linkeddata_metadata_dir: Path,
    linkeddata_repos: list[str],
) -> None:
    linkeddata_metadata_dir.mkdir(parents=True, exist_ok=True)
    copy_project_metadata_to_linkeddata_metadata(
        project_metadata_dir,
        linkeddata_metadata_dir,
        linkeddata_repos,
    )

    missing_repositories = [
        repository_url
        for repository_url in linkeddata_repos
        if find_metadata_file_for_repository(linkeddata_metadata_dir, repository_url) is None
    ]

    for repository_url in missing_repositories:
        print(f"Missing SOCA metadata for {repository_url}. Extracting it now...")
        extract_repository_metadata(repository_url, linkeddata_metadata_dir)

    still_missing = [
        repository_url
        for repository_url in linkeddata_repos
        if find_metadata_file_for_repository(linkeddata_metadata_dir, repository_url) is None
    ]

    if still_missing:
        formatted_repositories = ", ".join(still_missing)
        raise FileNotFoundError(
            "Missing SOCA metadata after fallback extraction for: "
            f"{formatted_repositories}"
        )


def load_metadata(metadata_path: Path) -> dict[str, Any]:
    with metadata_path.open(encoding="utf-8") as stream:
        data = json.load(stream)

    if not isinstance(data, dict):
        raise ValueError(f"Expected a JSON object in {metadata_path}")

    return data


def normalize_text_value(value: Any) -> str | None:
    if value is None:
        return None

    if isinstance(value, list):
        for item in value:
            normalized = normalize_text_value(item)
            if normalized:
                return normalized
        return None

    if isinstance(value, dict):
        for nested_key in ("value", "text", "name"):
            if nested_key not in value:
                continue

            normalized = normalize_text_value(value[nested_key])
            if normalized:
                return normalized
        return None

    text = str(value).strip()
    return text or None


def repository_url_from_metadata(metadata: dict[str, Any]) -> str | None:
    from soca.commands.portal.metadata import Metadata

    repository_url = Metadata("", metadata).repo_url()
    if not repository_url:
        return None

    return normalize_repository_url(repository_url)


def linkeddata_tool_card_from_metadata(
    repository_url: str,
    metadata: dict[str, Any],
) -> dict[str, Any]:
    from soca.commands.portal.metadata import Metadata

    _, repository = parse_github_repository(repository_url)
    md = Metadata("", metadata)

    return {
        "id": repository_slug(repository),
        "url": normalize_repository_url(repository_url),
        "name": md.title() or repository,
        "category": md.application_domain() or "Tool",
        "homepage": md.homepage() or normalize_repository_url(repository_url),
        "image": md.logo(),
        "description": md.description(),
    }


def load_tools_file_cards(
    tools_file: Path,
    metadata_dir: Path | None,
    linkeddata_metadata_dir: Path,
) -> list[dict[str, Any]]:
    repository_urls = dedupe_preserving_order(load_tools_file(tools_file))

    if repository_urls:
        ensure_metadata_for_repositories(
            metadata_dir,
            linkeddata_metadata_dir,
            repository_urls,
        )

    resolved_tools: list[dict[str, Any]] = []
    for repository_url in repository_urls:
        resolved_tools.append(
            linkeddata_tool_card_from_metadata(
                repository_url,
                load_metadata(metadata_file_for_repository(linkeddata_metadata_dir, repository_url)),
            )
        )

    return resolved_tools


def reset_directory(directory: Path) -> Path:
    if directory.exists():
        if not directory.is_dir():
            raise NotADirectoryError(f"Expected directory path: {directory}")
        shutil.rmtree(directory)

    directory.mkdir(parents=True, exist_ok=True)
    return directory


def ensure_distinct_metadata_dirs(
    project_metadata_dir: Path | None,
    linkeddata_metadata_dir: Path,
) -> None:
    if project_metadata_dir is None:
        return

    if project_metadata_dir.resolve() == linkeddata_metadata_dir.resolve():
        raise ValueError(
            "--metadata-dir and --linkeddata-metadata-dir must be different "
            "because the LinkedData metadata cache is reset on every build."
        )


def build_config_with_dynamic_tools(
    config_path: Path,
    metadata_dir: Path | None = None,
    linkeddata_metadata_dir: Path = DEFAULT_METADATA_DIR,
    tools_file: Path | None = None,
) -> dict[str, Any]:
    config = load_config(config_path)

    if tools_file is not None:
        config["tools"] = load_tools_file_cards(
            tools_file,
            metadata_dir,
            linkeddata_metadata_dir,
        )

    return config


def load_template_environment(templates_dir: Path) -> Environment:
    return Environment(
        loader=FileSystemLoader(templates_dir),
        autoescape=select_autoescape(enabled_extensions=("html", "xml")),
    )


def copy_assets(assets_dir: Path, output_dir: Path) -> None:
    for item in assets_dir.iterdir():
        target = output_dir / item.name
        if item.is_dir():
            shutil.copytree(item, target, dirs_exist_ok=True)
        else:
            shutil.copy2(item, target)


def render_page(
    env: Environment,
    template_name: str,
    output_path: Path,
    site: dict[str, Any],
    navigation: list[dict[str, Any]],
    page: dict[str, Any],
    items: list[dict[str, Any]],
) -> None:
    html = env.get_template(template_name).render(
        site=site,
        navigation=navigation,
        page=page,
        items=items,
    )
    output_path.write_text(html, encoding="utf-8")


def write_generated_config(config: dict[str, Any], generated_config_path: Path) -> None:
    generated_config_path.parent.mkdir(parents=True, exist_ok=True)
    generated_config_path.write_text(
        yaml.safe_dump(config, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )


def build(
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    config_path: Path = DEFAULT_CONFIG_PATH,
    templates_dir: Path = DEFAULT_TEMPLATES_DIR,
    assets_dir: Path = DEFAULT_ASSETS_DIR,
    metadata_dir: Path | None = None,
    linkeddata_metadata_dir: Path = DEFAULT_METADATA_DIR,
    generated_config_path: Path = DEFAULT_GENERATED_CONFIG_PATH,
    tools_file: Path | None = None,
) -> list[Path]:
    ensure_distinct_metadata_dirs(metadata_dir, linkeddata_metadata_dir)
    output_dir = reset_directory(output_dir)
    linkeddata_metadata_dir = reset_directory(linkeddata_metadata_dir)

    config = build_config_with_dynamic_tools(
        config_path=config_path,
        metadata_dir=metadata_dir,
        linkeddata_metadata_dir=linkeddata_metadata_dir,
        tools_file=tools_file,
    )
    write_generated_config(config, generated_config_path)
    env = load_template_environment(templates_dir)

    copy_assets(assets_dir, output_dir)

    generated_pages: list[Path] = []
    for page_key, page in config["pages"].items():
        collection_name = page["collection"]
        template_name = "awards.html" if page_key == "awards" else "cards_page.html"
        output_path = output_dir / page["output"]

        render_page(
            env,
            template_name,
            output_path,
            config["site"],
            config["navigation"],
            page,
            config[collection_name],
        )
        generated_pages.append(output_path)

    return generated_pages


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build the LinkedData.es static pages from linkeddata.base.yml."
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG_PATH,
        help="Path to linkeddata.base.yml.",
    )
    parser.add_argument(
        "--templates-dir",
        type=Path,
        default=DEFAULT_TEMPLATES_DIR,
        help="Directory containing Jinja templates.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory where generated HTML will be written.",
    )
    parser.add_argument(
        "--assets-dir",
        type=Path,
        default=DEFAULT_ASSETS_DIR,
        help="Directory containing static assets.",
    )
    parser.add_argument(
        "--metadata-dir",
        type=Path,
        default=None,
        help="Directory containing project SOCA metadata JSON files.",
    )
    parser.add_argument(
        "--linkeddata-metadata-dir",
        type=Path,
        default=DEFAULT_METADATA_DIR,
        help="Directory where LinkedData portal metadata cache will be saved.",
    )
    parser.add_argument(
        "--generated-config-output",
        type=Path,
        default=DEFAULT_GENERATED_CONFIG_PATH,
        help="Path where the resolved LinkedData YAML config will be written.",
    )
    parser.add_argument(
        "--tools-file",
        type=Path,
        default=None,
        help="YAML file with a tools list of GitHub repository URLs.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    generated_pages = build(
        output_dir=args.output_dir,
        config_path=args.config,
        templates_dir=args.templates_dir,
        assets_dir=args.assets_dir,
        metadata_dir=args.metadata_dir,
        linkeddata_metadata_dir=args.linkeddata_metadata_dir,
        generated_config_path=args.generated_config_output,
        tools_file=args.tools_file,
    )
    env = load_template_environment(args.templates_dir)
    available_templates = ", ".join(sorted(env.list_templates(extensions=["html"])))
    print(f"Loaded config: {args.config}")
    print(f"Loaded templates: {available_templates}")
    print(f"Copied assets from: {args.assets_dir}")
    print(f"Output directory ready: {args.output_dir}")
    print(f"Generated config: {args.generated_config_output}")
    print(
        "Generated pages: "
        + ", ".join(page.name for page in generated_pages)
    )


if __name__ == "__main__":
    main()
