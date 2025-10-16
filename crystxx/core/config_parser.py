from pathlib import Path
from typing import Dict, List, Any, Optional
import os
import glob

class ConfigParser:
    def __init__(self, config_file: str = "config.txt"):
        self.config_file = Path(config_file)
        self.config = {}
        
    def parse(self) -> Dict[str, Any]:
        """Парсит config.txt файл"""
        if not self.config_file.exists():
            raise FileNotFoundError(f"Config file {self.config_file} not found")
        
        with open(self.config_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        self.config = {
            'project': {'name': '', 'version': '1.0.0'},
            'language': {'type': 'CPP', 'standard': '20'},
            'compiler': {'name': 'auto', 'flags': []},
            'executors': [],
            'libraries': {},
            'global_includes': []
        }
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            self._parse_line(line)
        
        return self.config
    
    def _parse_line(self, line: str):
        """Парсит одну строку конфига"""
        parts = line.split()
        if not parts:
            return
            
        command = parts[0].upper()
        
        if command == "PROJECT":
            self._parse_project(parts[1:])
        elif command == "LANGUAGE":
            self._parse_language(parts[1:])
        elif command == "COMPILER":
            self._parse_compiler(parts[1:])
        elif command == "CREATE_EXECUTOR":
            self._parse_create_executor(parts[1:])
        elif command == "CREATE_LIB":
            self._parse_create_lib(parts[1:])
        elif command == "INCLUDE_LIB":
            self._parse_include_lib(parts[1:])
        elif command == "INCLUDE_EXECUTOR":
            self._parse_include_executor(parts[1:])
    
    def _parse_project(self, parts: List[str]):
        """Парсит PROJECT команду"""
        if len(parts) >= 1:
            self.config['project']['name'] = parts[0]
            
        # Ищем VERSION
        for i, part in enumerate(parts):
            if part.upper() == "VERSION" and i + 1 < len(parts):
                self.config['project']['version'] = parts[i + 1]
                break
    
    def _parse_language(self, parts: List[str]):
        """Парсит LANGUAGE команду"""
        i = 0
        while i < len(parts):
            if parts[i].upper() in ['C', 'CPP']:
                self.config['language']['type'] = parts[i].upper()
            elif parts[i].upper() == "STANDARD" and i + 1 < len(parts):
                self.config['language']['standard'] = parts[i + 1]
                i += 1
            i += 1
    
    def _parse_compiler(self, parts: List[str]):
        """Парсит COMPILER команду"""
        i = 0
        flags_started = False
        
        while i < len(parts):
            if parts[i].upper() == "FLAG":
                flags_started = True
                i += 1
                continue
                
            if flags_started:
                self.config['compiler']['flags'].append(parts[i])
            else:
                self.config['compiler']['name'] = parts[i]
                
            i += 1
    
    def _parse_create_executor(self, parts: List[str]):
        """Парсит CREATE_EXECUTOR команду"""
        if len(parts) >= 2:
            self.config['executors'].append({
                'name': parts[0],
                'main_file': parts[1],
                'dependencies': []
            })
    
    def _parse_create_lib(self, parts: List[str]):
        """Парсит CREATE_LIB команду - теперь поддерживает папки"""
        if len(parts) >= 2:
            lib_name = parts[0]
            source_path = parts[1]
            
            # Находим все исходные файлы
            source_files = self._find_source_files(source_path)
            
            self.config['libraries'][lib_name] = {
                'name': lib_name,
                'source_files': source_files,
                'include_dirs': [],
                'dependencies': []
            }
    
    def _find_source_files(self, path: str) -> List[str]:
        """Находит все исходные файлы по пути (файл или папка)"""
        path_obj = Path(path)
        source_files = []
        
        if path_obj.is_file():
            # Если это файл - просто возвращаем его
            source_files.append(str(path_obj))
        elif path_obj.is_dir():
            # Если это папка - ищем все .c/.cpp файлы рекурсивно
            extensions = ['.c', '.cpp', '.cc', '.cxx']
            for ext in extensions:
                pattern = f"{path}/**/*{ext}"
                source_files.extend([str(Path(f)) for f in glob.glob(pattern, recursive=True)])
        
        return source_files
    
    def _parse_include_lib(self, parts: List[str]):
        """Парсит INCLUDE_LIB команду - теперь для конкретных библиотек"""
        if len(parts) < 2:
            return
            
        # Обрабатываем список библиотек в формате [lib1, lib2] или одиночное имя
        lib_names = []
        include_path = parts[-1]  # Последний элемент - путь
        
        if parts[0].startswith('[') and ']' in ' '.join(parts):
            # Обрабатываем список библиотек [lib1, lib2, ...] path
            libs_str = ' '.join(parts)
            start = libs_str.find('[')
            end = libs_str.find(']')
            
            if start != -1 and end != -1:
                libs_list = libs_str[start+1:end].split(',')
                lib_names = [lib.strip() for lib in libs_list]
                include_path = libs_str[end+1:].strip()
        else:
            # Одиночная библиотека
            lib_names = [parts[0]]
            include_path = parts[1]
        
        # Добавляем include пути к указанным библиотекам
        for lib_name in lib_names:
            if lib_name in self.config['libraries']:
                self.config['libraries'][lib_name]['include_dirs'].append(include_path)
    
    def _parse_include_executor(self, parts: List[str]):
        """Парсит INCLUDE_EXECUTOR команду"""
        if len(parts) >= 2:
            target_name = parts[0]
            lib_name = parts[1]
            
            # Ищем в исполнителях
            for executor in self.config['executors']:
                if executor['name'] == target_name:
                    executor['dependencies'].append(lib_name)
                    return
            
            # Ищем в библиотеках (поддержка вложенных зависимостей)
            for lib in self.config['libraries'].values():
                if lib['name'] == target_name:
                    lib['dependencies'].append(lib_name)
                    return
    
    def validate(self) -> bool:
        """Проверяет валидность конфигурации"""
        if not self.config['project']['name']:
            return False
            
        if not self.config['executors']:
            return False
            
        # Проверяем что все зависимости существуют
        for executor in self.config['executors']:
            for dep in executor.get('dependencies', []):
                if dep not in self.config['libraries']:
                    print(f"Warning: Executor '{executor['name']}' depends on unknown library '{dep}'")
        
        for lib_name, library in self.config['libraries'].items():
            for dep in library.get('dependencies', []):
                if dep not in self.config['libraries']:
                    print(f"Warning: Library '{lib_name}' depends on unknown library '{dep}'")
            
        return True