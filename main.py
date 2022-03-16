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
    def __init__(self, target_folder):
        self.items = multiprocessing.Manager().dict()
        self.filelist = []
        self.evaluate_folders(target_folder)
        self.time_hashstart = time.perf_counter()
        print(f"\nStarting Hash of folder:\n{target_folder}\n")
        pool = multiprocessing.Pool(processes=4)
        result = pool.imap_unordered(HashFile, self.filelist)
        for i in result:
            self.items.setdefault(i.hash, [i]).append(i)
            print(len(self.items[i.hash]), i.filename)
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
                self.evaluate_folders(target_file)


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
    hash_target = Path.home() / 'Desktop' / "The Ark Challenge"
    testMerge = MainProcess(hash_target)
    time_mainstop = time.perf_counter()
    maintime = time_mainstop - time_mainstart
    [print(x, type(y), len(y)) for x, y in testMerge.items.items()]
    print(len(testMerge.items))
    print(f"Hash Time: {testMerge.hashtime}")
    print(f"Main Time: {maintime}")

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
