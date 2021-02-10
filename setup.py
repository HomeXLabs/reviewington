import setuptools
from distutils.core import setup


setup(
  name = 'reviewington',
  packages = setuptools.find_packages(),
  scripts = ['rton'],
  version = '0.0.1',
  license='MIT',
  description = 'Reviewington gives you wings when reviewing code', #change later
  author = 'HomeX',
  author_email = 'reviewington@homex.com',
  url = 'https://github.com/HomeXLabs/reviewington',
  download_url = 'https://github.com/HomeXLabs/reviewington',
  classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
  ],
  install_requires=[
    "flask>=1.1",
    "markdown>=3.3",
    "pygithub>=1.54",
  ],
  python_requires='>=3.6'
)
