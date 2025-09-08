# tests/test_security.py
import pytest
import os
from modules.utils.tools import _get_safe_path
from modules.settings.agent_config import settings


# Убедимся, что workspace существует для тестов
os.makedirs(settings.WORKSPACE_DIR, exist_ok=True)
REAL_WORKSPACE_PATH = os.path.realpath(settings.WORKSPACE_DIR)


def test_safe_path_allows_valid_paths():
    """Тест: функция должна разрешать безопасные пути внутри workspace."""
    assert _get_safe_path("project/file.txt").startswith(REAL_WORKSPACE_PATH)
    assert _get_safe_path("file.txt").startswith(REAL_WORKSPACE_PATH)


def test_safe_path_blocks_path_traversal():
    """Тест: функция должна блокировать попытки выхода из workspace."""
    with pytest.raises(ValueError):
        _get_safe_path("../secret.txt")

    with pytest.raises(ValueError):
        _get_safe_path("project/../../../etc/passwd")


def test_safe_path_handles_absolute_paths():
    """Тест: функция должна игнорировать абсолютные пути, если они ведут извне."""
    with pytest.raises(ValueError):
        _get_safe_path("/etc/passwd")
