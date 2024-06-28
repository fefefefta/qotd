from setuptools import setup, find_packages

setup(
    name='qotd_api',
    version='0.1',
    package_dir={'': 'qotd_api'},
    packages=find_packages(where='qotd_api'),
)