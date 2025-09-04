import os
import pytest
from main import write_file, edit_file, delete_file, delete_directory, read_file, list_directory

# Фикстура для создания тестовой директории и файлов
@pytest.fixture
def test_directory(tmpdir):
    test_dir = tmpdir.mkdir("test_dir")
    test_file = test_dir.join("test_file.txt")
    test_file.write("initial content")
    yield str(test_dir)
    # Очистка после теста
    # shutil.rmtree(str(test_dir))  # Лучше использовать tmpdir, чтобы pytest сам убирал временные файлы

def test_write_file(test_directory):
    file_path = os.path.join(test_directory, "new_file.txt")
    result = write_file(file_path, "test content")
    assert "успешно создан/перезаписан" in result
    with open(file_path, "r") as f:
        assert f.read() == "test content"

def test_edit_file(test_directory):
    file_path = os.path.join(test_directory, "test_file.txt")
    result = edit_file(file_path, " appended content")
    assert "успешно отредактирован" in result
    with open(file_path, "r") as f:
        assert f.read() == "initial content appended content"

def test_delete_file(test_directory):
    file_path = os.path.join(test_directory, "test_file.txt")
    result = delete_file(file_path)
    assert "успешно удален" in result
    assert not os.path.exists(file_path)

def test_delete_directory(test_directory):
    result = delete_directory(test_directory)
    assert "успешно удалены" in result
    assert not os.path.exists(test_directory)

def test_read_file(test_directory):
    file_path = os.path.join(test_directory, "test_file.txt")
    result = read_file(file_path)
    assert "Содержимое файла" in result
    assert "initial content" in result

def test_list_directory(test_directory):
    result = list_directory(test_directory)
    assert "Содержимое директории" in result
    assert "[F] test_file.txt" in result

def test_list_directory_empty(tmpdir):
    test_dir = tmpdir.mkdir("empty_dir")
    result = list_directory(str(test_dir))
    assert "Директория" in result
    assert "пуста" in result

def test_list_directory_not_found():
    result = list_directory("non_existent_dir")
    assert "не является директорией" in result