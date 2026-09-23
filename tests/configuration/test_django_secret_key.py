import pytest

from bridge.config import BridgeConfig
from bridge.framework.django import DjangoHandler
from bridge.platform import Platform


@pytest.fixture
def django_handler():
    return DjangoHandler(
        project_name="test",
        framework_locals={"SECRET_KEY": "settings-secret"},
        bridge_config=BridgeConfig(),
    )


def test_configure_secret_key_same_value_does_not_log(
    django_handler, monkeypatch, mocker
):
    monkeypatch.setenv("SECRET_KEY", "settings-secret")
    mock_info = mocker.patch("bridge.framework.django.log_info")
    django_handler.configure_secret_key(platform=Platform.RENDER)
    assert django_handler.framework_locals["SECRET_KEY"] == "settings-secret"
    mock_info.assert_not_called()


def test_configure_secret_key_different_value_overwrites_and_logs(
    django_handler, monkeypatch, mocker
):
    monkeypatch.setenv("SECRET_KEY", "env-secret")
    mock_info = mocker.patch("bridge.framework.django.log_info")
    django_handler.configure_secret_key(platform=Platform.RENDER)
    assert django_handler.framework_locals["SECRET_KEY"] == "env-secret"
    mock_info.assert_called_once()


def test_configure_secret_key_missing_env_leaves_value(
    django_handler, monkeypatch, mocker
):
    monkeypatch.delenv("SECRET_KEY", raising=False)
    mock_info = mocker.patch("bridge.framework.django.log_info")
    django_handler.configure_secret_key(platform=Platform.RENDER)
    assert django_handler.framework_locals["SECRET_KEY"] == "settings-secret"
    mock_info.assert_not_called()
