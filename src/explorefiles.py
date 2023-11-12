import os
import tempfile
import models.ocr
import utils.filehash as filehash
import services.ocrimage as ocrimage
import services.pdftoimage as pdftoimage
import database_engine
import models.file
import models.document
import models.page
import models.ocrtext
from datetime import datetime


def explore(base_dir: str, model_path: str):
    for root, _, files in os.walk(base_dir):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            input_file_path = os.path.join(root, file)
            if ext in [".pdf"]:
                ocr_pdf(input_file_path, model_path)
            elif ext in [
                ".avif",
                ".webp",
                ".tif",
                ".tiff",
                ".jpg",
                ".jpeg",
                ".bmp",
                ".png",
            ]:
                ocr_image(input_file_path)


def ocr_image(input_file_path: str):
    pass




def ocr_pdf(input_file_path: str, model_path: str):
    # print(json.dumps(res_for_json, indent=2))
    hash = filehash.calculate_file_hash(input_file_path)

    reg_document_id = models.document.get_document_id_by_hash(hash)
    reg_file_id = models.file.get_file_id_by_hash(input_file_path)

    if reg_document_id is None:
        # ドキュメント未登録
        print(f"mitouroku: {input_file_path}")

        # 一時フォルダを作成
        temp_dir = tempfile.mkdtemp()

        # PDFを一時フォルダに画像として保存
        images = pdftoimage.pdf_to_temp_images(input_file_path, temp_dir)

        # 画像情報に対してOCRを実行
        ocr_result, model_language, custom_model_path = ocrimage.ocr_on_images(
            images[0:2], model_path
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
            file_id = models.file.insert_file(
                document_id, input_file_path, False
            )
        else:
            # ファイルが登録済みの場合はファイルとドキュメントの紐付けし直し
            models.file.update_document_id(reg_file_id, document_id)

        for i, r in enumerate(res_for_json):
            page_id = models.page.insert_page_data(document_id, i)
            # ocr_json = json.dumps(r, ensure_ascii=False, indent=2)
            ocr_id = models.ocr.insert_ocr_data(
                page_id, model_language, custom_model_path, r
            )
            for ocr_dict in r:
                ocr_text_id = models.ocrtext.insert_ocr_text(ocr_id, ocr_dict)
                # print(ocr_json)
    else:
        print(f"tourokuzumi: {input_file_path}")
        # ドキュメント登録済み
        if reg_file_id is None:
            file_id = models.file.insert_file(
                reg_document_id, input_file_path, False
            )
