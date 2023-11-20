import toml


def load_config(file_path: str):
    global config
    # TOML ファイルを読み込む
    config = toml.load(file_path)
    return config
