from setuptools import setup

setup(
    name='sorter',
    version='0.0.1',
    packages=['sorter'],
    entry_points="""
        [console_scripts]
        anisorter=sorter.cli:cli
    """,
)
