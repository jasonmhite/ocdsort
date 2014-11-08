from setuptools import setup

setup(
    name='ocdsort',
    version='0.0.3',
    packages=['ocdsort'],
    install_requires=[
        'click',
        'guessit',
        'pyaml',
    ],
    entry_points="""
        [console_scripts]
        ocdsort=ocdsort.cli:cli
    """,
)
