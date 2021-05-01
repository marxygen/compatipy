import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="compatipy",
    version="0.0.1",
    author="marxygen",
    author_email="marxygen@gmail.com",
    description="A library to use code for Python 2 in Python 3.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marxygen/compatipy",
    project_urls={
        "Bug Tracker": "https://github.com/marxygen/compatipy/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "compatipy"},
    packages=setuptools.find_packages(where="compatipy"),
    python_requires=">=3.6",
)