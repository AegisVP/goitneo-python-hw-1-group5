from pathlib import Path
from setuptools import setup, find_namespace_packages

long_description = Path("README.md").read_text()

setup(name='goitneo-python-hw-1-group5',
      version="0.0.1",
      description="GoIT NeoVersity Python Homework 1",
      long_description=long_description,
      url="https://github.com/AegisVP/goitneo-python-hw-1-group5",
      author='Vladyslav Pysarenko',
      author_email='vlad@pysarenko.com',
      license='MIT',
      packages=find_namespace_packages(),
      classifiers=["Programming Language :: Python :: 3"],
      install_requires=['faker'],
      package_data={"":["*.json"]},
      include_package_data=False,
      entry_points={'console_scripts': [
          'get_birthdays_per_week = assignment1.main:get_birthdays_per_week',
          'run_bot = assignment2.main:run_bot'
      ]}
)
