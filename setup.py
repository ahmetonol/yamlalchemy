#
from setuptools import setup

setup(
    name='yamlalchemy',
    version='0.1.0',
    description='YAMLAlchemy is a Python-based library to convert YAML to SQLAlchemy read-only queries.',
    url='https://github.com/ahmetonol/yamlalchemy',
    author='Ahmet Onol',
    author_email='onol.ahmet@gmail.com',
    license='MIT',
    packages=['yamlalchemy'],
    install_requires=[
        'PyYAML',
        'SQLAlchemy'
    ],

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
