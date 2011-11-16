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

    test_suite = "nose.collector",
    tests_require = "nose==1.1.2",
#    tests_require = "nose==1.0.0",

    # Setting up executable/main functions links
    entry_points = {
        'console_scripts': [
            'stamp = stamp.main:main',
        ]
    }
)