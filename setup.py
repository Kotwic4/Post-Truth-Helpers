#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup


requirements = [

]

test_requirements = [
    'pytest',
]

setup(
    name='pt_helpers',
    version='0.1.0',
    description="Set of tools to help user find if information is true.",
    long_description=open('README.md').read(),
    author="Radomir Krawczykiewicz",
    author_email='kotwic4@gmail.com',
    url='https://github.com/AGHPythonCourse2017/zad3-Kotwic4',
    packages=[
        'pt_helpers',
    ],
    package_dir={'pt_helpers':
                 'pt_helpers'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='pt_helpers',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
