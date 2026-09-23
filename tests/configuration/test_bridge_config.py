import pytest

import bridge.config as bridge_config_module
from bridge.config import BridgeConfig, get_config


@pytest.fixture
def isolated_config(tmp_path, monkeypatch):
    monkeypatch.setattr(bridge_config_module, "CONFIG_PATH", tmp_path / "bridge.yaml")
    monkeypatch.setattr(bridge_config_module, "__CONFIG", None)
    monkeypatch.chdir(tmp_path)
    return tmp_path


def test_get_config_creates_default_when_missing(isolated_config):
    config = get_config()
    assert config == BridgeConfig()
    assert (isolated_config / "bridge.yaml").exists()


def test_get_config_reads_valid_yaml(isolated_config):
    (isolated_config / "bridge.yaml").write_text("enable_postgres: false\n")
    config = get_config()
    assert config.enable_postgres is False
    assert config.enable_worker is True


def test_get_config_malformed_yaml_falls_back_to_default(isolated_config, mocker):
    (isolated_config / "bridge.yaml").write_text("enable_postgres: [unclosed\n")
    mock_warning = mocker.patch("bridge.config.log_warning")
    config = get_config()
    assert config == BridgeConfig()
    mock_warning.assert_called_once()


def test_get_config_empty_file_falls_back_to_default(isolated_config, mocker):
    (isolated_config / "bridge.yaml").write_text("")
    mock_warning = mocker.patch("bridge.config.log_warning")
    config = get_config()
    assert config == BridgeConfig()
    mock_warning.assert_called_once()


def test_get_config_wrong_types_fall_back_to_default(isolated_config, mocker):
    (isolated_config / "bridge.yaml").write_text("enable_postgres: [1, 2]\n")
    mock_warning = mocker.patch("bridge.config.log_warning")
    config = get_config()
    assert config == BridgeConfig()
    mock_warning.assert_called_once()


def test_get_config_non_mapping_yaml_falls_back_to_default(isolated_config, mocker):
    (isolated_config / "bridge.yaml").write_text("- a\n- b\n")
    mock_warning = mocker.patch("bridge.config.log_warning")
    config = get_config()
    assert config == BridgeConfig()
    mock_warning.assert_called_once()
