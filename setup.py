from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="codecollector",
    version="0.1.0",
    author="Domagoj Lovric",
    author_email="dominic@algorise.co.uk",
    description="A CLI tool to aggregate and organize code files from complex projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DLOVRIC2/code_collector",
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    install_requires=[
        "click",
        "PyYAML",
        "prompt_toolkit",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "codecollector=codecollector.cli:main",
        ],
    },
    keywords="code aggregator organizer cli development",
    project_urls={
        "Bug Tracker": "https://github.com/DLOVRIC2/code_collector/issues",
    },
)
