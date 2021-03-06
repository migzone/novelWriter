.. _a_export:

******************
Exporting Projects
******************

The novelWriter project can be exported in various formats using the build tool available from
:guilabel:`Build Novel Project` in the :guilabel:`Tools` menu, or by pressing :kbd:`F5`.


.. _a_export_headers:

Header Formatting
=================

The titles for the five types of titles (the chapter headings come in a numbered and unnumbered
version) of story structure can be formatted collectively in the export tool. This is done through
a series of keyword–replace steps. They are all on the format ``%keyword%``.

``%title%``
   This keyword will always be replaced with the title text you put after the ``#`` characters in
   your document.

``%ch%``
   This is replaced by a chapter number. The number is incremented by one each time the build tool
   sees a new heading of level two in a file with layout :guilabel:`Chapter`. If the file has layout
   :guilabel:`Unnumbered`, the counter is *not* incremented. The latter is useful for for instance
   Prologue and Epilogue chapters.

``%chw%``
   This is like ``%ch%``, but the number is expressed as a word like for instance "One", "Two", etc.

``%chi%``
   This is also like ``%ch%``, but the number is represented as a lower case Roman number.

``%chI%``
   This is also like ``%ch%``, but the number is represented as an upper case Roman number.

``%sc%``
   This is the number counter equivalent for scenes. These are incremented each time a heading of
   level three is encountered, but reset to 1 each time a chapter is encountered. They can thus be
   used for counting scenes within a chapter.

``%sca%``
   This is like ``%sc%``, but the number is *not* reset to 1 for each chapter. Instead it runs from
   1 from the beginning of the novel.

``\\``
   This inserts a line break within the title.

.. note::
   Header formatting only applies to novel files. Headings in note files will will be left as-is on
   export. However, heading levels 1 through 4 are converted to the correct heading level in the
   respective output formats.

**Example**

* The format ``%title%`` just reproduces the title you set in the document file.
* The format ``Chapter %ch%: %title%`` produces something like "Chapter 1: My Chapter Title".
* The format ``Scene %ch%.%sc%`` produces something like "Scene 1.2" for scene 2 in chapter 1.


.. _a_export_scenes:

Scene Separators
================

If you don't want any titles for your scenes (and for your sections if you have them), you can leave
the boxes empty, and an empty paragraph will be inserted between the scenes or sections instead.

Alternatively, if you want a separator between them, like the common ``* * *``, you can also enter
that in the box. In fact, if the format is a piece of static text, it will always be treated as a
separator.


.. _a_export_files:

File Selection
==============

Which files are selected for export can also be controlled from the options on the left side of the
dialog window. The switch for :guilabel:`Include novel files` will select any file that isn't
classified as a note. The switch for :guilabel:`Include note files` will select any file that *is*
a note. This is allows for exporting just the novel, just your notes, or both, as you see fit.

In addition, you can select to export the synopsis comments, regular comments, keywords, and even
exclude the body text itself.

.. tip::
   If you for instance want to export a document with an outline of the novel, you can enable
   keywords and synopsis export and disable body text, thus getting a document with each heading
   followed by the tags and references and the synopsis.

If you need to exclude specific files from your exports, like draft files or files you want to take
out of your manuscript, but don't want to delete, you can un-check the :guilabel:`Include when
building project` option for each file in the project tree. An included file has a checkmark after
the status icon in the :guilabel:`Flags` column. The :guilabel:`Build Novel Project` tool has a
switch to ignore this flag if you need to collectively override these settings.


.. _a_export_formats:

Export Formats
==============

Currently, six formats are supported for exporting.

OpenDocument Format
   This produces an open document ``.odt`` file. The document produced has very little formatting,
   and may require further editing afterwards. For a better formatted office document, you may get a
   better result with exporting to HTML and then import that HTML document into your office word
   processor. They are generally very good at importing HTML files.

PDF Format
   The PDF export is just a shortcut for print to file. For a better PDF result, you may instead
   want to export HTML, and use a word processor to convert the HTML document to PDF.

novelWriter HTML
   The HTML export format writes a single ``.htm`` file with minimal style formatting. The exported
   HTML file is suitable for further processing by document conversion tools like Pandoc, for
   importing in word processors, or for printing from browser. It is generally the best formatted
   export option and supports all features of novelWriter since it is entirely geenrated by the
   application and doesn't depend on Qt library features.

novelWriter Markdown
   This is simply a concatenation of the files selected by the filters. The files in the project are
   stacked together in the order they appear in the tree view, with comments, tags, etc. included if
   they are selected. This is a useful format for exporting the project for later import back into
   novelWriter.

Standard Markdown
   If you have Qt 5.14 or higher, the option to export to plain markdown is available. This feature
   uses Qt's own markdown export feature.

Plain Text
   The plain text export format writes a simple ``.txt`` file without any formatting at all.


.. _a_export_options:

Additional Export Options
=========================

In addition to the above document formats, the novelWriter HTML and Markdown formats can also be
wrapped in a JSON file. The files will have a meta data entry and a body entry. For HTML, also the
accompanying css styles are exported.

The text body is saved in a two-level list. The outer list contains one entry per exported file, in
the order they appear in the project tree. Each file is then split up into a list as well, with one
entry per paragraph in the document.

These files are mainly intended for scripted post-processing for those who want that option. A JSON
file can be imported directly into a Python dict object or a PHP array, to mentions a few options.
