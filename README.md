[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)  
# mkp5
Generate a blank p5.js project containing an HTML page that imports p5.js and p5.sound from cdnjs, an empty javascript sketch, and an empty css stylesheet.

# Usage
Run 'python main.py project_name' to create a blank project named project_name

# Command line arguments:
|Argument|Explanation|
|---|---|
|--directory_name DIR_NAME, -d DIR_NAME  |Name of directory to create project in, if not specified default to project name |
|--author AUTHOR_NAME, -a AUTHOR_NAME  |Author name to be used in headers |
|--debug             |Show debug info during process |
|--no_headers        |Don't use headers in any files |
|--sparse_headers    |Only use project name in headers| 

# Author
Written by Tyler Weston, 2021