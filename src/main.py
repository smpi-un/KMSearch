import argparse
from database_engine import init_database, get_engine, init_engine
import services.explorefiles as explorefiles
import services.searchfile as searchfile
import services.updatedata as updatedata
import services.showdocument as showdocument
from utils.config import load_config
from sys import exit
from typing import Literal

def main(config: dict):
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
    search_parser.add_argument("--extract_method", type=str, help="抽出タイプ")
    search_parser.add_argument("--file_path_pattern", type=str, help="ファイルパスのパターン")
    search_parser.add_argument("--unit", type=str, choices=["word", "page", "file"], help="検索単位", default='page')
    search_parser.add_argument("--out", type=str, help="出力先ファイル名")

    # 'showdocument' サブコマンド
    showdocument_parser = subparsers.add_parser("showdocument", help="パスを指定してドキュメント情報を表示")
    showdocument_parser.add_argument("path", type=str, help="表示対象ドキュメント")
    showdocument_parser.add_argument("--out", type=str, help="出力先ファイル名")

    args = parser.parse_args()

    match args.subcommand:
        case "explore":
            res = explorefiles.explore(args.dir_path, config['explore'], config["ocr"])
        case "update":
            res = updatedata.update(args.model_path)
        case "search":
            res = searchfile.search(args.keyword,
                                    unit=args.unit,
                                    extract_method=args.extract_method,
                                    file_path_pattern=args.file_path_pattern,
                                    out_path=args.out,
                                    )
        case "show":
            res = showdocument.show_document(args.path, args.out)
        case _:
            parser.print_help()
            res = 0
    exit(res)

if __name__ == "__main__":
    config = load_config("./config.toml")
    init_engine(config["database"]["url"])
    assert get_engine() is not None, "Engine is not initialized."
    init_database()
    main(config)