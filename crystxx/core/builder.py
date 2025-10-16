from pathlib import Path
import subprocess
import sys
from typing import List, Dict, Any, Set
import os
import glob

from .config_parser import ConfigParser

class ProjectBuilder:
    def __init__(self, config_file: str = "config.txt"):
        self.config_file = Path(config_file)
        self.parser = ConfigParser(config_file)
        self.config: Dict[str, Any] = {}
        
    def build(self) -> bool:
        """Собирает проект"""
        try:
            self.config = self.parser.parse()
            
            if not self.parser.validate():
                print("Invalid configuration!")
                return False
            
            print(f"Building project: {self.config['project']['name']}")
            
            # Определяем компилятор
            compiler = self._get_compiler()
            
            # Собираем все исходные файлы с учетом зависимостей
            source_files, include_dirs = self._resolve_dependencies()
            
            if not source_files:
                print("No source files found!")
                return False
            
            # Компилируем в монолитный исполняемый файл
            return self._compile_monolithic(compiler, source_files, include_dirs)
            
        except Exception as e:
            print(f"Build error: {e}")
            return False
    
    def _get_compiler(self) -> str:
        """Определяет компилятор для использования"""
        config_compiler = self.config['compiler']['name']
        language = self.config['language']['type']
        
        if config_compiler != "auto":
            return config_compiler
        
        # Автоопределение
        compilers = {
            "C": ["gcc", "clang"],
            "CPP": ["g++", "clang++"]
        }
        
        for compiler in compilers[language]:
            try:
                subprocess.run([compiler, "--version"], capture_output=True, check=True)
                return compiler
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue
        
        raise RuntimeError(f"No suitable compiler found for {language}")
    
    def _resolve_dependencies(self) -> tuple[List[Path], List[Path]]:
        """Разрешает зависимости и возвращает все исходные файлы и include директории"""
        all_source_files: Set[Path] = set()
        all_include_dirs: Set[Path] = set()
        
        # Обрабатываем исполнителей и их зависимости
        for executor in self.config['executors']:
            # Добавляем основной файл исполнителя
            main_file = Path(executor['main_file'])
            if main_file.exists():
                all_source_files.add(main_file.resolve())
            
            # Добавляем зависимости исполнителя
            for lib_name in executor.get('dependencies', []):
                if lib_name in self.config['libraries']:
                    lib = self.config['libraries'][lib_name]
                    self._add_library_files(lib, all_source_files, all_include_dirs)
        
        # Добавляем include директории из конфига
        for include_path in self.config.get('global_includes', []):
            include_dir = Path(include_path)
            if include_dir.exists():
                all_include_dirs.add(include_dir.resolve())
        
        return list(all_source_files), list(all_include_dirs)
    
    def _add_library_files(self, library: Dict, source_files: Set[Path], include_dirs: Set[Path]):
        """Рекурсивно добавляет файлы библиотеки и её зависимости"""
        # Добавляем исходные файлы библиотеки
        for source_file in library.get('source_files', []):
            source_path = Path(source_file)
            if source_path.exists():
                source_files.add(source_path.resolve())
        
        # Добавляем include директории библиотеки
        for include_dir in library.get('include_dirs', []):
            include_path = Path(include_dir)
            if include_path.exists():
                include_dirs.add(include_path.resolve())
        
        # Рекурсивно обрабатываем зависимости
        for dep_name in library.get('dependencies', []):
            if dep_name in self.config['libraries']:
                dep_lib = self.config['libraries'][dep_name]
                self._add_library_files(dep_lib, source_files, include_dirs)
    
    def _compile_monolithic(self, compiler: str, source_files: List[Path], include_dirs: List[Path]) -> bool:
        """Компилирует все в один исполняемый файл"""
        build_dir = Path("build")
        build_dir.mkdir(exist_ok=True)
        
        output_file = build_dir / self.config['project']['name']
        if compiler in ["cl", "clang-cl"] or os.name == 'nt':
            output_file = output_file.with_suffix(".exe")
        
        # Формируем команду компиляции
        cmd = [compiler]
        
        # Добавляем стандарт
        language = self.config['language']['type']
        standard = self.config['language']['standard']
        if compiler in ["gcc", "g++", "clang", "clang++"]:
            std_flag = "-std=c++" if language == "CPP" else "-std=c"
            cmd.append(f"{std_flag}{standard}")
        elif compiler in ["cl"]:
            cmd.append(f"/std:c++{standard}")
        
        # Добавляем флаги компиляции
        cmd.extend(self.config['compiler']['flags'])
        
        # Добавляем include пути
        for include_dir in include_dirs:
            if compiler in ["gcc", "g++", "clang", "clang++"]:
                cmd.append(f"-I{include_dir}")
            elif compiler in ["cl"]:
                cmd.append(f"/I{include_dir}")
        
        # Добавляем исходные файлы
        cmd.extend([str(f) for f in source_files])
        
        # Добавляем выходной файл
        if compiler in ["gcc", "g++", "clang", "clang++"]:
            cmd.extend(["-o", str(output_file)])
        elif compiler in ["cl"]:
            cmd.extend([f"/Fe{output_file}"])
        
        print(f"Source files: {[str(f) for f in source_files]}")
        print(f"Include dirs: {[str(f) for f in include_dirs]}")
        print(f"Compiling with: {' '.join(cmd)}")
        
        # Выполняем компиляцию
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print("Compilation failed!")
            print(result.stderr)
            return False
        
        print(f"Successfully built: {output_file}")
        return True