import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='aifig',
     version='0.1.6',
     author="Sigve Rokenes",
     author_email="me@evgiz.net",
     description="A machine learning figure generation library",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/evgiz/aifig",
     packages=["aifig"],
     install_requires=[
          'svgwrite'
     ],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent"
     ],
 )