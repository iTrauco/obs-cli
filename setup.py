from setuptools import setup, find_packages

setup(
    name='obsbot_cli',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'inquirer>=3.1.0',
        'click>=8.0.0',
        'rich>=10.0.0'
    ],
    entry_points={
        'console_scripts': [
            'obsbot=obsbot_cli.cli:main',
        ],
    },
)
