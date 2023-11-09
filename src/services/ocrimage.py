import os
import shutil
import easyocr
import tempfile

def ocr_on_images(image_paths: list[str], custom_model_path = '') -> tuple[dict[str, any], str, str]:
    language = []
    
    if custom_model_path is None or custom_model_path.strip() == '':
        reader = easyocr.Reader(['ja', 'en'] + language)
    else:
        reader = easyocr.Reader(['ja', 'en'] + language, model_storage_directory=custom_model_path.strip())

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
    
    return (ocr_results, reader.model_lang, custom_model_path)


