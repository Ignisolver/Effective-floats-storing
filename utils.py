import json
import os
import shutil
import struct
from typing import List
import tarfile
import gzip

import bson

from pathlib import Path


BYTES_IN_MEGABYTE = 1000_000
BYTES_IN_FLOAT = 8
RESULTS_FILES_PATH = "files"
class ValuesExtractor:
    def __init__(self):
        self.values = []
        self.val_set_id = 0

    def split_values_and_metadata(self, json_dict: dict):
        self._manage_dict(json_dict)
        self.val_set_id = 0
        metadata = json_dict
        return self.values, metadata

    def _manage_obj(self, obj):
        if isinstance(obj, list):
            self._manage_list(obj)
        if isinstance(obj, dict):
            self._manage_dict(obj)
        else:
            pass

    def _manage_list(self, obj: list):
        for el in obj:
            self._manage_obj(el)

    def _manage_dict(self, obj: dict):
        for key in obj:
            if key == "values":
                self.values.append(obj[key])
                obj[key] = self.val_set_id
                self.val_set_id += 1
            else:
                self._manage_obj(obj[key])


def get_json_dict(file_path):
    with open(file_path) as f:
        json_dict = json.load(f)
    return json_dict


def get_min_size_report(values_list, meta_path):
    report = "Min available size without_compression = "
    min_values_size = calc_min_size_in_mb(values_list)
    meta_size = get_size_in_mb(meta_path)
    report += str(round(min_values_size + meta_size, 3)) + " MB\n"
    return report


def get_size_raport(file_path, meta_path=None, folder=False):
    file_name = file_path.name
    meta_size = 0
    if meta_path:
        meta_size = get_size_in_mb(meta_path)
    file_size = get_size_in_mb(file_path, folder=folder)
    report = f"File: {file_name}"
    if meta_path:
        report += f" + metadata"
    report += f" = {round(file_size, 3):<6}"
    if meta_path:
        report += f" + {round(meta_size, 3):<6}"
    report += f" = {round(meta_size+file_size, 3):6}"
    report += " MB\n"
    return report

def get_dir_size(path='.'):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total


def get_size_in_mb(path, folder=False):
    if folder:
        size_in_bytes = get_dir_size(path)
    else:
        size_in_bytes = os.path.getsize(path)
    size_in_mb = size_in_bytes / BYTES_IN_MEGABYTE
    return size_in_mb


def compress(source_path, dest_path, folder=False):
    if folder:
        # Create a temporary tar archive
        temp_tar_path = str(dest_path) + '.tar'
        with tarfile.open(temp_tar_path, 'w') as tar:
            tar.add(source_path, arcname=os.path.basename(source_path))

        # Compress the tar archive using gzip
        with open(temp_tar_path, 'rb') as f_in, gzip.open(dest_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

        # Delete the temporary tar archive
        os.remove(temp_tar_path)
    else:
        # Compress the single file using gzip
        with open(source_path, 'rb') as f_in, gzip.open(dest_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


def rm_folder_if_exist(results_path):
    try:
        shutil.rmtree(results_path)
    except FileNotFoundError:
        pass


def save_dict_as_bson(dict_, dest_path):
    bson_obj = bson.dumps(dict_)
    with open(dest_path, "wb") as file:
        file.write(bson_obj)


def save_dict_as_json(dict_, dest_path):
    with open(dest_path, "w") as file:
        json.dump(dict_, file)


def save_values_with_struct(values_list: List[List[float]], dest_folder_path):
    folder_path = Path(dest_folder_path)
    Path.mkdir(folder_path)
    for nr, values in enumerate(values_list):
        binary_data = struct.pack(f'!{len(values)}d', *values)
        file_name = f'{nr}.bin'
        file_path = folder_path.joinpath(file_name)
        with open(file_path, 'wb') as file:
            file.write(binary_data)


def calc_min_size_in_mb(values_list):
    floats_amount = 0
    for values in values_list:
        floats_amount += len(values)
    size_in_mb = floats_amount * BYTES_IN_FLOAT / BYTES_IN_MEGABYTE
    return size_in_mb


def save_report(path, report):
    report_path = path.joinpath("REPORT.txt")
    with open(report_path, 'w') as f:
        f.write(report)