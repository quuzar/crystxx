from pathlib import Path
import os
from typing import Optional

class ProjectCreator:
    def __init__(self):
        self.template_dir = Path(__file__).parent.parent / "templates"
    
    def create_project(self, name: str, language: str = "CPP", compiler: Optional[str] = None):
        """Создает новый проект"""
        project_dir = Path(name)
        project_dir.mkdir(exist_ok=True)
        
        # Создаем структуру папок
        (project_dir / "lib").mkdir(exist_ok=True)
        (project_dir / "src").mkdir(exist_ok=True)
        (project_dir / "build").mkdir(exist_ok=True)
        
        # Создаем основной файл
        self._create_main_file(project_dir, language)
        
        # Создаем config.txt
        self._create_config_file(project_dir, name, language, compiler)
        
        print(f"Created project structure for '{name}'")
        print(f"  - {name}/")
        print(f"  - {name}/main.{'cpp' if language == 'CPP' else 'c'}")
        print(f"  - {name}/config.txt")
        print(f"  - {name}/lib/")
        print(f"  - {name}/src/")
        print(f"  - {name}/build/")
    
    def _create_main_file(self, project_dir: Path, language: str):
        """Создает основной файл проекта"""
        if language == "C":
            template_file = self.template_dir / "main_c.template"
            main_file = project_dir / "main.c"
        else:
            template_file = self.template_dir / "main_cpp.template"
            main_file = project_dir / "main.cpp"
        
        if template_file.exists():
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            # Fallback template
            if language == "C":
                content = """#include <stdio.h>

int main() {
    printf("Hello from C project!\\n");
    return 0;
}
"""
            else:
                content = """#include <iostream>

int main() {
    std::cout << "Hello from C++ project!" << std::endl;
    return 0;
}
"""
        
        with open(main_file, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _create_config_file(self, project_dir: Path, name: str, language: str, compiler: Optional[str]):
        """Создает config.txt файл"""
        config_file = project_dir / "config.txt"
        
        # Определяем стандарт по умолчанию
        standard = "17" if language == "C" else "20"
        
        # Определяем компилятор по умолчанию
        if not compiler:
            compiler = "gcc" if language == "C" else "g++"
        
        config_content = f"""PROJECT {name} VERSION 1.0.0
LANGUAGE {language} STANDARD {standard}
COMPILER {compiler} FLAG -O2

CREATE_EXECUTOR {name} main.{'cpp' if language == 'CPP' else 'c'}

# CREATE_LIB mylib src/mylib.cpp
# INCLUDE_LIB lib/
# INCLUDE_EXECUTOR {name} mylib
"""
        
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(config_content)