# KMSearch

## プログラムについて

このプログラムは、Pythonで書かれたコマンドラインインターフェースで、フォルダ探索、登録済みデータの更新、ファイル検索、指定パスによるドキュメント情報の表示を可能にします。

## コマンド

プログラムには7つのコマンドがあります。

1. **main**
    この関数は、パーサーを初期化し、実行します。

2. **explore**
    フォルダを探索します。構文：`explore dir_path [dir_path ...] [--model_path MODEL_PATH]`
    - dir_path：探索するディレクトリのパス。
    - `--model_path`：モデルのパス。任意。

3. **update**
    登録済みのデータを更新します。構文：`update [--model_path MODEL_PATH]`
    - `--model_path`：モデルのパス。任意。

4. **search**
    キーワードを使用してファイルを検索します。構文：`search keyword [--extract_type EXTRACT_TYPE] [--file_path_pattern FILE_PATH_PATTERN]`
    - keyword：検索のキーワード。
    - `--extract_type`：抽出タイプ。任意。
    - `--file_path_pattern`：ファイルパスのパターン。任意。

5. **showdocument**
    パスを指定してドキュメント情報を表示します。構文：`showdocument path`
    - path：表示したいドキュメントへのパス。
