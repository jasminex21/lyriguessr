from setuptools import setup, find_packages

setup(
    name="lyriguessr",
    version='0.1',
    packages=find_packages(where="lyriguessr"),
    package_dir = {'': 'lyriguessr'}
)