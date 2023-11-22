import tkinter as tk
from tkinter import ttk

import subprocess
import os
import platform


def execute_batch(subcommand: str, args: list[str]):
    if platform.system() == "Windows":
        script_name = "kmsearch.bat"
    else:
        script_name = "kmsearch.sh"
    batch_file_path = os.path.join(os.path.dirname(__file__), script_name)

    arguments = [subcommand] + args

    try:
        subprocess.run([batch_file_path] + arguments, check=True)
        print("Batch file executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing batch file: {e}")


# Tkinterウィンドウの作成
root = tk.Tk()
root.title("Batch File Executor")

# Notebook（タブ）を作成
notebook = ttk.Notebook(root)

tab1 = ttk.Frame(notebook)
notebook.add(tab1, text='Tab')

# タブ内のコンテンツを追加
# label = tk.Label(tab, text=f"This is the {tab_name} tab")
# label.pack(padx=10, pady=10)
# 入力ボックス、参照ボタン、探索ボタンを配置
input_label = tk.Label(tab1, text="Input:")
input_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

input_entry = tk.Entry(tab1)
input_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

browse_button = tk.Button(tab1, text="Browse")
browse_button.grid(row=1, column=2, padx=10, pady=10)

search_button = tk.Button(tab1, text="Search", command=lambda : None)
search_button.grid(row=1, column=3, padx=10, pady=10, sticky="w")

# 結果表示用のテキストフィールドを配置
result_text = tk.Text(tab1, height=5, width=50)
result_text.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

# テキストフィールドの列にのみ重みを設定してリサイズに対応
tab1.grid_columnconfigure(3, weight=1)

# 行の重みを設定してリサイズに対応
tab1.grid_rowconfigure(2, weight=1)


# タブを配置
notebook.pack(expand=True, fill="both")



# ボタンの作成
button = tk.Button(
    root, text="Execute Batch File", command=lambda: execute_batch("explore", ["."])
)
button.pack(pady=20)

# ウィンドウの表示
root.mainloop()