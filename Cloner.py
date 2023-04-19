import os
import json
import sys


def copy_file_win(src: str, dest: str):
    '''Copy a file from one location to another'''
    os.system(f'robocopy /q /y /h "{src}" "{dest}"')

def copy_dir_win(src: str, dest: str):
    '''Copy a directory from one location to another'''
    os.system(f'robocopy /q /s /y /i /h /e "{src}" "{dest}"')

def copy_file_other(src: str, dest: str):
    '''Copy a file from one location to another'''
    os.system(f'cp "{src}" "{dest}"')

def copy_dir_other(src: str, dest: str):
    '''Copy a directory from one location to another'''
    os.system(f'cp -R "{src}" "{dest}"')

def rm_dir_win(path: str):
    '''Delete a directory'''
    os.system(f'rmdir /s /q "{path}"')

def rm_file_win(path: str):
    '''Delete a file'''
    os.system(f'del /f /q "{path}"')

def rm_dir_other(path: str):
    '''Delete a file/directory'''
    os.system(f'rm -rf "{path}"')

def mv_dir_win(src: str, dest: str):
    '''Move a directory from one location to another'''
    os.system(f'move /y "{src}" "{dest}"')

def mv_dir_other(src: str, dest: str):
    '''Move a directory from one location to another'''
    os.system(f'mv "{src}" "{dest}"')

def mkdir_win(path: str):
    '''Create a directory'''
    os.system(f'mkdir "{path}"')

def mkdir_other(path: str):
    '''Create a directory'''
    os.system(f'mkdir -p "{path}"')

if sys.platform == "win32":
    copy_file = copy_file_win
    copy_dir = copy_dir_win
    rm_dir = rm_dir_win
    rm_file = rm_file_win
    mv_dir = mv_dir_win
    mkdir = mkdir_win
else:
    copy_file = copy_file_other
    copy_dir = copy_dir_other
    rm_dir = rm_dir_other
    rm_file = rm_dir_other
    mv_dir = mv_dir_other
    mkdir = mkdir_other

    

def get_dir_name(path: str):
    '''Get the name of a directory from a path'''
    # Split the path into a list
    path_list = path.split("/")
    # Loop through the list
    for i in range(len(path_list) - 1, -1, -1):
        # Check if the item is not empty
        if path_list[i] != "":
            # Return the item
            return path_list[i]

def subtract_base_dir(path: str, base_dir: str):
    '''Subtract the base directory from a path'''
    # Get the name of the base directory
    base_dir_name = get_dir_name(base_dir)
    # Split the path into a list
    path_list = path.split("/")
    # Loop through the list
    for i in range(len(path_list) - 1, -1, -1):
        # Check if the item is the base directory name
        if path_list[i] == base_dir_name:
            # Return the path after the base directory
            return "/".join(path_list[i + 1:]), len(path_list) - i - 1
    # Base directory not found
    return path, 0
            

def __clone_dir(src:str , dest: str, trunc_src=None) -> int:
    '''Copy a directory from one location to another (assumes absolute paths)'''
    # Check if the destination directory exists
    if not os.path.exists(dest):
        # Check if the source directory is a nested directory
        if trunc_src is not None:
            dest_parent = dest[:dest.rfind("/")]
            mkdir(dest_parent)
        # Copy the directory
        copy_dir(src, dest)
        #os.system(f"cp -R {src} {dest}")
        count = len(os.listdir(src))
        print(f"Cloned {src} (new)")
        return count

    # Get contents of the source directory
    src_contents = os.scandir(src)
    src_cont_names = [item.name for item in src_contents]
    dest_contents = os.scandir(dest)
    dest_cont_names = [item.name for item in dest_contents]
    count = 0
    src_contents = os.scandir(src)
    # Loop through the contents
    for item in src_contents:
        # Check if the item exists in the destination directory
        try:
            dest_i = dest_cont_names.index(item.name)
        except ValueError:
            dest_i = None
        if dest_i is not None:
            src_mtime = os.path.getmtime(f"{src}/{item.name}")
            dest_mtime = os.path.getmtime(f"{dest}/{item.name}")
            # Check if the source item is more recently modified than the destination item
            if src_mtime > dest_mtime:
                if item.is_file():
                    copy_file(f"{src}/{item.name}", f"{dest}/{item.name}")
                    #os.system(f"cp {src}/{item.name} {dest}/{item.name}")
                    count += 1
                    print(f"Cloned {src}/{item.name} (overwrite)")
                elif item.is_dir():
                    # Clone the sub-directory
                    count += __clone_dir(f"{src}/{item.name}", f"{dest}/{item.name}")
                    print(f"Cloned {src}/{item.name} (overwrite)")
        # Item does not exist in the destination directory
        else:
            if item.is_file():
                copy_file(f"{src}/{item.name}", f"{dest}/{item.name}")
                #os.system(f"cp {src}/{item.name} {dest}/{item.name}")
            elif item.is_dir():
                copy_dir(f"{src}/{item.name}", f"{dest}/{item.name}")
                #os.system(f"cp -R {src}/{item.name} {dest}/{item.name}")
            count += 1
            print(f"Cloned {src}/{item.name} (new)")
    dest_contents = os.scandir(dest)
    # Delete files in the destination directory that are not in the source directory
    for item in dest_contents:
        if item.name not in src_cont_names:
            if item.is_file():
                rm_file(f"{dest}/{item.name}")
                #os.system(f"rm {dest}/{item.name}")
            elif item.is_dir():
                rm_dir(f"{dest}/{item.name}")
                #os.system(f"rm -rf {dest}/{item.name}")
            count += 1
            print(f"Deleted {dest}/{item.name}")
    return count

