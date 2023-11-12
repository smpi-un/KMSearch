import database_engine
import explorefiles
import searchfiles
import argparse
import updatedata

def main():
    parser = argparse.ArgumentParser(description="フォルダの探索とファイル検索ツール")

    subparsers = parser.add_subparsers(title="サブコマンド", dest="subcommand")

    # 'explore' サブコマンド
    explore_parser = subparsers.add_parser("explore", help="フォルダを探索")
    explore_parser.add_argument("dir_path", type=str, help="フォルダのパス")
    explore_parser.add_argument("--model_path", type=str, help="モデルのパス")

    # 'update' サブコマンド
    update_parser = subparsers.add_parser("update", help="登録済みデータを更新")
    update_parser.add_argument("--model_path", type=str, help="モデルのパス")

    # 'search' サブコマンド
    search_parser = subparsers.add_parser("search", help="ファイルを検索")
    search_parser.add_argument("keyword", type=str, help="検索キーワード")

    args = parser.parse_args()

    if args.subcommand == "explore":
        explorefiles.explore(args.dir_path, args.model_path)
    if args.subcommand == "update":
        updatedata.update(args.model_path)
    elif args.subcommand == "search":
        searchfiles.search(args.keyword)
    else:
        parser.print_help()
      
if __name__ == "__main__":
    main()
