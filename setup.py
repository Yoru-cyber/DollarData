from setuptools import setup


def readme():
    with open("README.md", "r") as f:
        return f.read()


setup(
    name="dollar_data",
    version="0.0.1",
    author="Carlos Mendez",
    author_email="carlosmendez170210@gmail.com",
    description=("Module that allows different operations with BCV's statistics"),
    license="BSD",
    packages=["dollar_data", "tests"],
    long_description=readme(),
    long_description_content_type="text/markdown",
)
