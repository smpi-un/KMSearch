import os
from PIL import Image, ImageSequence

def save_pages_as_png(tiff_path, output_folder):
    # フォルダが存在しない場合は作成
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    saved_paths = []  # 保存したPNGファイルのパスを格納するリスト

    # TIFFファイルを開く
    with Image.open(tiff_path) as img:
        # すべてのページを取得し、PNGファイルとして保存
        for i, page in enumerate(ImageSequence.Iterator(img)):
            # ファイル名の生成
            file_name = f"page_{i}.png"
            # ファイルの保存パス
            save_path = os.path.join(output_folder, file_name)
            # 画像をPNGファイルとして保存
            page = page.convert("RGB")
            page.save(save_path, format="PNG")
            # 保存したファイルのパスをリストに追加
            saved_paths.append(save_path)

    return saved_paths

if __name__ == '__main__':
  # マルチページTIFFファイルのパス
  tiff_file_path = 'path/to/your/multi_page.tiff'
  # 保存先フォルダのパス
  output_folder_path = 'path/to/your/output/folder'

  # TIFFファイルの各ページをPNGに変換して保存し、保存したファイルのパスを取得
  saved_paths_list = save_pages_as_png(tiff_file_path, output_folder_path)

  # 保存したファイルのパスを表示
  for i, path in enumerate(saved_paths_list):
      print(f"Saved Image {i+1}: {path}")
