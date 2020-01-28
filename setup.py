from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='ipparser',
    version='0.3.6',
    author = 'm8r0wn',
    author_email = 'm8r0wn@protonmail.com',
    description = 'Parse IP address information and return a list for iteration.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/m8r0wn/ipparser',
    license='BSD 3-clause',
    classifiers = [
        "Environment :: Console",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License"
    ],
    packages=['ipparser'],
    install_requires = ['dnspython']
)
