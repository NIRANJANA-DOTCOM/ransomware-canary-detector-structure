from setuptools import setup, find_packages

setup(
    name="ransomware-canary-detector",
    version="1.0.0",
    author="Ruchir Ganatra",
    author_email="you@example.com",
    description="Early-warning ransomware detection tool using canary files.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Ranchiro/ransomware-canary-detector",
    project_urls={
        "Bug Tracker": "https://github.com/Ranchiro/ransomware-canary-detector/issues",
        "Documentation": "https://github.com/Ranchiro/ransomware-canary-detector/wiki",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Developers",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "watchdog",
        "pyyaml",
        "colorama"
    ],
    entry_points={
        'console_scripts': [
            'canary-detector = main:main'
        ]
    },
    include_package_data=True,
)
