import toml

class Config:
  pass
def load_config() -> Config:
    # TOML ファイルを読み込む
    config = toml.load("config.toml")

    # 設定内容を表示
    # print("Database Information:")
    # print(f"Server: {config['database']['server']}")
    # print(f"Ports: {config['database']['ports']}")
    # print(f"Max Connections: {config['database']['connection_max']}")
    # print(f"Enabled: {config['database']['enabled']}")
    return Config()