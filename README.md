# Crystxx - Modern C/C++ Build System

**Crystxx** - это современная система сборки для C/C++ проектов, написанная на Python. Простая конфигурация, поддержка современных стандартов и компиляторов.

## Быстрый старт

### Установка

```bash
# Установка из исходного кода
git clone https://github.com/quuzar/crystxx.git
cd crystxx
pip install -e .
```

### Создание первого проекта

```bash
# Создать C++ проект
crystxx --create --cpp MyProject

# Создать C проект
crystxx --create --c MyCProject

# Перейти в проект и собрать
cd MyProject
crystxx --build
crystxx --run
```

### Особенности
Простая конфигурация - текстовый файл config.txt
Поддержка современных стандартов - C17, C++20, C++23
Мультикомпилятор - GCC, Clang, MSVC
Гибкая система библиотек - создание и подключение библиотек

### Требования
Python 3.8+
Один из поддерживаемых компиляторов

### Лицензия
MIT License - смотрите файл LICENSE для подробностей