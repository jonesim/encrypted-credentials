import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="encrypted-credentials",
    version="0.0.2",
    author="Ian Jones",
    description="Encrypt credentials/Django settings to store in repositories",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jonesim/encrypted-credentials",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['cryptography'],
)