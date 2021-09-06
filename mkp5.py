import os
import argparse
import shutil
from datetime import datetime

class project_info_class:
    # Information about the project that is passed around and used by various functions
    project_name = None
    copy_to_dir = None
    args = None

    libs_location_from = None
    p5_lib_name = None
    p5_sound_name = None
    p5_lib_ver = '1.4.0'
    p5_libs_base_path = None

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
    parser.add_argument('--no_sound', action='store_true', help="Don't include sound library")
    parser.add_argument('--use_cdn', action='store_true', help="Use CDN source instead of local copy of p5 library")
    parser.add_argument('--no_min', action='store_true', help="Don't use minified p5 libraries")
    parser.add_argument('--use_ver', type=str, help="Specify version number to use through CDN. Defaults to newest version")
    return parser.parse_args()

def main():
    # Main driver for mk5
    args = parse_args()
    project_info = project_info_class()
    project_info.args = args
    project_info.project_name = args.project_name
    print("mkp5 -----")
    if project_info.args.use_ver:
        project_info.p5_lib_ver = project_info.args.use_ver

    create_file_targets(project_info)

    print(f"Making project {project_info.project_name} in \{project_info.copy_to_dir}")
    try:
        os.mkdir(project_info.copy_to_dir)
    except FileExistsError as e:
        print(f"Error: Directory {project_info.project_name} already exists, specify an empty directory")
        exit(1)

    make_headers(project_info)

    try:
        make_html(project_info)
        make_css(project_info)
        make_js(project_info)
        if not project_info.args.use_cdn:
            copy_libs(project_info)
    except:
        cleanup(project_info)
        print("Error creating project")
        exit(1)
    finally:
        print("Success!")
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

    if not project_info.args.use_cdn:
        project_info.libs_location_from = os.path.join(script_path, "assets", "libraries")
        project_info.libs_location_to = os.path.join(project_info.copy_to_dir, "libraries")

    if project_info.args.no_min:
        project_info.p5_lib_name = 'p5.js'
        project_info.p5_sound_name = 'p5.sound.js'
    else:
        project_info.p5_lib_name = 'p5.min.js'
        project_info.p5_sound_name = 'p5.sound.min.js'

    if project_info.args.use_cdn:
        project_info.p5_libs_base_path = f'https://cdnjs.cloudflare.com/ajax/libs/p5.js/{project_info.p5_lib_ver}/'
    else:
        project_info.p5_libs_base_path = 'libraries/'


    if project_info.args.debug:
        print(f"Current working directory: {cwd}")
        print(f"Script path: {script_path}")
        print(f"Assets path: {copy_from_dir}")
        print("Files to copy:")
        print(f"{project_info.html_from} ==> {project_info.html_to}")
        print(f"{project_info.css_from} ==> {project_info.css_to}")
        print(f"{project_info.js_from} ==> {project_info.js_to}")
        print(f"p5 library name: {project_info.p5_lib_name}")
        print(f"p5 sound lib name: {project_info.p5_sound_name}")
        print(f"libraries: {project_info.p5_libs_base_path}")
        if not project_info.args.use_cdn:
            print(f"{project_info.libs_location_from} ==> {project_info.libs_location_to}")


def copy_libs(project_info):
    try:
        os.mkdir(project_info.libs_location_to)
    except OSError as e:
        print(str(e))
        raise
    p5_lib_file_from = os.path.join(project_info.libs_location_from, project_info.p5_lib_name)
    p5_lib_file_to = os.path.join(project_info.libs_location_to, project_info.p5_lib_name)
    try:
        shutil.copyfile(p5_lib_file_from, p5_lib_file_to)
    except IOError as e:
        print(str(e))
        raise

    if project_info.args.no_sound:
        return

    p5_sound_file_from = os.path.join(project_info.libs_location_from, project_info.p5_sound_name)
    p5_sound_file_to = os.path.join(project_info.libs_location_to, project_info.p5_sound_name)
    try:
        shutil.copyfile(p5_sound_file_from, p5_sound_file_to)
    except IOError as e:
        print(str(e))
        raise


def make_html(project_info):
    generated_html_string = make_html_string(project_info)
    with open(project_info.html_to, 'w') as html_file:
        html_file.write(generated_html_string)


def make_html_string(project_info):
    p5_libs_string = f'<script src="{project_info.p5_libs_base_path}{project_info.p5_lib_name}"></script>'
    if not project_info.args.no_sound:
        p5_libs_string += f'\n\t<script src="{project_info.p5_libs_base_path}{project_info.p5_sound_name}"></script>'
    # TODO: Nicer way to do this!
    html_string =   f"""<!-- {project_info.project_header} -->
<html>
<head>
    {p5_libs_string}
    <link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>
    <script src="sketch.js"></script>
</body>
</html>
""" 
    return html_string

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
    os.rmdir(project_info.copy_to_dir)


if __name__ == "__main__":
    main()