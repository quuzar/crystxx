from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="crystxx",
    version="1.0.0",
    author="MrQuuzar",
    author_email="your.email@example.com",
    description="Modern C/C++ Build System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mrquuzar/crystxx",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "crystxx=crystxx.__main__:main",
        ],
    },
    package_data={
        "crystxx": ["templates/*.template"],
    },
    include_package_data=True,
)