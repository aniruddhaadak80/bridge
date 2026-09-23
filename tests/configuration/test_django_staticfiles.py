import os

import pytest

from bridge.config import BridgeConfig
from bridge.framework.django import DjangoHandler
from bridge.platform import Platform

WHITE_NOISE = "whitenoise.middleware.WhiteNoiseMiddleware"
SECURITY = "django.middleware.security.SecurityMiddleware"


@pytest.fixture
def make_handler():
    def _make(middleware):
        return DjangoHandler(
            project_name="test",
            framework_locals={"BASE_DIR": "test", "MIDDLEWARE": middleware},
            bridge_config=BridgeConfig(),
        )

    return _make


def test_configure_staticfiles_tuple_middleware(make_handler):
    handler = make_handler((SECURITY, "django.middleware.common.CommonMiddleware"))
    handler.configure_staticfiles(platform=Platform.RENDER)
    assert handler.framework_locals["MIDDLEWARE"] == [
        SECURITY,
        WHITE_NOISE,
        "django.middleware.common.CommonMiddleware",
    ]
    assert handler.framework_locals["STATIC_ROOT"] == os.path.join(
        "test", "staticfiles"
    )


def test_configure_staticfiles_tuple_without_security_middleware(make_handler):
    handler = make_handler(("django.middleware.common.CommonMiddleware",))
    handler.configure_staticfiles(platform=Platform.RENDER)
    assert handler.framework_locals["MIDDLEWARE"] == [
        WHITE_NOISE,
        "django.middleware.common.CommonMiddleware",
    ]


def test_configure_staticfiles_list_middleware(make_handler):
    handler = make_handler([SECURITY])
    handler.configure_staticfiles(platform=Platform.RENDER)
    assert handler.framework_locals["MIDDLEWARE"] == [SECURITY, WHITE_NOISE]


def test_configure_staticfiles_missing_middleware():
    handler = DjangoHandler(
        project_name="test",
        framework_locals={"BASE_DIR": "test"},
        bridge_config=BridgeConfig(),
    )
    handler.configure_staticfiles(platform=Platform.RENDER)
    assert handler.framework_locals["MIDDLEWARE"] == [WHITE_NOISE]


def test_configure_staticfiles_none_middleware(make_handler):
    handler = make_handler(None)
    handler.configure_staticfiles(platform=Platform.RENDER)
    assert handler.framework_locals["MIDDLEWARE"] == [WHITE_NOISE]
