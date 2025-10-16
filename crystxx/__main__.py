#!/usr/bin/env python3
import argparse
import sys
import os
from pathlib import Path

from core.project_creator import ProjectCreator
from core.builder import ProjectBuilder
from core.runner import ProjectRunner

def main():
    parser = argparse.ArgumentParser(description='Crystxx - Modern C/C++ Build System')
    parser.add_argument('--create', type=str, help='Create new project with given name')
    parser.add_argument('--build', action='store_true', help='Build the project')
    parser.add_argument('--run', action='store_true', help='Run the project')
    parser.add_argument('--c', action='store_true', help='Create C project')
    parser.add_argument('--cpp', action='store_true', help='Create C++ project')
    parser.add_argument('--gcc', action='store_true', help='Use GCC compiler')
    parser.add_argument('--g++', action='store_true', help='Use G++ compiler')
    parser.add_argument('--clang', action='store_true', help='Use Clang compiler')
    parser.add_argument('--clang++', action='store_true', help='Use Clang++ compiler')
    
    args = parser.parse_args()
    
    if args.create:
        # Определяем язык и компилятор
        language = "CPP" if args.cpp else "C" if args.c else "CPP"  # По умолчанию C++
        compiler = None
        if args.gcc: compiler = "gcc"
        elif args.g__: compiler = "g++"
        elif args.clang: compiler = "clang"
        elif args.clang__: compiler = "clang++"
        
        creator = ProjectCreator()
        creator.create_project(args.create, language, compiler)
        print(f"Project '{args.create}' created successfully!")
        
    elif args.build:
        builder = ProjectBuilder()
        if builder.build():
            print("Build completed successfully!")
        else:
            print("Build failed!")
            sys.exit(1)
            
    elif args.run:
        runner = ProjectRunner()
        if not runner.run():
            print("Run failed!")
            sys.exit(1)
            
    else:
        parser.print_help()

if __name__ == '__main__':
    main()