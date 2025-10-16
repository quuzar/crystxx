from pathlib import Path
import subprocess
import sys

from .config_parser import ConfigParser

class ProjectRunner:
    def __init__(self, config_file: str = "config.txt"):
        self.config_file = Path(config_file)
        self.parser = ConfigParser(config_file)
        
    def run(self) -> bool:
        """Запускает проект"""
        try:
            config = self.parser.parse()
            
            build_dir = Path("build")
            executable = build_dir / config['project']['name']
            
            # Для Windows добавляем .exe если нужно
            if not executable.exists():
                executable = executable.with_suffix(".exe")
            
            if not executable.exists():
                print(f"Executable not found: {executable}")
                print("Please build the project first with: crystxx --build")
                return False
            
            print(f"Running: {executable}")
            result = subprocess.run([str(executable)])
            return result.returncode == 0
            
        except Exception as e:
            print(f"Run error: {e}")
            return False