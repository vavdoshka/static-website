import os
import shutil
from generator import generate_pages_recursive

BASE_DIRECTORY = os.path.dirname(__file__)
STATIC_ASSETS = os.path.join(BASE_DIRECTORY, "..", "static")
PUBLIC_ASSETS = os.path.join(BASE_DIRECTORY, "..", "public")

def recursive_copy(filename, parent=""):
    src = os.path.join(STATIC_ASSETS, parent, filename)
    dest = os.path.join(PUBLIC_ASSETS, parent, filename)
    if os.path.isfile(src):
        print(f"Copy '{src}' to '{dest}'")
        shutil.copy(src, dest)
    elif os.path.isdir(src):
        print(f"Creating directory at {dest}")
        os.mkdir(dest)
        ls = os.listdir(os.path.join(STATIC_ASSETS, parent, filename))
        for fn in ls:
            recursive_copy(fn, parent=os.path.join(parent, filename))



def copy_from_static_to_public():

    shutil.rmtree(PUBLIC_ASSETS, ignore_errors=True)
    os.mkdir(PUBLIC_ASSETS)

    for filename in os.listdir(STATIC_ASSETS):
        recursive_copy(filename)

def main():
    copy_from_static_to_public()

    generate_pages_recursive(os.path.join(BASE_DIRECTORY, "..", "content"), os.path.join(BASE_DIRECTORY, "..", "template.html"), os.path.join(PUBLIC_ASSETS))

main()