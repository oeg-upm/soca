# Changelog

### Added

- Added the `extract-1-repo` CLI command to extract metadata for a single GitHub repository without requiring a CSV repository list.
- Added Poetry project configuration so contributors can create a local virtual environment and install SOCA with `poetry install`.
- Added a current `portal_example` demo and moved older SOMEF metadata/example outputs to `old` for historical reference.
- Added a `linkeddata-portal` CLI command to generate LinkedData.es static pages from a YAML configuration.
- Added the `linkeddata_portal` package with:
  - a Jinja-based static site builder;
  - configurable pages, navigation, initiatives, tools, retired initiatives and awards;
  - static assets and templates for the generated LinkedData.es pages;
  - a generated YAML output that records the resolved site configuration.
- Added dynamic tool-card generation from SOCA metadata. The LinkedData portal can read a list of GitHub repository URLs, reuse existing SOCA metadata when available and extract missing metadata as a fallback.
- Added metadata lookup helpers that match repositories by normalized GitHub URL, owner/repository names and case-insensitive metadata filenames.
- Added portal support for repository-level quality information from RSFC, RESQUI and RsMetaCheck/sw-metadata-bot outputs.
- Added tests covering LinkedData portal generation, dynamic metadata-based cards, repository owner fallback logic and RESQUI quality report rendering.

### Changed

- Updated package requirements:
  - Python support is constrained to `>=3.11,<3.13`;
  - SOMEF is raised to `>=0.11.2`;
  - `Jinja2`, `PyYAML` and `pybtex` are included for the LinkedData portal and citation-related features.
- Updated `MANIFEST.in` so LinkedData portal templates, assets and base YAML configurations are included in packaged builds.
- Improved GitHub repository fetching:
  - reads the GitHub token from SOMEF configuration or from `GITHUB_TOKEN`/`GITHUB_API_TOKEN`;
  - normalizes authorization headers;
  - adds request timeouts;
  - retries transient GitHub `502`, `503` and `504` responses;
  - fails with a non-zero error instead of silently accepting partial repository inventories.
- Improved the classic SOCA portal UI:
  - replaced the previous neumorphic styling with a flatter, clearer card and filter layout;
  - added loading and error states while `cards_data.json` is fetched;
  - improved modal scrolling and quality-report readability;
  - renamed embedded dashboard labels to "Organization analytics dashboard" and "User analytics dashboard".
- Improved repository cards:
  - owner badges now ignore empty or literal `None` values and fall back to the GitHub URL owner;
  - repository type classification now scores software, ontology and web repositories using languages, metadata fields, repository names and descriptions;
  - homepage, application domain and description extraction now prefer higher-quality metadata sources and normalize nested/list values.
- Improved citation rendering:
  - CFF conversion now generates stable BibTeX citation keys from author, year and title;
  - BibTeX output is formatted before display/copy;
  - citation source labels are clearer, especially when BibTeX comes from `README.md`.
- Improved ontology and identifier rendering:
  - ontology cards show a fallback message when no ontology URL is available;
  - identifiers represented as Python-list-like strings are normalized before display.
- Improved RsMetaCheck/sw-metadata-bot summaries by distinguishing missing CodeMeta files, missing pitfall reports and GitHub issue publication failures.
- Updated documentation with the actual integrations of soca and leaved old documentation with influxDB & Graphana doc

### Fixed

- Fixed RSFC output lookup by supporting both repository-name folders and `owner_repo` output folders.
- Fixed `rsfc_assessment.json` loading so data is returned only when the file exists.
- Fixed owner filtering in portal generation so missing owners are not added to the owner list.
- Fixed portal startup behavior so users see a loading indicator while cards are being loaded and an error message if loading fails.
