import os
import pytest
from pathlib import Path
from modules.utils.tools import write_file
from modules.settings.agent_config import settings


@pytest.fixture
def setup_workspace(tmp_path: Path):
    """
    Фикстура для создания временной рабочей директории и установки ее в настройках.
    """
    original_workspace = settings.WORKSPACE_DIR
    test_workspace = tmp_path / "test_workspace"

    test_workspace.mkdir()
    test_file = test_workspace / "test_overwrite.txt"
    test_file.write_text("Initial content.", encoding="utf-8")

    settings.WORKSPACE_DIR = str(test_workspace)

    # Переинициализация REAL_WORKSPACE_PATH в тестируемом модуле
    import modules.utils.tools

    modules.utils.tools.REAL_WORKSPACE_PATH = os.path.realpath(settings.WORKSPACE_DIR)

    yield str(test_workspace)

    # Восстановление исходной рабочей директории после теста
    settings.WORKSPACE_DIR = original_workspace
    modules.utils.tools.REAL_WORKSPACE_PATH = os.path.realpath(settings.WORKSPACE_DIR)


@pytest.mark.parametrize(
    "test_path, test_content, test_id",
    [
        ("test_file.txt", "This is a test content.", "simple_file"),
        (
            "nested/dir/test_file.txt",
            "Content in a nested directory.",
            "nested_directories",
        ),
    ],
)
def test_write_file_creates_and_writes_successfully(
    setup_workspace, test_path, test_content, test_id
):
    """
    Параметризованный тест для проверки успешного создания/перезаписи файла.
    Проверяет как простой случай, так и создание вложенных директорий.
    """
    result = write_file(test_path, test_content)

    assert result == f"Файл '{test_path}' успешно создан/перезаписан."

    full_path = Path(setup_workspace) / test_path
    assert full_path.exists(), f"Файл должен был быть создан по пути {full_path}"
    assert full_path.read_text(encoding="utf-8") == test_content


def test_write_file_overwrite_existing_file(setup_workspace):
    """
    Тест перезаписи существующего файла.
    """
    file_path = "test_overwrite.txt"
    new_content = "New overwritten content."

    full_path = Path(setup_workspace) / file_path

    assert full_path.exists()
    assert full_path.read_text(encoding="utf-8") == "Initial content."

    result = write_file(file_path, new_content)
    assert result == f"Файл '{file_path}' успешно создан/перезаписан."
    assert full_path.exists()
    assert full_path.read_text(encoding="utf-8") == new_content


def test_write_file_path_traversal_attack(setup_workspace):
    """
    Тест на попытку записи файла за пределами рабочей директории.
    """
    malicious_path = "../../../test_outside.txt"
    content = "This should not be written."

    result = write_file(malicious_path, content)

    assert "Попытка доступа за пределы рабочей директории" in result

    assert not (Path(setup_workspace) / malicious_path).resolve().exists()
