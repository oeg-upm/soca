import json
import os
import requests
import time
from pathlib import Path


GITHUB_TIMEOUT = 30
GITHUB_MAX_RETRIES = 3
GITHUB_RETRY_SECONDS = 2
RETRYABLE_GITHUB_STATUS_CODES = {502, 503, 504}


def _normalize_authorization_token(token):
    token = str(token or "").strip()
    if not token:
        return None

    lower_token = token.lower()
    if lower_token.startswith("bearer ") or lower_token.startswith("token "):
        return token

    return f"Bearer {token}"


def _authorization_header_from_somef_config():
    config_path = Path("~/.somef/config.json").expanduser()
    if not config_path.is_file():
        return None

    with config_path.open(encoding="utf-8") as json_file:
        data = json.load(json_file)

    return _normalize_authorization_token(data.get("Authorization"))


def _authorization_header():
    try:
        config_token = _authorization_header_from_somef_config()
        if config_token:
            return config_token
    except Exception as exc:
        print(str(exc))

    env_token = os.getenv("GITHUB_TOKEN") or os.getenv("GITHUB_API_TOKEN")
    return _normalize_authorization_token(env_token)


def _github_get(url, params, headers):
    request_kwargs = {
        "url": url,
        "params": params,
        "timeout": GITHUB_TIMEOUT,
    }
    if headers:
        request_kwargs["headers"] = headers

    for attempt in range(1, GITHUB_MAX_RETRIES + 1):
        response = requests.get(**request_kwargs)
        if (
            response.status_code in RETRYABLE_GITHUB_STATUS_CODES
            and attempt < GITHUB_MAX_RETRIES
        ):
            print(
                f"GitHub returned {response.status_code}; "
                f"retrying in {GITHUB_RETRY_SECONDS}s..."
            )
            time.sleep(GITHUB_RETRY_SECONDS)
            continue

        return response


def fetch(input, output, type, not_archived, not_forked, not_disabled):

    Path(output).write_text("", encoding="utf-8")

    if os.path.isfile(input):
        with open(input) as org_list:
            for org in org_list.readlines():
                _fetch(org.rstrip("\n"), output, type,
                       not_archived, not_forked, not_disabled)
    else:
        _fetch(input, output, type, not_archived, not_forked, not_disabled)


def _fetch(name, out_path, type, not_archived, not_forked, not_disabled):

    if type not in ['orgs', 'users']:
        raise ValueError(f'Type {type} is not supported.')

    print(f"Fetching repositories from {type} {name}:")

    URL = f"https://api.github.com/{type}/{name}/repos"
    page_size = 100 #antes 50, pero soporta el doble, 1 request menos a githubapi
    page = 1
    PARAMS = {'per_page': page_size, 'page': page}
    # TOKEN
    authorization = _authorization_header()
    HEADERS = None
    if authorization:
        HEADERS = {
            "accept": "application/vnd.github.v3+json",
            "Authorization": authorization,
        }
    else:
        print("Please provide Valid Authorization Token\n")
        print("Will commence fetch WITHOUT token \n")

    cont = True

    with open(out_path, 'a') as file_out:
        while cont:
            try:
                r = _github_get(URL, PARAMS, HEADERS)

                # Interrumpir el fetch si GitHub responde con un error HTTP.
                # De este modo no se acepta como válido un repos.txt parcial.
                r.raise_for_status()

                data_repos = r.json()

                # La API debe devolver una lista de repositorios. Las respuestas
                # de error de GitHub suelen ser objetos con un campo "message".
                if not isinstance(data_repos, list):
                    raise RuntimeError(
                        f"Invalid GitHub response for {type} '{name}'"
                    )

                print("Request " + str(page) + ". " + str(len(data_repos)
                                                            ) + " repositories are downloaded per request")
                page += 1
                PARAMS['page'] = page
                for repo in data_repos:
                    if (
                        (not not_archived or not repo["archived"])
                        and
                        (not not_forked or not repo["fork"])
                        and
                        (not not_disabled or not repo["disabled"])
                    ):
                        file_out.write(repo["html_url"] + "\n")
                    else:
                        print(
                            f"    - The repository '{repo['url']}' has been filtered out...")

                if len(data_repos) < page_size:
                    cont = False
            except Exception as exc:
                # Propagar el error hace que el comando termine con código
                # distinto de cero y evita procesar un inventario incompleto.
                raise RuntimeError(
                    f"Could not fetch {type} '{name}', page {page}: {exc}"
                ) from exc
