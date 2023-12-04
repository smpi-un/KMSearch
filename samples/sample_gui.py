import subprocess
import os
import platform
import tkinter as tk
from tkinter import ttk
import threading

# Global to keep reference to the process
process = None

def handle_output(process, result_text):
    for line in iter(process.stdout.readline, b''):
        # 末尾の改行を削除しデコード
        line = line.rstrip().decode()
        result_text.insert(tk.END, line + '\n')
        # スクロール
        result_text.see(tk.END)

def abort_process(result_text):
    global process
    if process:
        process.terminate()
        result_text.insert(tk.END, "Aborted.\n")
        result_text.see(tk.END)
    result_text.insert(tk.END, '終わったよ！\n')
    result_text.see(tk.END)

def execute_batch(subcommand: str, args: list[str], result_text: tk.Text):
    global process
    if platform.system() == "Windows":
        script_name = "kmsearch.bat"
    else:
        script_name = "kmsearch.sh"
    batch_file_path = os.path.join(os.path.dirname(__file__), '../', script_name)

    arguments = [subcommand] + args

    try:
        result_text.insert(tk.END, batch_file_path + "\n")

        process = subprocess.Popen([batch_file_path] + arguments,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   bufsize=1)

        thread = threading.Thread(target=handle_output, args=(process, result_text))
        thread.start()

    except subprocess.CalledProcessError as e:
        result_text.insert(tk.END, f"Error executing batch file: {e}\n")

root = tk.Tk()
root.title("Batch File Executor")

notebook = ttk.Notebook(root)

tab1 = ttk.Frame(notebook)
notebook.add(tab1, text='Tab')

input_label = tk.Label(tab1, text="Input:")
input_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

input_entry = tk.Entry(tab1)
input_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

browse_button = tk.Button(tab1, text="Browse")
browse_button.grid(row=1, column=2, padx=10, pady=10)

search_button = tk.Button(tab1, text="Search", command=lambda : None)
search_button.grid(row=1, column=3, padx=10, pady=10, sticky="w")

result_text = tk.Text(tab1, height=5, width=50)
result_text.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

tab1.grid_columnconfigure(3, weight=1)

tab1.grid_rowconfigure(2, weight=1)

notebook.pack(expand=True, fill="both")

button = tk.Button(
    root, text="Execute Batch File", command=lambda: execute_batch("explore", [input_entry.get()], result_text)
)
button.pack(pady=20)

abort_button = tk.Button(
    root, text="Abort", command=lambda: abort_process(result_text)
)
abort_button.pack(pady=20)

root.mainloop()
