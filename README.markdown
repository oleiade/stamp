StampIt
=======

A simple and extensible Python util which applies recursively files or/and folder content a given (raw content) license
such as Apache, BSD, GPL... It automatically manages languages comment style. Though every languages are not managed, you'll
be able to add yours into the package constants.py soon (tag 0.0.3).

It's still in an early state of development (first release); and only works as a one shot patching at the moment. Already 
patched file detection and incremental patching will be managed in the next release.

Installation
------------
```bash
python setup.py build
python setup.py install
```
Project will be pushed to pypi when more mature (approximatively 0.0.3/0.0.4 release tag)


Usage
-----
```bash
stamp license_file file/folders ...
```
license_file arg has to be a file suffixed with the extension '.lic'. It should contain the raw license content you'd wanna
apply to the content of
file/folders you've specified.

### Options
+ -v verbose mode

### Nota Bene
Example license files are given in the project license_files folder, take a look to their content in order to create 
yours.



Incoming improvements
---------------------
+ Incremental patching (managing already patched files, changing an already applied license)
+ Better performances on large stack of files to patch
+ File/folders scanning to fine existing license and beautiful verbose output
+ more robust testing
+ better documentation : how to use/participate/extend
incoming features and bugs are referenced in the Github issue tracker of the project.