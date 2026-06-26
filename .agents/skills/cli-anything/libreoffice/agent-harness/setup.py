from setuptools import setup, find_namespace_packages

setup(
    name="cli-anything-libreoffice",
    version="0.1.0",
    packages=find_namespace_packages(include=["cli_anything.*"]),
    namespace_packages=["cli_anything"],
    install_requires=[
        "click>=8.0.0",
        "prompt-toolkit>=3.0.0",
    ],
    extras_require={
        "merge": ["pypdf>=3.0.0"],
        "magic": ["python-magic>=0.4.0"],
    },
    entry_points={
        "console_scripts": [
            "cli-anything-libreoffice=cli_anything.libreoffice.libreoffice_cli:cli",
        ],
    },
    python_requires=">=3.10",
    description="CLI harness for LibreOffice — document conversion and batch operations",
    author="QoderWork Agent",
)
