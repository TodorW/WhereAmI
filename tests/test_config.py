import pytest

from whereami.config import ConfigError, load_config


def test_missing_file_returns_empty_dict(tmp_path):
    assert load_config(tmp_path / "nope.toml") == {}


def test_valid_config_is_loaded(tmp_path):
    path = tmp_path / "cfg.toml"
    path.write_text('workers = 5\ncategories = ["Development"]\n', encoding="utf-8")
    assert load_config(path) == {"workers": 5, "categories": ["Development"]}


def test_invalid_toml_raises(tmp_path):
    path = tmp_path / "bad.toml"
    path.write_text("not = [valid", encoding="utf-8")
    with pytest.raises(ConfigError):
        load_config(path)


def test_unknown_key_raises(tmp_path):
    path = tmp_path / "unk.toml"
    path.write_text("nonsense_key = 1\n", encoding="utf-8")
    with pytest.raises(ConfigError):
        load_config(path)
