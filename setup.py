import io
import os
from datetime import datetime
from setuptools import setup, find_packages


setup(
    name="newreleases",
    version=os.environ.get("CI_BUILD_TAG", "0.0.0"),
    description="Unofficial python client for https://newreleases.io",
    long_description=io.open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    platforms=["Windows", "POSIX", "MacOS"],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache License Version 2.0",
        "Natural Language :: English",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
    ],
    keywords="pypi requirements.txt newreleases",
    author="Viktor Kerkez",
    author_email="alefnula@gmail.com",
    maintainer="Viktor Kerkez",
    maintainer_email="alefnula@gmail.com",
    url="https://github.com/alefnula/newreleases",
    license=f"Copyright © {datetime.now():%Y} Viktor Kerkez",
    packages=find_packages(),
    install_requires=io.open("requirements.txt").read().splitlines(),
    include_package_data=True,
    scripts=[],
    entry_points="""
        [console_scripts]
        newreleases=newreleases.__main__:cli
    """,
)
