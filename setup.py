from distutils.core import setup

setup(
    name='ocdsort',
    version='0.0.2',
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
