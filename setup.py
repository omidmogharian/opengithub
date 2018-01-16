#!/usr/bin/env python
import octohub
import opengithub
import setuptools

setuptools.setup(
    name='opengithub',
    version=opengithub.__version__,
    description='Python interface to GitHub',
    long_description=open('README.rst').read(),
    author='Omid Mogharian',
    author_email='omid.mogharian@gmail.com',
    url='https://github.com/omidmogharian/opengithub',
    license='MIT',
    install_requires=[
        'requests'
    ],
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    ],
    packages=[
        'opengithub',
    ],
    entry_points={
        'console_scripts': [
            'opengithub=opengithub.__main__:main',
        ],
    }
)
