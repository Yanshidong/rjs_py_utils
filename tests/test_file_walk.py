import os


def get_dir_files_name( dir_path):
    for root,dirs,files in os.walk(dir_path):
        for fi in files:
            print(fi)

get_dir_files_name('./tmp/keyvaluepairs')
