# This is my README

##Important notice

Since Xcode 5.1, some unknown argument warnings turn into errors, which blocks the installation of the pillow library. One way to overcome this issue is to use the following command:

	$ ARCHFLAGS=-Wno-error=unused-command-line-argument-hard-error-in-future pip install pillow

More info in this great article from @kaspermunck: http://kaspermunck.github.io/2014/03/fixing-clang-error/