from setuptools import setup



setup(

    name='macchanger',

    version='1.0',

    py_modules=['macchanger'],

    install_requires=[],

    entry_points={

        'console_scripts': [

            'macchanger=macchanger:main',

        ],

    },

)

