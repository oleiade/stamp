from setuptools import setup, find_packages
import stamp

setup(
    name = "Stamp",
    version = "0.1",
    packages = find_packages(),
    include_package_data = True,

    author = "Oleiade",
    author_email = "oleiade.nab@gmail.com",
    description = "Stamp applies a given license to a batch of files and folders",
    license = "Apache",
    keywords = "stamp license licenser open-source",
    url = "http://github.com/oleiade/stamp",

    # Requirements
    install_requires = [
        'simplejson'
    ],

    test_suite = "nose.collector",
    tests_require = "nose",

    # Setting up executable/main functions links
    entry_points = {
        'console_scripts': [
            'stamp = stamp.main:main',
        ]
    },

    classifiers = [
        'Development Status :: 0.1 - Early Alpha',
        'Environment :: Unix-like Systems',
        'Intended Audience :: Developers, Project managers, Sys admins',
        'Programming Language :: Python',
        'Operating System :: Unix-like',
    ],
)