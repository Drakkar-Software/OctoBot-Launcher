#  Drakkar-Software OctoBot-Launcher
#  Copyright (c) Drakkar-Software, All rights reserved.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3.0 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library.

from setuptools import setup

from launcher import PROJECT_NAME, VERSION

setup(
    name=PROJECT_NAME,
    version=VERSION,
    url='https://github.com/Drakkar-Software/OctoBot-Launcher',
    license='LGPL-3.0',
    author='Drakkar-Software',
    author_email='drakkar.software@protonmail.com',
    description='Cryptocurrencies alert / trading bot',
    py_modules=['entrypoint'],
    packages=['launcher'],
    long_description='Cryptocurrencies alert / trading bot',
    install_requires=['requests'],
    tests_require=['pytest'],
    test_suite="tests",
    zip_safe=False,
    python_requires='>=3.7.2',
    entry_points={
        'console_scripts': [
            PROJECT_NAME + ' = entrypoint:main'
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
    ],
)
