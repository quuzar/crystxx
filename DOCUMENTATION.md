# Crystxx Documentation

## Quick Start

### Install
```bash
git clone https://github.com/mrquuzar/crystxx.git
cd crystxx
pip install -e .
```

### Create Project
```bash
# C++ project
crystxx --create MyProject --cpp 

# C project  
crystxx --create MyCProject --c

# With specific compiler
crystxx --create MyProject --cpp --g++ 
```

### Build & Run
```bash
cd MyProject
crystxx --build
crystxx --run
```

### Commands
crystxx --create NAME --cpp - Create C++ project
crystxx --create NAME --c  - Create C project
crystxx --build - Build project
crystxx --run - Run project

## Config File (config.txt)
### Basic Structure
```text
PROJECT myapp VERSION 1.0.0
LANGUAGE CPP STANDARD 20
COMPILER g++ FLAG -O2

CREATE_EXECUTOR myapp main.cpp
CREATE_LIB math src/math.cpp
INCLUDE_LIB math include/
INCLUDE_EXECUTOR myapp math
```

### Commands Explained
PROJECT - Set project name and version
```text
PROJECT name VERSION version
```

LANGUAGE - Set language and standard
```text
LANGUAGE [C|CPP] STANDARD [17|20|23]
```

COMPILER - Set compiler and flags
```text
COMPILER [gcc|g++|clang|clang++|auto] FLAG flag1 FLAG flag2...
```

CREATE_EXECUTOR - Create executable
```text
CREATE_EXECUTOR name main_file.c/cpp
```

CREATE_LIB - Create library from file or folder
```text
CREATE_LIB name path/to/source
```

INCLUDE_LIB - Add headers to library
```text
INCLUDE_LIB name path/to/headers
INCLUDE_LIB [name1,name2] path/to/headers
```

INCLUDE_EXECUTOR - Link library to executable
```text
INCLUDE_EXECUTOR executor_name library_name
```

## Project Structure
```text
MyProject/
├── config.txt
├── main.cpp (or main.c)
├── src/     # Your source files
├── lib/     # Your header files  
└── build/   # Built executables (created on build)
```

### Supported Compilers
GCC: gcc, g++
Clang: clang, clang++
MSVC: cl