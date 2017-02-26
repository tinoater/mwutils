from distutils.core import setup
from setuptools import find_packages

setup(
    name='mwutils',
    version='1.0.11',
    url='https://github.com/tinoater/mwutils.git',
    license='',
    author='bobby',
    author_email='',
    description='',
    packages=find_packages(exclude=('Tests', 'Files')),
    include_package_data=True
)
