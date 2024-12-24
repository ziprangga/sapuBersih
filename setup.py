from setuptools import setup, find_packages
import os


def read_file(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        return f.read()


setup(
    name="sapuBersih",
    version="1.5.0",
    author="ziprangga",
    author_email="ziprangga@gmail.com",
    description="A Cleaner Application",
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/your_username/sapuBersih",
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
    install_requires=[
        "PySide6",
        "PySide6_Addons",
        "PySide6_Essentials",
    ],
)
