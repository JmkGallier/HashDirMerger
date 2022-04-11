import hashlib
import os
from pathlib import Path
from os.path import basename, splitext
import multiprocessing
import time
import operator


class MainProcess:
    def __init__(self, target_folder, merge_heads=None):
        if merge_heads is None:
            self.merge_enabled = False
        self.target_folder = target_folder
        self.manager = multiprocessing.Manager()
        self.items = self.manager.dict()
        self.filelist = []
        self.dirlist = []
        self.evaluate_folders(target_folder)
        self.merge_heads = merge_heads
        self.hash_time = None
        self.hash_driver()
        # Merging is disabled if list is empty

    def hash_driver(self):
        """
        Multi-threaded Recursive Directory File Hash driver function.
        Input:  self.file_list
        Output: self.items (updated), self.hash_time (updated)
        """
        time_hashstart = time.perf_counter()
        print(f"\nStarting Hash of folder:\n{self.target_folder}\n")
        pool = multiprocessing.Pool(processes=4)    # ToDo: Dynamically assign process count
        # ToDo: Refactor below: HashFile (HF) to driver function in MainProcess class;
        # "HF" init & nested hash_file func should be unit testable
        result = pool.imap_unordered(HashFile, self.filelist)
        for i in result:
            self.items.setdefault(i.hash, self.manager.list()).append(i)
        pool.close()
        pool.join()
        time_hashstop = time.perf_counter()
        self.hash_time = time_hashstop - time_hashstart

    def evaluate_folders(self, target_folder):
        #   ToDo: Refactor to Unit Testable StaticMethod.
        """

        :param target_folder:
        :return:
        """
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
        self.associate_folder = []


class HashFile:
    def __init__(self, file_path_obj):
        self.file_path = file_path_obj
        self.filename, self.filetype = splitext(basename(file_path_obj))
        self.filesize = os.path.getsize(self.file_path)
        self.rd_blk_sz = self.eval_blocksize(self.filesize)
        self.parent_dir = file_path_obj.parent
        self.hash = self.hash_file(self.file_path, self.rd_blk_sz)

    @staticmethod
    def hash_file(file_path, blk_sz):
        """
        Return sha256sum of file using filename and blocksize to incrementally read in file.
        :param file_path:
        :param blk_sz:
        :return:
        """
        file_hash = hashlib.sha256()
        block_size = blk_sz
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(block_size)
                if not chunk:
                    break
                file_hash.update(chunk)
        return file_hash.hexdigest()

    @staticmethod
    def eval_blocksize(file_size):
        """
        Retunrs read blocksize in bytes; The smaller of 1.5GB or round up file size to nearest 2^n bits).
        :param file_size:
        :return:
        """
        max_block = 1610612736
        bit_len = len(bin(file_size*8))-2
        bin_roundup = int(int(f"1{'0'*bit_len}", 2)/8)
        if bin_roundup > max_block:
            return max_block
        return bin_roundup


def find_file_home(parent_path, file_dict):
    #   ToDo: Refactor to Unit Testable StaticMethod.
    tail_arr = []
    head_arr = []
    prime_str = []
    subpath_arr = []
    os_sep = os.path.sep

    max_tail = max([x.count(os_sep) for x in file_dict])
    for filepath in file_dict:
        sub_path = filepath.replace(parent_path, "")
        subpath_arr.append(sub_path)

    tail_count, keep_loop = 0, True
    while tail_count < max_tail and keep_loop:
        check_list = []
        check_dict = {}
        for x in subpath_arr:
            filepath_temp = x
            if len(tail_arr) > 0:
                for substring in tail_arr:
                    filepath_temp = filepath_temp.replace(f"{os_sep}{substring}", "")
            if filepath_temp[-1] == os_sep:
                filepath_temp = filepath_temp[:-1]
            check_list.append(filepath_temp.split(os_sep)[-1])

        for item in check_list:
            check_dict[item] = check_list.count(item)

        if len(check_dict) == 1:
            save_val = max(check_dict.items(), key=operator.itemgetter(1))[0]
            tail_arr.insert(0, save_val)
            tail_count += 1
        elif max(check_dict.items(), key=operator.itemgetter(1))[1] > 1:
            save_val = max(check_dict.items(), key=operator.itemgetter(1))[0]
            tail_arr.insert(0, save_val)
            tail_count += 1
        else:
            keep_loop = False

    head_count, keep_loop = 0, True
    common_prefix_head = tail_arr[0]
    while keep_loop and head_count < max_tail-len(tail_arr):
        check_list = []
        check_dict = {}

        for sub_path in subpath_arr:
            current_file = sub_path
            if len(head_arr) > 0:
                for item in head_arr:
                    current_file = current_file.replace(f'{item}', "")
            while current_file[0] == os_sep:
                current_file = current_file[1:]
            check_list.append(current_file.split(os_sep)[0])
        for item in check_list:
            check_dict[item] = check_list.count(item)
            if item == common_prefix_head:
                prime_str = os.path.join(parent_path, os_sep.join(head_arr + tail_arr))
                keep_loop = False
                break
        if len(check_dict) == 1:
            head_arr.insert(0, check_list[0])
            head_count += 1
        elif max(check_dict.items(), key=operator.itemgetter(1))[1] > 1:
            save_val = max(check_dict.items(), key=operator.itemgetter(1))
            head_arr.append(save_val[0])
            head_count += 1
        else:
            prime_str = os.path.join(parent_path, os_sep.join(head_arr + tail_arr))
            keep_loop = False

    if prime_str in file_dict:
        return {'Prime': prime_str}
    else:
        return {'Suggested': prime_str}


if __name__ == '__main__':
    time_mainstart = time.perf_counter()
    hash_target = Path.home() / 'Desktop' / "The Ark Challenge" / "v" / "Backup Muzik"
    testMerge = MainProcess(hash_target)
    time_mainstop = time.perf_counter()
    maintime = time_mainstop - time_mainstart
    new_dict = {}
    for x, y in testMerge.items.items():
        new_dict[x] = list(y)
    for x in new_dict:
        if len(new_dict[x]) > 1:
            # find_file_home()
            [print(hashfile.file_path) for hashfile in new_dict[x]]
    print(len(testMerge.items))
    print(f"Hash Time: {testMerge.hash_time}\nMain Time: {maintime}")
