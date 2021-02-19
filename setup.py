from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="duffel-api-client",
    version="0.0.1",
    author="Duffel Engineering",
    author_email="client-libraries@duffel.com",
    description="Client library for the Duffel API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/duffelhq/duffel-python-api-client",
    packages=setuptools.find_packages(),
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
    ],
    keywords='duffel api flights airports airlines aircraft',
    python_requires='>=3.6',
)
