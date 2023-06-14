import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    # Here is the module name.
    name="objtyping",

    # version of the module
    version="0.5.3.r2",

    # Name of Author
    author="Song Hui",

    # your Email address
    author_email="songofhawk@gmail.com",

    # #Small Description about module
    description="convert a primitive dict-list data structure to/from an instance of user-defined class.",

    # Specifying that we are using markdown file for description
    long_description=long_description,
    long_description_content_type="text/markdown",

    # Any link to reach this module, ***if*** you have any webpage or github profile
    # url="https://github.com/username/",
    packages=setuptools.find_packages(),

    # if module has dependencies i.e. if your package rely on other package at pypi.org
    # then you must add there, in order to download every requirement of package

    #	 install_requires=[
    #	 "package1",
    # "package2",
    # ],

    license="MIT",

    # classifiers like program is suitable for python3, just leave as it is.
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
