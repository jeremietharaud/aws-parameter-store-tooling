from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="aws-parameter-store",
    version="1.0.0",
    author="Jeremie Tharaud",
    author_email="jeremie.tharaud@gmail.com",
    description="A tool for managing AWS Parameter Store",
    long_description=long_description,
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