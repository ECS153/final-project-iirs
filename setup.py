from setuptools import setup

setup(
    name="iirs",
    version="0.0.1",
    install_requires=['cryptography'],
    packages=['iirs', 'iirs.client', 'iirs.server'],
)
