import argparse
import toml
import services.explorefiles as explorefiles
import services.searchfile as searchfile
import services.updatedata as updatedata
import services.showdocument as showdocument
import services.searchcsv as searchcsv

def main():
    parser = argparse.ArgumentParser(description="フォルダの探索とファイル検索ツール")

    subparsers = parser.add_subparsers(title="サブコマンド", dest="subcommand")

    # 'explore' サブコマンド
    explore_parser = subparsers.add_parser("explore", help="フォルダを探索")
    explore_parser.add_argument("dir_path", type=str, nargs='+', help="フォルダのパス")
    explore_parser.add_argument("--model_path", type=str, help="モデルのパス")

    # 'update' サブコマンド
    update_parser = subparsers.add_parser("update", help="登録済みデータを更新")
    update_parser.add_argument("--model_path", type=str, help="モデルのパス")

    # 'search' サブコマンド
    search_parser = subparsers.add_parser("search", help="ファイルを検索")
    search_parser.add_argument("keyword", type=str, help="検索キーワード")
    search_parser.add_argument("--extract_type", type=str, help="抽出タイプ")
    search_parser.add_argument("--file_path_pattern", type=str, help="ファイルパスのパターン")

    # 'showdocument' サブコマンド
    showdocument_parser = subparsers.add_parser("showdocument", help="パスを指定してドキュメント情報を表示")
    showdocument_parser.add_argument("path", type=str, help="表示対象ドキュメント")

    args = parser.parse_args()

    if args.subcommand == "explore":
        explorefiles.explore(args.dir_path, args.model_path)
    elif args.subcommand == "update":
        updatedata.update(args.model_path)
    elif args.subcommand == "search":
        searchfile.search(args.keyword, args.extract_type, args.file_path_pattern)
    elif args.subcommand == "showdocument":
        showdocument.show_document(args.path)
    else:
        parser.print_help()

def load_config():
    # TOML ファイルを読み込む
    config = toml.load("config.toml")

    # 設定内容を表示
    print("Database Information:")
    print(f"Server: {config['database']['server']}")
    print(f"Ports: {config['database']['ports']}")
    print(f"Max Connections: {config['database']['connection_max']}")
    print(f"Enabled: {config['database']['enabled']}")



if __name__ == "__main__":
    load_config()
    main()