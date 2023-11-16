import os
from PIL import Image
import fitz  # PyMuPDFをインポート

def create_temp_images(input_path: str, temp_dir: str) -> list[str]:
    ext = os.path.splitext(input_path)[1]
    if ext == '.pdf':
        print(input_path)
        return pdf_to_temp_images(input_path, temp_dir)
    else:
        return convert_image_to_png(input_path, temp_dir)

def pdf_to_temp_images(pdf_path: str, temp_dir: str) -> list[str]:
    # PDFを画像に変換して一時フォルダに保存
    pdf_document = fitz.open(pdf_path)
    image_paths = []
    resolution = 600

    for page_number in range(len(pdf_document)):
        page = pdf_document[page_number]
        # image = page.get_pixmap()
        image = page.get_pixmap(matrix=fitz.Matrix(resolution / 72, resolution / 72))

        image_path = os.path.join(temp_dir, f"page_{page_number}.png")
        image.save(image_path, "png")
        image_paths.append(image_path)

    pdf_document.close()

    return image_paths

def convert_image_to_png(input_path: str, output_folder: str) -> list[str]:
    """
    複数ページを持つ画像ファイルをPNG形式に変換して指定したフォルダに複数のPNGファイルとして保存する関数。
    
    Args:
        input_path (str): 入力画像ファイルのパス。
        output_folder (str): 出力フォルダのパス。
    
    Returns:
        list of str: 保存されたPNGファイルのパスのリスト。
    """
    try:
        # 画像を開く
        img = Image.open(input_path)

        # 複数ページの画像をPNG形式で保存するためのリスト
        png_paths = []

        # 出力フォルダが存在しない場合は作成
        os.makedirs(output_folder, exist_ok=True)

        # 複数ページの画像を分割してPNG形式で保存
        for page in range(img.n_frames):
            img.seek(page)  # ページを切り替え

            # 出力ファイルのパスを生成
            output_path = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(input_path))[0]}_page{page + 1}.png")

            # 画像をPNG形式で保存
            img.save(output_path, 'PNG')
            
            png_paths.append(output_path)

        # 保存されたPNGファイルのパスのリストを返す
        return png_paths

    except Exception as e:
        # エラーが発生した場合は例外をキャッチしてエラーメッセージを表示
        return str(e)
