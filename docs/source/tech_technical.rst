.. _a_tech:

*********************
Technical Information
*********************

This section contains details of how novelWriter stores and handles the project data.


How Data is Stored
==================

All novelWriter files are written with utf-8 encoding. Since Python automatically converts Unix line
endings to Windows line endings on Windows systems, novelWriter does not make any adaptations to the
formatting on Windows systems. This is handled entirely by the Python standard library. Python also
handles this fairly well when working on the same files on both Windows and Unix-based operating
systems.


Main Project File
-----------------

The project itself requires a dedicated folder for storing its files, where novelWriter will create
its own "file system" where the folder and file hierarchy is described in a project XML file. This
is the main project file in the project's root folder with the name ``nwProject.nwx``. This file
also contains all the meta data required for the project, and a number of related project settings.

If this file is lost or corrupted, the structure of the project is lost. It is important to keep
this file backed up, either through the built-in backup tool, or your own backup solution.

.. tip::
   The novelWriter project folder is structured so that it can easily be added to a version control
   system like git. If so, you may want to add a `.gitignore` file to exclude files with the
   extensions `.json` as JSON files are used to cache the index and various run-time settings and
   are generally large files that change often. You'd also want to exclude the ``cache`` folder.

The project XML file is indent-formatted, suitable for diff tools and version control since most of
the file will stay static, although a timesetamp is set in the meta section on line 2 each time the
file is saved.


Project Documents
-----------------

The project documents are saved in a folder in the main project folder named ``content``. Each
document has a file handle taken from the first 13 characters of a SHA256 hash of the system time
when the file was first created. The documents are saved with a filename assembled from this hash
and the file extension ``.nwd``.

If you wish to find the physical location of a file in the project, you can either look it up in the
project XML file, select :guilabel:`Show File Details` from the :guilabel:`Document` menu when
having the document open, or look in the ``ToC.txt`` file in the root of the project folder.
The ``ToC.txt`` file has a list of all document files in the project and where they are saved.

The reason for this cryptic file naming is to avoid issues with file naming conventions and
restrictions on different operating systems, and also to have a file name that does not depend on
what the user names the files, or changes it to. The file meta data in the tree view, except the
file label, is only saved in the project XML file.

Each document file contains a plain text version of the text from the editor. The file can in
principle be edited in any text editor, and is suitable for diffing and version control if so
desired. Just make sure the file remains in utf-8 encoding, otherwise unicode chatracters may become
mangled when the file is opened in novelWriter again.

The first line of the file contains some meta data starting with the characters ``%%~``. This line
is mainly there to restore some information if it is lost from the project file, and the information
may be helpful if you do open the file in an external editor as it contains the file label as the
last entry. The line can be deleted without any consequences to the rest of the content of the file,
and will be added back the next time the file is saved in novelWriter.


The File Saving Process
-----------------------

When saving the project file, or any of the documents, the data is first saved to a temporary file.
If successful, the old data file is removed, and the temporary file becomes the new file. This
ensures that the previously saved data is only replaced when the new data has been successfully
saved.

For the project XML file, a ``.bak`` file is kept which will always contain the previous version of
the file, although when auto-save is enabled, they may have the same content. If the opening of a
project file fails, novelWriter will automatically try to open the ``.bak`` file instead.
