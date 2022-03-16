import hashlib
import os
from pathlib import Path
from os.path import basename, splitext
# import subprocess


"""
Full Feature set:
Detect duplicates
Detect variant folders to be merged
    If a folder has enough duplicate hashes, it may be a variant
    If a folder has enough duplicate named sub folders
Merge variant folders
Point system that considers: Parent_Dir, file match hits, hit/total files, sub_dir hits, sub_dir hit/total subdirs
"""


class MainProcess:
    def __init__(self, target_folder):
        self.items = {}
        self.process_folder(target_folder)

    def process_folder(self, target_folder):
        print(target_folder)
        folder_contents = os.listdir(target_folder)
        folder_files = []
        folder_dirs = []
        for file in folder_contents:
            target_file = target_folder / file
            if os.path.isfile(target_file):
                folder_files.append(target_file)
            if os.path.isdir(target_file):
                folder_dirs.append(target_file)
        for sub_dir in folder_dirs:
            self.process_folder(sub_dir)
        for file in folder_files:
            if len(self.items) % 1000 == 0:
                print(f"[ INFO ] {len(self.items)} Hashing {file}")
            hash_obj = HashFile(file)
            self.items.setdefault(hash_obj.hash, []).append(hash_obj)


class HashFile:
    def __init__(self, file_path_obj):
        self.file_path = file_path_obj
        self.filename, self.filetype = splitext(basename(file_path_obj))
        self.filesize = os.path.getsize(self.file_path)
        self.parent_dir = file_path_obj.parent
        self.hash = self.hash_file()

    def hash_file(self, block_size=4096):
        file_hash = hashlib.sha256()
        with open(self.file_path, 'rb') as f:
            fb = f.read(block_size)
            while len(fb) > 0:
                file_hash.update(fb)
                fb = f.read(block_size)
        return file_hash.hexdigest()


hash_target = Path.home() / 'Desktop' / "The Ark Challenge"
testMerge = MainProcess(hash_target)
[print(x, len(y)) for x, y in testMerge.items.items()]

# Dictionary Update Queue
# Queue of Hash-HashObj tuple pairs

# Path Matching
# os.path.commonprefix
# os.path.commonpath

# Merge all folder structures into a primary branch + duplicates branch
# Create folder branches as separate folders for each unique commonprefix
# Create shadow copy of folder-branch hierarchy by attempting to reassemble the primary/idea folder-branch

# Create class for files hashed
# Attributes: hash, full path, parent folder, grandparent folder, metadate
# print(HashMerger.hash_file(hash_target, 4096))

# # Running commands
# output = subprocess.check_output(['ls', '-l'])
#
# # Path File Manipulation
# test1 = splitext(basename('/path/file.suffix'))[0]  # Filename w/suffix
# test3 = Path('/path/file.suffix').stem  # Filename w/o suffix
# test5 = Path('/path/file/suffix').suffix # Filename  suffix
#
# # Making Directories
# path = Path.home() / 'python-file-paths'
# path.mkdir()
#
# # Making Directories and sub-directories
# path = Path.home() / 'python-file-paths' / 'foo' / 'bar'
# path.mkdir(parents=True, exist_ok=True)
