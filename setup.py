from setuptools import setup, find_packages

setup(
    name='sphinx-ref-in-plantuml-hyperlinks',
    version='0.5.0',
    packages=find_packages(),
    author='Michael Parkes',
    author_email='mparkes@post.cz',
    description='sphinx-ref-in-plantuml-hyperlinks is a Sphinx extension to resolve std:ref-s defined in plantuml files',
    url='https://github.com/mi-parkes/sphinx-ref-in-plantuml-hyperlinks',
    license="MIT License",
    include_package_data=False,
    python_requires=">=3.10",
    install_requires=["Sphinx>=5.3.0"],
    long_description="",
    long_description_content_type='text/markdown'
)
