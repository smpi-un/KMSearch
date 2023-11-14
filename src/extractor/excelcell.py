from .extractor import *
import openpyxl

class ExcelCellExtractor(Extractor):
    method = 'excelCell'
    def __init__(self):
        pass
    def extract(self, path: str) -> ExtractResult:
        search_texts = []
        extract_details = {
        }
        all_sheet_data = extract_excel_cell(path)
        for sheet_name, sheet in all_sheet_data.items():
          for cell in sheet:
            details = {
              "sheet_name": sheet_name,
              "address": cell["address"],
              "row": cell["row"],
              "column": cell["column"],
            }
            search_text = SearchText(cell["value"], details)
            search_texts.append(search_text)
        return ExtractResult(extract_details, search_texts)

def extract_cell_data(cell) -> dict:
    if cell.data_type not in ["s", "n", "inlineStr", "str"] or cell.value is None or cell.value == "":
        return None
    return {
        "address": cell.coordinate,
        "row": cell.row,
        "column": cell.column,
        "value": cell.value,
        # "formula": cell.formula if cell.data_type == 'f' else None
    }

def extract_excel_cell(file_path) -> dict:
  # Excelファイルを開く
  workbook = openpyxl.load_workbook(file_path)

  # セルのデータを格納するためのリスト
  all_sheet_data = {}

  # すべてのシートに対して処理を行う
  for i, sheet_name in enumerate(list(workbook.sheetnames)):
      sheet = workbook[sheet_name]
      all_cell_data = []

      # シート内のセルに対して処理を行う
      for row in sheet.iter_rows():
          for cell in row:
              cell_data = extract_cell_data(cell)
              if cell_data is not None:
                all_cell_data.append(cell_data)
      all_sheet_data[sheet_name] = all_cell_data

  return all_sheet_data