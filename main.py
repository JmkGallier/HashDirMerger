import hashlib
from pathlib import Path
from os.path import basename, splitext
import subprocess


"""
Full Featureset:
Detect duplicates
Detect variant folders to be merged
    If a folder has enough duplicate hashes, it may be a variant
    If a folder has enough duplicate named sub folders
Merge variant folders
"""


class FileHashTree:
    cumulative_files = {}
    simple_folders = {}
    folder_flagger = {}

    def __init__(self):
        pass


class FileHashTable:
    def __init__(self, file_path_obj, recursive=False):
        try:
            self.items = {}
            self.sub_dir = []
            p = file_path_obj.glob('**/*')
            for item in p:
                if item.is_file():
                    hash_obj = HashFile(item)
                    if hash_obj in FileHashTree.cumulative_files:
                        FileHashTree.cumulative_files[hash_obj.hash].append(hash_obj.file_path)
                        FileHashTree.folder_flagger.setdefault(hash_obj.file_path, 0)
                        FileHashTree.folder_flagger[hash_obj] += 1
                    else:
                        FileHashTree.cumulative_files.setdefault(hash_obj.hash, []).append(hash_obj)
                elif item.is_dir():
                    FileHashTable(item)
                else:
                    print(f"[ INFO ] Unexpected file found: {item}")
            # files = [x for x in p if x.is_file()]
            # [print(j) for j in files]
            # for each dir
            # {filepath: {'examplehash123': hashfile_obj, .....}}
            # for each file,
        except IsADirectoryError:
            print(f"{file_path_obj} is a File.")

    def dir_hash(self):
        pass


class HashFile:
    def __init__(self, file_path_obj):
        self.file_path = file_path_obj
        self.filename = splitext(basename('/path/file.suffix'))[0]
        self.hash = self.hash_file()
        self.parent_dir = file_path_obj.parent

    def hash_file(self, block_size=4096):
        file_hash = hashlib.sha256()
        with open(self.file_path, 'rb') as f:
            fb = f.read(block_size)
            while len(fb) > 0:
                file_hash.update(fb)
                fb = f.read(block_size)
        return file_hash.hexdigest()


hash_target = Path.home() / 'Desktop' / "testdir"
FileHashTable(hash_target)

[print(x, [y.file_path for y in contents]) for x, contents in FileHashTree.cumulative_files.items()]
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


