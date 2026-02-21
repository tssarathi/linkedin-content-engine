from setuptools import find_packages, setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="researcher-agent",
    version="1.1.6",
    author="Sarathi",
    packages=find_packages(),
    install_requires=requirements,
)
