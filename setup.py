"""Setup configuration for CFB Dynasty Data package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="cfb-dynasty-data",
    version="1.0.0",
    author="Christian Thomas",
    author_email="your.email@example.com",
    description="A comprehensive toolkit for managing college football dynasty rosters",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/CFB-Dynasty-Data",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Games/Entertainment :: Simulation",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    python_requires=">=3.11",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=22.0",
            "flake8>=5.0",
        ],
        "jupyter": [
            "jupyter>=1.0",
            "matplotlib>=3.5",
            "seaborn>=0.11",
        ],
    },
    entry_points={
        "console_scripts": [
            "cfb-dynasty=cfb_dynasty.analysis.roster_analysis:main",
            "cfb-roster-gen=cfb_dynasty.data.roster_generator:main",
        ],
    },
    include_package_data=True,
    package_data={
        "cfb_dynasty": ["config/*.py"],
    },
)
