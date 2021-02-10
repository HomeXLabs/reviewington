import setuptools
from distutils.core import setup


setup(
    name="reviewington",
    packages=setuptools.find_packages(),
    scripts=["rton"],
    version="0.0.1",
    license="MIT",
    description="Reviewington gives you wings when reviewing code",  # change later
    author="HomeX",
    author_email="reviewington@homex.com",
    url="https://github.com/HomeXLabs/reviewington",
    download_url="https://github.com/HomeXLabs/reviewington",
    package_dir={"reviewington": "reviewington"},
    package_data={
        "reviewington": ["templates/*"],
        "reviewington": ["static/css/*"],
        "reviewington": ["github_templates/*"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)
