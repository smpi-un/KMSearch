from .extractor import *
import os
import zipfile
import xml.etree.ElementTree as ET
import tempfile
import shutil

class ExcelSharpExtractor(Extractor):
    method = 'excelSharp'
    def __init__(self):
        pass
    def extract(self, path: str) -> ExtractResult:
        extract_details = {
        }
        search_texts = extract_drawing_data(path)
        return ExtractResult(extract_details, search_texts)

def extract_drawing_data(zip_file_path: str) -> list[SearchText]:
    # 一時フォルダを作成
    temp_folder_path = tempfile.mkdtemp()
    # 一時フォルダを作成
    if not os.path.exists(temp_folder_path):
        os.makedirs(temp_folder_path)

    # Zipファイルを解凍
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(temp_folder_path)

    # xl/drawings フォルダのパス
    drawings_folder_path = os.path.join(temp_folder_path, 'xl', 'drawings')
    drawing_data = get_drawings_data(drawings_folder_path)

    # 一時フォルダを削除
    try:
        shutil.rmtree(temp_folder_path)
    except Exception as e:
        print(e)

    search_texts = []
    for filename, texts in drawing_data.items():
        for text in texts:
            details = {
                "sheet_drawings_file_name" : filename
            }
            search_text = SearchText(text, details)
            search_texts.append(search_text)
    return search_texts

def get_drawings_data(drawings_folder_path: str) -> dict[str, list[str]]:
    # drawingデータを格納する辞書
    drawing_data = {}

    # xl/drawings フォルダが存在する場合
    if os.path.exists(drawings_folder_path):
        # フォルダ内の XML ファイルを検索
        for filename in os.listdir(drawings_folder_path):
            if filename.startswith('drawing') and filename.endswith('.xml'):
                file_path = os.path.join(drawings_folder_path, filename)

                # XML ファイルを解析してデータを取得
                with open(file_path, 'r', encoding='utf-8') as file:
                    xml_data = file.read()
                    root = ET.fromstring(xml_data)
                    # ここでXMLデータを必要な形に変換するか処理を追加
                    elem_data = []
                    for elem in root.findall(".//{http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing}sp"):
                        # すべてのテキストを抽出
                        all_text_elements = [element.text for element in elem.iter()]

                        # Noneでないテキスト要素だけを抽出
                        all_text_elements = [text for text in all_text_elements if text is not None and text != ""]

                        # 抽出したテキストを結合して返す
                        all_text = ''.join(all_text_elements)

                        if all_text != '':
                            elem_data.append(all_text)

                    # ファイル名をキー、データを値として辞書に追加
                    drawing_data[filename] = elem_data

    return drawing_data