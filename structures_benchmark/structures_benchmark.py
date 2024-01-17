import os
from copy import deepcopy
from pathlib import Path

from utils import rm_folder_if_exist, get_json_dict, ValuesExtractor, save_dict_as_json, save_dict_as_bson, \
    save_values_with_struct, compress, get_size_raport, get_min_size_report, save_report

TEST_FILE_NAME = r'ex3.json'  # my_json.json / zero_json.json
BENCHMARK_NAME = "restored_benchmark"

DATA_PATH = Path(r".\data")
RESULTS_PATH = Path(r'.\results')
test_file_path = DATA_PATH.joinpath(TEST_FILE_NAME)


def do_benchmark(benchmark_name, file_path):
    results_path = RESULTS_PATH / benchmark_name
    json_path = results_path / "raw_json.json"
    metadata_path = results_path / "metadata.json"
    metadata_2_path = results_path / "struct_packed" / "metadata.json"
    raw_bson_path = results_path / "bson_with_whole_json.bson"
    bson_with_only_values_path = results_path / "bson_with_only_values.bson"
    struct_packed_folder_path = results_path / "struct_packed"
    zipped_json_path = results_path / "zipped_json.zip"
    zipped_raw_bson_path = results_path / "zipped_raw_bson.zip"
    zipped_bson_with_only_values_path = results_path / "zipped_bson_with_only_values.zip"
    zipped_struct_path = results_path / "zipped_struct.zip"
    print("START BENCHMARK")
    rm_folder_if_exist(results_path)
    os.mkdir(results_path)

    json_dict = get_json_dict(file_path)
    raw_json_dict = deepcopy(json_dict)

    ve = ValuesExtractor()
    values, metadata = ve.split_values_and_metadata(json_dict)
    values_dict = {"v": values}

    print("SAVING...")
    save_dict_as_json(raw_json_dict, json_path)
    save_dict_as_json(metadata, metadata_path)

    save_dict_as_bson(raw_json_dict, raw_bson_path)
    save_dict_as_bson(values_dict, bson_with_only_values_path)

    save_values_with_struct(values, struct_packed_folder_path)
    save_dict_as_json(metadata, metadata_2_path)

    print("COMPRESSING...")
    compress(json_path, zipped_json_path)

    compress(raw_bson_path, zipped_raw_bson_path)
    compress(bson_with_only_values_path, zipped_bson_with_only_values_path)

    compress(struct_packed_folder_path, zipped_struct_path, folder=True)

    print("GENERATING REPORT...")
    whole_report = "RAPORT\n"
    whole_report += f"FILE: {file_path}\n\n"

    whole_report += get_min_size_report(values, metadata_path)

    whole_report += get_size_raport(json_path)
    whole_report += get_size_raport(raw_bson_path)
    whole_report += get_size_raport(bson_with_only_values_path, metadata_path)
    whole_report += get_size_raport(struct_packed_folder_path, folder=True)

    whole_report += get_size_raport(zipped_json_path)
    whole_report += get_size_raport(zipped_raw_bson_path)
    whole_report += get_size_raport(zipped_bson_with_only_values_path, metadata_path)
    whole_report += get_size_raport(zipped_struct_path)

    save_report(results_path, whole_report)
    print(f"REPORT AND RESULTS SAVED TO {results_path}")
    print(whole_report)


if __name__ == "__main__":
    do_benchmark(BENCHMARK_NAME, test_file_path)




