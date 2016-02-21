from setuptools import setup
setup(name='akk',
      version='1.0',
      packages=['akk', "akk.db"],
      tests_require=['pytest', 'pytest-cov'],
      setup_requires=['pytest-runner'],
      )
