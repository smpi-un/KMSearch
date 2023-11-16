import os
import hashlib

def calculate_file_hash(file_path:str, hash_algorithm='sha256')->str:
    # ハッシュオブジェクトを作成
    hash_object = hashlib.new(hash_algorithm)

    # ファイルをバイナリモードで開いて読み込み、ハッシュを計算
    if not os.path.isfile(file_path):
        return None
    with open(file_path, 'rb') as file:
        while True:
            data = file.read(65536)  # ファイルを小さなブロックで読み込む
            if not data:
                break
            hash_object.update(data)

    # ハッシュ値を16進数文字列として取得
    file_hash = hash_object.hexdigest()

    return file_hash
