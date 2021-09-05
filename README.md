[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)  
# mkp5
Generate a blank p5.js project containing an HTML page that imports p5.js and p5.sound from cdnjs, an empty javascript sketch, and an empty css stylesheet.

# Usage
Recommended:  
Windows: clone the project and then add the directory you cloned into into your PATH. Now, from any directory, run:  
```console
C:\folder\mkp5 project_name
``` 
to create a blank project named project_name under the current working directory. For example, running:  
```console
C:\folder\mkp5 first_proj
```
will create `C:\folder\first_proj` with the neccessary files to start your p5.js project

# Command line arguments:
|Argument|Explanation|
|---|---|
|--directory_name DIR_NAME<br />-d DIR_NAME  |Name of directory to create project in, if not specified default to project name |
|--author AUTHOR_NAME<br />-a AUTHOR_NAME  |Author name to be used in headers |
|--debug             |Show debug info during process |
|--no_headers        |Don't use headers in any files |
|--sparse_headers    |Only use project name in headers| 

Example:
Running  
```console
C:\folder\mkp5 first_proj --author "Tyler Weston" -d proj_dir
```
will create a project named first_proj in `C:\folder\proj_dir`  

# Issues
This is still a very early work so will be changing and being fixed in the near future. If you find any issues, feel free to open them in the issue board here or submit a PR.

# Author
Written by Tyler Weston, 2021