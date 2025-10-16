from pathlib import Path
import shutil

def ensure_dir(path: Path) -> None:
    """Создает директорию если она не существует"""
    path.mkdir(parents=True, exist_ok=True)

def copy_template(template_path: Path, destination: Path, variables: dict = None) -> None:
    """Копирует шаблонный файл с подстановкой переменных"""
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")
    
    content = template_path.read_text(encoding='utf-8')
    
    if variables:
        for key, value in variables.items():
            content = content.replace(f"{{{key}}}", str(value))
    
    destination.write_text(content, encoding='utf-8')