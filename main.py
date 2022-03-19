import hashlib
import os
from pathlib import Path
from os.path import basename, splitext
import multiprocessing
import time


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
    def __init__(self, target_folder, merge_heads=None):
        if merge_heads is None:
            self.merge_enabled = False
        self.manager = multiprocessing.Manager()
        self.items = self.manager.dict()
        self.filelist = []
        self.dirlist = []
        self.evaluate_folders(target_folder)
        self.merge_heads = merge_heads
        # Merging is disabled if list is empty
        self.time_hashstart = time.perf_counter()
        print(f"\nStarting Hash of folder:\n{target_folder}\n")
        pool = multiprocessing.Pool(processes=4)
        result = pool.imap_unordered(HashFile, self.filelist)
        for i in result:
            self.items.setdefault(i.hash, self.manager.list()).append(i)
        pool.close()
        pool.join()
        self.time_hashstop = time.perf_counter()
        self.hashtime = self.time_hashstop - self.time_hashstart

    def evaluate_folders(self, target_folder):
        print(target_folder)
        folder_contents = os.listdir(target_folder)
        for file in folder_contents:
            target_file = target_folder / file
            if os.path.isfile(target_file):
                self.filelist.append(target_file)
            if os.path.isdir(target_file):
                self.dirlist.append(FolderProfile(target_folder))
                self.evaluate_folders(target_file)


class FolderProfile:
    def __init__(self, dirpath):
        self.dirname = ""
        self.dirpath = dirpath
        self.eskimo_folders = [] # folder + list of shared files (can share more than one file)
        # Update in script that reviews hash results. append parent dir that share child files.
        # Mid hashing shared child updates are feasible in the following scenario:
        # If Hash is added to MainProcess.items,
        # FolderProfile of new HashFile Dir receies copy of last Hash items eskimo folder
        #   (self.items[HashObj.hash].parentdir].eskimo_folders)
        #   Occurs before Hashfile is added to .items
        # Other HashFile's FolderProfiles eskimo Lists are appended with parent dir of new HashFile
        #   for x in MainProcess.items[HashObj]:
        #       x.


class HashFile:
    def __init__(self, file_path_obj):
        self.file_path = file_path_obj
        self.filename, self.filetype = splitext(basename(file_path_obj))
        self.filesize = os.path.getsize(self.file_path)
        self.parent_dir = file_path_obj.parent
        self.hash = self.hash_file()

    def hash_file(self):
        file_hash = hashlib.sha256()
        block_size = self.eval_blocksize()
        with open(self.file_path, 'rb') as f:
            while True:
                chunk = f.read(block_size)
                if not chunk:
                    break
                file_hash.update(chunk)
        return file_hash.hexdigest()

    def eval_blocksize(self, max_block=1073741824):
        if self.filesize > max_block:
            return max_block
        return 536870912


if __name__ == '__main__':
    time_mainstart = time.perf_counter()
    hash_target = Path.home() / 'Desktop' / "HashMergerTest"
    merge_focus = ["j"]
    testMerge = MainProcess(hash_target, merge_heads=merge_focus)
    time_mainstop = time.perf_counter()
    maintime = time_mainstop - time_mainstart
    new_dict = {}
    for x, y in testMerge.items.items():
        new_dict[x] = list(y)
    for x, y in new_dict.items():
        for file in y:
            print(x, file.parent_dir)
    print(len(testMerge.items))
    print(f"Hash Time: {testMerge.hashtime}")
    print(f"Main Time: {maintime}")

# Mutable sub object within dictionary not updates
# Fix by making each unique hash an instance of hash class with a mangager list.

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
