from setuptools import setup, find_namespace_packages

setup(name='GoIT NEO Python HW 1',
      version="0.0.1",
      description="GoIT NeoVersity Python Homework 1",
      url="https://github.com/AegisVP/goitneo-python-hw-1-group5",
      author='Vladyslav Pysarenko',
      author_email='vlad@pysarenko.com',
      license='MIT',
      packages=find_namespace_packages(),
      install_requires=['faker'],
      entry_points={'console_scripts': [
          'run_work1 = assignment1.main:run_code',
          'run_work2 = assignment2.main:run_code'
      ]}
)
