import os
import argparse
import shutil
from datetime import datetime

class project_info_class:
    # Information about the project that is passed around and used by various functions
    project_name = None
    copy_to_dir = None
    args = None

    project_header = None

    html_from = None
    css_from = None
    js_from = None

    html_to = None
    css_to = None
    js_to = None


def parse_args():
    # Parse command line argugments
    parser = argparse.ArgumentParser(description="A p5.js blank project creator", epilog="Tyler Weston, 2021")
    parser.add_argument('project_name', type=str, help="Name of the project to create")
    parser.add_argument('--directory_name', '-d', type=str, help="Name of directory to create project in, if not specified default to project name")
    parser.add_argument('--author', '-a', type=str, help="Author name to be used in headers")
    parser.add_argument('--debug', action='store_true', help="Show debug info during process")
    parser.add_argument('--no_headers', action='store_true', help="Don't use headers in any files")
    parser.add_argument('--sparse_headers', action='store_true', help="Only use project name in headers")
    return parser.parse_args()

def main():
    # Main driver for mk5
    args = parse_args()
    project_info = project_info_class()
    project_info.args = args
    project_info.project_name = args.project_name
    print("mkp5 -----")
    create_file_targets(project_info)

    print(f"Making project {project_info.project_name} in \{project_info.copy_to_dir}")
    try:
        os.mkdir(project_info.copy_to_dir)
    except FileExistsError as e:
        print(f"Error: Directory {project_info.project_name} already exists")
        exit(1)

    make_headers(project_info)

    try:
        make_html(project_info)
        make_css(project_info)
        make_js(project_info)
    except:
        cleanup()
    finally:
        print("Done")
    # Print some status messages here
    exit(0)

def make_headers(project_info):
    project_info.project_header = project_info.project_name
    if project_info.args.sparse_headers:
        return
    project_info.project_header = "\n" + project_info.project_header + "\n"
    if project_info.args.author is not None:
        project_info.project_header += f"Author: {project_info.args.author}\n"
    now = datetime.now()
    now_string = now.strftime("%d/%m/%Y %H:%M:%S")
    project_info.project_header += f"Created by mkp5 on {now_string}\n" 

def create_file_targets(project_info):
    cwd = os.getcwd()

    dir_name = project_info.args.directory_name \
                if project_info.args.directory_name is not None \
                else project_info.project_name

    project_info.copy_to_dir = os.path.join(cwd, dir_name)

    script_path = os.path.dirname(os.path.realpath(__file__))
    copy_from_dir = os.path.join(script_path, "assets")

    project_info.html_from = os.path.join(copy_from_dir, "index.html")
    project_info.css_from = os.path.join(copy_from_dir, "style.css")
    project_info.js_from = os.path.join(copy_from_dir, "sketch.js")

    project_info.html_to = os.path.join(project_info.copy_to_dir, "index.html")
    project_info.css_to = os.path.join(project_info.copy_to_dir, "style.css")
    project_info.js_to = os.path.join(project_info.copy_to_dir, "sketch.js") 

    if project_info.args.debug:
        print(f"Current working directory: {cwd}")
        print(f"Script path: {script_path}")
        print(f"Assets path: {copy_from_dir}")
        print("Files to copy:")
        print(f"{project_info.html_from} ==> {project_info.html_to}")
        print(f"{project_info.css_from} ==> {project_info.css_to}")
        print(f"{project_info.js_from} ==> {project_info.js_to}")



def make_html(project_info):
    try:
        shutil.copyfile(project_info.html_from, project_info.html_to)
        if not project_info.args.no_headers:
            with open(project_info.html_to, 'r') as original: 
                data = original.read()
            with open(project_info.html_to, 'w') as modified: 
                modified.write(f"<!-- {project_info.project_header} -->\n" + data)
    except IOError as e:
        print(str(e))
        raise

def make_css(project_info):
    try:
        shutil.copyfile(project_info.css_from, project_info.css_to)
        if not project_info.args.no_headers:
            with open(project_info.css_to, 'r') as original: 
                data = original.read()
            with open(project_info.css_to, 'w') as modified: 
                modified.write(f"/* {project_info.project_header} */\n" + data)
    except IOError as e:
        print(str(e))
        raise

def make_js(project_info):
    # copy with /* project name */ at the top
    try:
        shutil.copyfile(project_info.js_from, project_info.js_to)
        if not project_info.args.no_headers:
            with open(project_info.js_to, 'r') as original: 
                data = original.read()
            with open(project_info.js_to, 'w') as modified: 
                modified.write(f"/* {project_info.project_header} */\n" + data)
    except IOError as e:
        print(str(e))
        raise

def cleanup(project_info):
    # in case of a failure during creation of a project, remove whatever bits 
    # are already there and delete the folder since we don't want a malformed
    # project kicking around our drive
    print("Cleaning up")
    if os.path.exists(project_info.html_to):
        os.remove(project_info.html_to)
    if os.path.exists(project_info.css_to):
        os.remove(project_info.css_to)
    if os.path.exists(project_info.js_to):
        os.remove(project_info.js_to)
    os.rmdir(project_info.dir_name)


if __name__ == "__main__":
    main()