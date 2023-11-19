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
    # drawing_data = get_drawings_data(drawings_folder_path)
    sheet_list = get_sheet_list(temp_folder_path)
    worksheet_dict = rel_worksheet_file(temp_folder_path)
    drawing_data_list = []
    for sheet in sheet_list:
        sheet_path = worksheet_dict[sheet["id"]]
        drawing_id = get_drawing_id(temp_folder_path, sheet_path)
        if drawing_id is None:
            continue
        drawing_dict = get_drawingfile_from_sheet(temp_folder_path, sheet_path)
        sheet_drawing_data = get_drawings_data(temp_folder_path, drawing_dict[drawing_id])
        drawing_data_list.append(sheet_drawing_data)

    # 一時フォルダを削除
    try:
        shutil.rmtree(temp_folder_path)
    except Exception as e:
        print(e)

    search_texts = []
    file_texts = []
    file_details = {}
    for sheet_drawing_data in drawing_data_list:
        page_texts = []
        page_details = { }
        for drawing_data in sheet_drawing_data:
            
            details = {
                "name" : drawing_data["name"]
            }
            page_text = SearchText(drawing_data["text"], SearchTextUnit.word, details)
            search_texts.append(page_text)
            page_texts.append(drawing_data["text"])
            
        page_search_text = SearchText('\n'.join(page_texts), SearchTextUnit.page, page_details)
        search_texts.append(page_search_text)
    file_search_text = SearchText('\n'.join(file_texts), SearchTextUnit.file, file_details)
    search_texts.append(file_search_text)
    return search_texts


def get_sheet_list(workbook_dir: str) -> list[dict[str, str]]:
    workbook_path = os.path.join(workbook_dir, 'xl/workbook.xml')
    # xl/drawings フォルダが存在する場合
    if not os.path.exists(workbook_path):
        return None

    # XML 文字列
    with open(workbook_path, 'r') as fp:
        xml = fp.read()

    # XML のパース
    root = ET.fromstring(xml)

    # シートのIDと名前の辞書作成
    sheet_list = []
    for sheet in root.iter('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}sheet'):
        s = {
            "sheetId": sheet.attrib['sheetId'],
            "name": sheet.attrib['name'],
            "id": sheet.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id'],
        }
        sheet_list.append(s)

    return sheet_list

def rel_worksheet_file(workbook_dir: str) -> dict[str, str]:
    rels_path = os.path.join(workbook_dir, 'xl/_rels/workbook.xml.rels')
    root = ET.parse(rels_path)
    # RelationshipのIDとTargetの辞書を作成
    # RelationshipのIDとTargetの辞書を作成
    relationship_dict = {}
    for relationship in root.iter('{http://schemas.openxmlformats.org/package/2006/relationships}Relationship'):
        relationship_dict[relationship.attrib['Id']] = relationship.attrib['Target']
    return relationship_dict

def get_drawing_id(workbook_dir: str, sheet_path: str):
    abs_path = os.path.join(workbook_dir, 'xl', sheet_path)
    # XML ファイルからパース
    tree = ET.parse(abs_path)
    root = tree.getroot()

    # Drawingのidを取得
    tag = root.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}drawing')
    if tag is None:
        return None
    drawing_id = tag.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']
    return drawing_id




def get_drawingfile_from_sheet(workbook_dir:str, sheet_id:str):
    rels_path = os.path.join(workbook_dir, 'xl/worksheets/_rels', os.path.basename(sheet_id) + '.rels')
    root = ET.parse(rels_path)
    # RelationshipのIDとTargetの辞書を作成
    relationship_dict = {}
    for relationship in root.iter('{http://schemas.openxmlformats.org/package/2006/relationships}Relationship'):
        relationship_dict[relationship.attrib['Id']] = relationship.attrib['Target']

    return relationship_dict




def get_drawings_data(workbook_dir: str, drawing_path: str) -> dict[str, list[str]]:
    # drawingデータを格納する辞書
    drawing_data = {}

    file_path = os.path.join(workbook_dir, 'xl/drawings', os.path.basename(drawing_path))

    # XML ファイルを解析してデータを取得
    root = ET.parse(file_path)
    # ここでXMLデータを必要な形に変換するか処理を追加
    elem_data = []
    # 名前空間の定義
    ns = {
        'xdr': 'http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing',
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'
    }
    # sp の名前とテキストを抽出
    for sp in root.findall('.//xdr:sp', ns):
        name = sp.find('./xdr:nvSpPr/xdr:cNvPr', ns).attrib['name']
        text = sp.find('.//a:t', ns).text

        elem_data.append({'name': name, 'text': text})
    return elem_data



def get_drawings_data__(drawings_folder_path: str) -> dict[str, list[str]]:
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


def test():

    b = '/home/smpiun/Downloads/pop_area_2009 (コピー)/'
    sheet_list = get_sheet_list(b)
    print(sheet_list)
    worksheet_dict = rel_worksheet_file(b)
    for sheet in sheet_list:
        sheet_path = worksheet_dict[sheet["id"]]
        drawing_id = get_drawing_id(b, sheet_path)
        if drawing_id is None:
            continue
        drawing_dict = get_drawingfile_from_sheet(b, sheet_path)
        drawing_data = get_drawings_data(b, drawing_dict[drawing_id])
        print(drawing_data)
        # get_drawing_path(b, sh)