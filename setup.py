from setuptools import setup

setup(
    name="iirs",
    version="0.0.1",
    install_requires=['cryptography'],
    packages=['iirs', 'iirs.client', 'iirs.server'],
    entry_points= {
        'console_scripts': ['iirs-server = iirs.server.main:main'],
        'gui_scripts': ['iirs-client = iirs.client.main:main']
    }
)
