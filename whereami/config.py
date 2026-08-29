"""Optional user config file (~/.whereami.toml) for default CLI settings.

CLI flags always win over the config file; the config file always wins over
hardcoded defaults. Nothing here is required — an absent file just means
"use the built-in defaults".
"""

import tomllib
from pathlib import Path

DEFAULT_CONFIG_PATH = Path.home() / ".whereami.toml"

_KNOWN_KEYS = {
    "workers",
    "timeout",
    "host_concurrency",
    "categories",
    "only_found",
    "no_color",
    "format",
}


class ConfigError(RuntimeError):
    pass


def load_config(path: Path | None = None) -> dict:
    path = path or DEFAULT_CONFIG_PATH
    if not path.exists():
        return {}

    try:
        with open(path, "rb") as handle:
            data = tomllib.load(handle)
    except tomllib.TOMLDecodeError as exc:
        raise ConfigError(f"'{path}' is not valid TOML: {exc}") from exc
    except OSError as exc:
        raise ConfigError(f"could not read '{path}': {exc.strerror}") from exc

    unknown = set(data) - _KNOWN_KEYS
    if unknown:
        raise ConfigError(f"'{path}' has unknown setting(s): {', '.join(sorted(unknown))}")

    return data
