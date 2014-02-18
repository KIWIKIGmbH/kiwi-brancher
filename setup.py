from setuptools import setup


setup(
    name="kiwibrancher",
    version="0.1",
    entry_points={
        "console_scripts": ["kiwibrancher=kiwibrancher.command_line:main"],
    })
