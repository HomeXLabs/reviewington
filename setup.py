import setuptools
from distutils.core import setup


setup(
    name="reviewington",
    packages=setuptools.find_packages(),
    scripts=["rton"],
    license="MIT",
    version="1.0.0",
    description="Reviewington gives you wings when reviewing code",  # change later
    author="HomeX",
    author_email="reviewington@homex.com",
    url="https://github.com/HomeXLabs/reviewington",
    download_url="https://github.com/HomeXLabs/reviewington",
    package_dir={"reviewington": "reviewington"},
    package_data={
        "reviewington": [
            "templates/*",
            "static/css/*",
            "static/img/*",
            "about.txt",
            "github_action_template/*",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=[
        "flask>=1.1",
        "Markdown>=3.3.3",
        "PyGithub>=1.54.1",
        "Pygments>=2.7.4",
    ],
    python_requires=">=3.6",
)
