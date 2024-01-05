import os
from copy import deepcopy
from pathlib import Path

from utils import rm_folder_if_exist, get_json_dict, ValuesExtractor, save_dict_as_json, save_dict_as_bson, \
    save_values_with_struct, compress, get_size_raport, get_min_size_report, calc_min_size_in_mb, save_report

TEST_FILE_NAME = r'ex3.json'
BENCHMARK_NAME = "ex3_benchmark"

DATA_PATH = Path(r".\data")
RESULTS_PATH = Path(r'.\results')
test_file_path = DATA_PATH.joinpath(TEST_FILE_NAME)


def do_benchmark(benchmark_name, file_path):
    results_path = RESULTS_PATH.joinpath(benchmark_name)
    json_path = results_path.joinpath("raw_json.json")
    metadata_path = results_path.joinpath("metadata.json")
    raw_bson_path = results_path.joinpath("bson_with_whole_json.bson")
    bson_with_only_values_path = results_path.joinpath("bson_with_only_values.bson")
    struct_packed_folder_path = results_path.joinpath("struct_packed")
    zipped_json_path = results_path.joinpath("zipped_json.gz")
    zipped_raw_bson_path = results_path.joinpath("zipped_raw_bson.gz")
    zipped_bson_with_only_values_path = results_path.joinpath("zipped_bson_with_only_values.gz")
    zipped_struct_path = results_path.joinpath("zipped_struct.gz")
    print("START BENCHMARK")
    rm_folder_if_exist(results_path)
    os.mkdir(results_path)

    json_dict = get_json_dict(file_path)
    raw_json_dict = deepcopy(json_dict)

    ve = ValuesExtractor()
    values, metadata = ve.split_values_and_metadata(json_dict)
    values_dict = {"v": values}
    print("START SAVING")
    save_dict_as_json(raw_json_dict, json_path)
    save_dict_as_json(metadata, metadata_path)

    save_dict_as_bson(raw_json_dict, raw_bson_path)
    save_dict_as_bson(values_dict, bson_with_only_values_path)

    save_values_with_struct(values, struct_packed_folder_path)
    print("START COMPRESSING")
    compress(json_path, zipped_json_path)

    compress(raw_bson_path, zipped_raw_bson_path)
    compress(bson_with_only_values_path, zipped_bson_with_only_values_path)

    compress(struct_packed_folder_path, zipped_struct_path, folder=True)
    print("GENERATING REPORT")
    whole_report = ""

    whole_report += get_min_size_report(values, metadata_path)

    whole_report += get_size_raport(json_path)
    whole_report += get_size_raport(raw_bson_path)
    whole_report += get_size_raport(bson_with_only_values_path, metadata_path)
    whole_report += get_size_raport(struct_packed_folder_path, metadata_path, folder=True)

    whole_report += get_size_raport(zipped_json_path)
    whole_report += get_size_raport(zipped_raw_bson_path)
    whole_report += get_size_raport(zipped_bson_with_only_values_path, metadata_path)
    whole_report += get_size_raport(zipped_struct_path, metadata_path)

    save_report(results_path, whole_report)
    print(whole_report)


if __name__ == "__main__":
    do_benchmark(BENCHMARK_NAME, test_file_path)




