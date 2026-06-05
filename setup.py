"""
Setup script for ClipMind.
"""

from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="clipmind",
    version="1.0.0",
    author="ClipMind Team",
    author_email="clipmind@example.com",
    description="🧠 Intelligent Terminal Clipboard History Manager",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitstq/ClipMind",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "Topic :: Terminals",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "clipmind=clipmind.cli:main",
            "cm=clipmind.cli:main",
        ],
    },
    keywords="clipboard history terminal cli tui developer-tools productivity",
    project_urls={
        "Bug Reports": "https://github.com/gitstq/ClipMind/issues",
        "Source": "https://github.com/gitstq/ClipMind",
    },
)
