import os
import tempfile
import utils.filehash as filehash
import services.ocrimage as ocrimage
import services.pdftoimage as pdftoimage
import services.multitosingleimages as multitosingleimages
import services.excel as excel
import database_engine
import models.file
import models.extract
import models.search
from datetime import datetime

pdf_exts = [".pdf"]
image_exts = [
    ".avif",
    ".webp",
    ".tif",
    ".tiff",
    ".jpg",
    ".jpeg",
    ".bmp",
    ".png",
]
excel_exts = [".xlsx", ".xlsm"]


def explore(base_dir: str, model_path: str):
    for root, _, files in os.walk(base_dir):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            input_file_path = os.path.join(root, file)
            if ext in pdf_exts + image_exts:
                ocr_image(input_file_path, model_path)
            elif ext in excel_exts:
                extract_excel(input_file_path)


def ocr_image(input_file_path: str, model_path: str):
    # print(json.dumps(res_for_json, indent=2))
    hash = filehash.calculate_file_hash(input_file_path)

    reg_document_id = models.document.get_document_id_by_hash(hash)
    reg_file_id = models.file.get_file_id_by_hash(input_file_path)

    if reg_document_id is None:
        # ドキュメント未登録
        print(f"mitouroku: {input_file_path}")

        # 一時フォルダを作成
        temp_dir = tempfile.mkdtemp()

        # PDF・画像を一時フォルダに画像として保存
        if os.path.splitext(input_file_path)[1].lower() in pdf_exts:
            images = pdftoimage.pdf_to_temp_images(input_file_path, temp_dir)
        elif os.path.splitext(input_file_path)[1].lower() in image_exts:
            images = multitosingleimages.save_pages_as_png(input_file_path, temp_dir)

        # 画像情報に対してOCRを実行
        ocr_result, model_language, custom_model_path = ocrimage.ocr_on_images(
            images, model_path
        )

        # 一時フォルダ内の画像を削除
        for image in os.listdir(temp_dir):
            image_path = os.path.join(temp_dir, image)
            os.remove(image_path)

        # 一時フォルダを削除
        os.rmdir(temp_dir)

        res_for_json = []
        for ocr_data in ocr_result:
            new_ocr_data = []
            for r in ocr_data:
                d = dict()
                # jsonに変換するため、numpy intから通常のintに変換する
                d["boxes"] = [[int(x) for x in pos] for pos in r["boxes"]]
                d["text"] = r["text"]
                d["confident"] = r["confident"]
                new_ocr_data.append(d)
            res_for_json.append(new_ocr_data)

        document_id = models.document.insert_document(
            hash, os.path.getsize(input_file_path)
        )
        if reg_file_id is None:
            # ファイルが未登録の場合はファイルの登録
            file_id = models.file.insert_file(document_id, input_file_path, False)
        else:
            # ファイルが登録済みの場合はファイルとドキュメントの紐付けし直し
            models.file.update_document_id(reg_file_id, document_id)

        details = {
            "model_language": model_language,
            "custom_model_path": custom_model_path,
        }
        extract_id = models.extract.insert_extract_data(
            document_id, res_for_json, details,
        )

        for i, r in enumerate(res_for_json):
            for ocr_dict in r:
                position = {"page": i}
                search_text_id = models.search.insert_search_text(
                    extract_id, ocr_dict["text"], position
                )
                # print(ocr_json)
    else:
        print(f"tourokuzumi: {input_file_path}")
        # ドキュメント登録済み
        if reg_file_id is None:
            file_id = models.file.insert_file(reg_document_id, input_file_path, False)

def extract_excel(input_file_path: str):
    # print(json.dumps(res_for_json, indent=2))
    hash = filehash.calculate_file_hash(input_file_path)

    reg_document_id = models.document.get_document_id_by_hash(hash)
    reg_file_id = models.file.get_file_id_by_hash(input_file_path)

    if reg_document_id is None:
        # ドキュメント未登録
        print(f"mitouroku: {input_file_path}")

        # 画像情報に対してOCRを実行
        extract_result = excel.excel_to_json_string(input_file_path)
        if extract_result is None:
            return

        document_id = models.document.insert_document(
            hash, os.path.getsize(input_file_path)
        )
        if reg_file_id is None:
            # ファイルが未登録の場合はファイルの登録
            file_id = models.file.insert_file(document_id, input_file_path, False)
        else:
            # ファイルが登録済みの場合はファイルとドキュメントの紐付けし直し
            models.file.update_document_id(reg_file_id, document_id)

        extract_id = models.extract.insert_extract_data(
            document_id, extract_result, {}
        )

        for i, sheet in enumerate(extract_result.values()):
            for cell in sheet['cells']:
                search_text_id = models.search.insert_search_text(
                    extract_id, cell["value"], cell
                )
                # print(ocr_json)
    else:
        print(f"tourokuzumi: {input_file_path}")
        # ドキュメント登録済み
        if reg_file_id is None:
            file_id = models.file.insert_file(reg_document_id, input_file_path, False)