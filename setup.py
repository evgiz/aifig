import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='aifig',
     version='0.1',
     scripts=['example'],
     author="Sigve Rokenes",
     author_email="me@evgiz.net",
     description="A machine learning figure generator script",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/evgiz/aifig",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )