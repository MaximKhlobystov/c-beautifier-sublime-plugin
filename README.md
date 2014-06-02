About
=====

Sublime Text 2 plugin to format your C/C++ code according to your own code conventions.

Installation
============

-   Clone or download the source code here
-   Go to:
    -   ~/.config/sublime-text-2/packages (Linux)
	-   %APPDATA%\Sublime Text 2\Packages (Windows)
	-   ~/Library/Application\ Support/Sublime\ Text\ 2/Packages
	and move the package there
-   Enjoy!

Settings
========

There's a file called Convention.sublime-settings. It defines your favourite code conventions.

-   "indent_size" is the size of indentation you prefer (in spaces). You can make it whatever you want.
-   "space_in_arguments_definition" can be "no" or "one". It declares what format you like inside the brackets while defining arguments: with spaces in the beginning and the end, or without.
-   "line_length" is the maximum length of line you think is appropriate. You can make it whatever number of characters you like.
-   "space_in_condition" defines if you like to put a space after if/while/switch or not ("one"/"no").
-   "block_statement" can be either "one", "no", or "newline". It depend on the style you prefer in writing the beginning of a block statement: no space between closing bracket and opening curly bracket, one space, or you like to put a curly bracket on the next line.

Usage
=====

-   To show the quick panel, press Ctrl+Alt+4.
-   The first line is to clear all the previously made highlights.
-   The second one aligns the code according to the "indent_size" setting (if the set of curly brackets is not correct, it stops at the break and highlight it).
-   Other lines are the warnings found in your code according to your settings. Navigate to the warning and press enter: you see the exact place and it is highlighted for you.

License
=======

The MIT License (MIT)

Copyright (c) 2014 Maxim Khlobystov

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.