import os
import shutil
import easyocr
import tempfile
import locale

def get_system_language():
    system_lang = locale.getdefaultlocale()[0].split("_")[0]
    return system_lang

def ocr_on_images(image_paths: list[str], custom_model_path = '', languages = []) -> tuple[dict[str, any], str]:
    system_language = [get_system_language()]
    
    if custom_model_path is None or custom_model_path.strip() == '':
        reader = easyocr.Reader(languages + system_language)
    else:
        reader = easyocr.Reader(languages + system_language, model_storage_directory=custom_model_path.strip())

    ocr_results = []
    
    # 一時フォルダを作成
    temp_folder = tempfile.mkdtemp()
    
    try:
        for image_path in image_paths:
            # 画像を一時フォルダにコピー
            temp_image_path = os.path.join(temp_folder, os.path.basename(image_path))
            shutil.copy(image_path, temp_image_path)
            
            # 一時フォルダにコピーした画像からテキストをOCRで抽出
            result = reader.readtext(temp_image_path, output_format='dict')
            # {'boxes':item[0],'text':item[1],'confident':item[2]}
            ocr_results.append(result)
    finally:
        # 一時フォルダを削除
        shutil.rmtree(temp_folder)
    
    return (ocr_results, reader.model_lang)


