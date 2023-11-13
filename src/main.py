import database_engine
import explorefiles
import searchfiles
import argparse
import updatedata
import showdocument
import services.excel

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
    elif args.subcommand == "update":
        updatedata.update(args.model_path)
    elif args.subcommand == "search":
        searchfiles.search(args.keyword)
    else:
        parser.print_help()
      
if __name__ == "__main__":
    main()
    # path = r"C:\Users\sml150823\Desktop\新しいフォルダー\10.1.11.49-20231026102845-00001.pdf"
    # path = r"\\Dns11\精密機器\技術\00_技術統括部\02_第二技術部\02_規格設計課\500_係別\530_規格設計三係\50_非定型業務\2023年度\2-6-4_アクションプラン検討\スケジュール.xlsx"
    # print(services.excel.excel_to_json_string(path))
    # print(services.excel.extract_drawing_data(path, r'c:\ttemp'))
    
    # services.showdocument.show_document(path)
