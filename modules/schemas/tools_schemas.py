from pydantic import BaseModel, Field
from typing import Optional


class WriteFileSpec(BaseModel):
    path: str = Field(..., description="Путь к файлу.")
    content: str = Field(..., description="Содержимое файла.")


class CreateDirectorySpec(BaseModel):
    path: str = Field(
        ...,
        description="Путь к директории, которую нужно создать. Может включать родительские папки.",
    )


class AppendToFileSpec(BaseModel):
    path: str = Field(..., description="Путь к файлу.")
    content: str = Field(..., description="Содержимое для добавления в конец файла.")


class DeletePathSpec(BaseModel):
    path: str = Field(..., description="Путь к файлу/директории.")


class ReadFileSpec(BaseModel):
    path: str = Field(..., description="Путь к файлу.")


class ListDirectorySpec(BaseModel):
    path: Optional[str] = Field(
        default=".", description="Путь к директории. По умолчанию - корень."
    )


class RenameOrMoveSpec(BaseModel):
    source_path: str = Field(..., description="Текущий Путь.")
    destination_path: str = Field(..., description="Новый Путь.")
