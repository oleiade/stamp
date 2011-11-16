StampIt
=======

A simple and extensible Python util which applies recursively to a given file, list of files, or list of directories a given License (Apache, BSD, GPL...).

### Still Missing
Under heavy development, major features are still missing, or may be buggy:
+ Permit License class easy subclassing in order to manage licenses as classes instead of raw files : example would be, you'd wanna bring a new kind of license to the util, you would only have to subclass License mother class. And that would be it.
+ Be able to change a yet applied license (apache for example), to another one (bsd for example)
+ Generically detect languages specifications in order not to override them while patching files with desired license. Such as '#!/usr/bin/env python\n#-* coding utf-8 *-#" thing in Python.
+ Anyone that you could notice

### If you'd wanna test it
Just clone this repository, and you're done, you'll be able to:
    ./license-applier.py <file/dir1,...,file/dir> license_file
    > license_file being containing a license text content
I'll make a clean package later.


### Coming improvements
+ more tests
+ packaging
+ better documentation : how to use/participate/extend
