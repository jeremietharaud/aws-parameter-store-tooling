import codecs
import os.path
import re
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    return codecs.open(os.path.join(here, *parts), 'r').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name="aws-parameter-store",
    version=find_version("aws_parameter_store", "__init__.py"),
    author="Jeremie Tharaud",
    author_email="jeremie.tharaud@gmail.com",
    description="A tool for managing AWS Parameter Store",
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    url="https://github.com/jeremietharaud/aws-parameter-store-tooling",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache License",
        "Operating System :: OS Independent",
    ],
    entry_points='''
        [console_scripts]
        aws-parameter-store=aws_parameter_store.manage:main
    ''',
    license='Apache',
    install_requires=[
        'numpy',
        'boto3',
    ],
    include_package_data=True,
    zip_safe=False
)
