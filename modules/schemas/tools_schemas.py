from pydantic import BaseModel, Field
from typing import Optional


class WriteFileSpec(BaseModel):
    path: str = Field(..., description="Относительный путь к файлу в workspace.")
    content: str = Field(..., description="Содержимое файла.")

class CreateDirectorySpec(BaseModel):
    path: str = Field(..., description="Относительный путь к директории, которую нужно создать в workspace. Может включать родительские папки.")


class AppendToFileSpec(BaseModel):
    path: str = Field(..., description="Относительный путь к файлу в workspace.")
    content: str = Field(..., description="Содержимое для добавления в конец файла.")


class DeletePathSpec(BaseModel):
    path: str = Field(..., description="Относительный путь к файлу/директории в workspace.")


class ReadFileSpec(BaseModel):
    path: str = Field(..., description="Относительный путь к файлу в workspace.")


class ListDirectorySpec(BaseModel):
    path: Optional[str] = Field(default=".", description="Относительный путь к директории в workspace. По умолчанию - корень workspace.")


class RenameOrMoveSpec(BaseModel):
    source_path: str = Field(..., description="Текущий относительный путь в workspace.")
    destination_path: str = Field(..., description="Новый относительный путь в workspace.")