def rebase_dir(parent: str, prev_parent: str, base_dest: str):
    '''Rebase a directory to a new base directory'''
    parent_name = get_dir_name(parent)
    prev_name = get_dir_name(prev_parent)
    # Determine if the previous parent directory is a sub-directory of the new parent directory
    if parent in prev_parent:
        # Determine the truncated source directory
        trunc_src, n = subtract_base_dir(prev_parent, parent)
        # Create the new sub-directory
        dest_parent = trunc_src[:trunc_src.rfind("/")]
        mkdir(f"{base_dest}/{parent_name}/{dest_parent}")
        # Move the sub-directory to the new destination directory
        mv_dir(f"{base_dest}/{prev_name}", f"{base_dest}/{parent_name}/{trunc_src}")
        #os.system(f"mv {base_dest}/{prev_name} {dest_base}/{prev_name}")
    elif prev_parent in parent:
        # New parent directory is a sub-directory of the previous parent directory
        # Determine the truncated source directory
        trunc_src, n = subtract_base_dir(parent, prev_parent)
        # Move the sub-directory to the new destination directory
        mv_dir(f"{base_dest}/{prev_name}/{trunc_src}", f"{base_dest}/{parent_name}")
        #os.system(f"mv {base_dest}/{prev_name}/{trunc_src} {base_dest}/{parent_name}")
        # Remove the old sub-directory
        rm_dir(f"{base_dest}/{prev_name}")
        #os.system(f"rm -rf {base_dest}/{prev_name}")

def clone_dirs(src_dirs: list[str], base_dest: str):
    '''Clone a list of directories to a single destination directory.
    The destination directory must already exist.
    A common base directory will be determined for the given source directories.
    '''
    try:
        f_base_dest = os.path.abspath(base_dest)
        # Ensure the destination directory exists
        if not os.path.exists(f_base_dest):
            raise Exception(f"Destination directory '{f_base_dest}' does not exist")
        f_srcs = [os.path.abspath(src) for src in src_dirs]
        # Ensure all source directories exist
        for src in f_srcs:
            if not os.path.exists(src):
                raise Exception(f"Source directory '{src}' does not exist")
        # Get the common parent directory of the source directories
        src_parent = os.path.commonpath(f_srcs)
        # Ensure the metadata file exists
        meta_file = None
        if not os.path.exists(f"{f_base_dest}/.cloneinfo"):
            meta_file = open(f"{f_base_dest}/.cloneinfo", "w")
            # Get the common prefix and write it to the file
            json.dump({"CLONE_BASE_DIR": ""}, meta_file)
            meta_file.close()
        # Open the metadata file
        meta_file = open(f"{f_base_dest}/.cloneinfo", "r")
        metadata = json.load(meta_file)
        meta_file.close()
        # Keep count of edits
        count = 0
        # Ensure the base directory is correct
        if src_parent != metadata["CLONE_BASE_DIR"]:
            # Move all previously cloned files to the new base directory
            rebase_dir(src_parent, metadata["CLONE_BASE_DIR"], f_base_dest)
            # Replace the base directory in the metadata file
            metadata["CLONE_BASE_DIR"] = src_parent
            meta_file = open(f"{f_base_dest}/.cloneinfo", "w")
            json.dump(metadata, meta_file)
            meta_file.close()
            count += 1

        base_dir_name = get_dir_name(src_parent)
        if not os.path.exists(f"{f_base_dest}/{base_dir_name}"):
            mkdir(f"{f_base_dest}/{base_dir_name}")
            #os.system(f"mkdir {f_base_dest}/{base_dir_name}")
        # Loop through the source directories
        for src in f_srcs:
            # Get the name of the source directory
            trunc_src, n = subtract_base_dir(src, src_parent)
            # Clone the directory
            count += __clone_dir(src, f"{f_base_dest}/{base_dir_name}/{trunc_src}", trunc_src if n > 1 else None)
        print(f"Edited {count} files.")
    except Exception as e:
        print(e)

'''if __name__ == "__main__":
    # Copy the files
    clone_dirs(["/Users/ericblois/Development/Python/FantasyTools", "/Users/ericblois/Downloads"], "./cloned_dir")

# "/Users/ericblois/Downloads"
# "dir1", "dir2", "./dir3/dir4"
'''