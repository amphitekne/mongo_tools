import json
import os

path_to_config_files = "./config"
config_files_names = [pos_json for pos_json in os.listdir(path_to_config_files) if pos_json.endswith('.json')]

config_files = {}
for config_file_name in config_files_names:
    with open(os.path.join(path_to_config_files, config_file_name), 'r', encoding='utf-8') as fp:
        config_files[config_file_name] = json.load(fp)
