from setuptools import setup

setup(
    name='aggiestack',
    version='0.1',
    py_modules=['aggiestack'],
    install_requires=[
        'Click'
    ],
    entry_points='''
        [console_scripts]
        aggiestack=aggiestack:cli
    '''
)
