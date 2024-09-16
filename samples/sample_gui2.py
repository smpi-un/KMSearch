import os
import platform
import threading
import tkinter as tk
import subprocess
from tkinter import ttk
from signal import SIGTERM

class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.process = None
        self.create_widgets()

    def create_widgets(self):
        notebook = ttk.Notebook(self)

        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text='Explore')

        self.create_explore_tab_widgets(tab1)

        tab1.grid_columnconfigure(3, weight=1)
        tab1.grid_rowconfigure(1, weight=1)
        
        notebook.pack(expand=True, fill="both")

    def create_explore_tab_widgets(self, tab):

        input_label = tk.Label(tab, text="Input:")
        input_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        input_entry = tk.Entry(tab)
        input_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        browse_button = tk.Button(tab, text="Browse")
        browse_button.grid(row=0, column=2, padx=10, pady=10)

        search_button = tk.Button(tab, text="Search")
        search_button.grid(row=0, column=3, padx=10, pady=10, sticky="w")

        self.result_text = tk.Text(tab, height=10, width=50)
        self.result_text.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        abort_button = tk.Button(tab, text="Abort", command=self.abort_process)
        abort_button.pack(pady=10)

        execute_button = tk.Button(tab, text="Execute Batch File", command=lambda :self.explore(input_entry.get()))
        execute_button.pack(pady=10)

    def clear_output(self):
        self.result_text.delete(1.0, tk.END)
    def insert_text(self, text: str):
        self.result_text.insert(tk.END, text + "\n")
        self.result_text.see(tk.END)

    def execute_batch(self, subcommand: str, args: list[str]):
        if platform.system() == "Windows":
            script_name = "kmsearch.bat"
        else:
            script_name = "kmsearch.sh"
        batch_file_path = os.path.join(os.path.dirname(__file__), "../", script_name)
        arguments = [subcommand] + args

        self.insert_text(batch_file_path)

        self.process = subprocess.Popen(
            [batch_file_path] + arguments,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )

        thread = threading.Thread(target=self.handle_output)
        thread.start()

    def explore(self, path: str):
        self.clear_output()
        if path is None or not os.path.exists(path):
            self.insert_text(f'"{path}" is not found. {path}')
            return
        subcommand = "explore"
        args = [path]
        self.execute_batch(subcommand, args)


    def handle_output(self):
        for line in iter(self.process.stdout.readline, ""):
            line = line.rstrip()
            self.insert_text(line)
        self.insert_text("Finished.")

    def abort_process(self):
        if self.process:
            os.kill(self.process.pid, SIGTERM)  # Send the SIGTERM signal.
            self.insert_text("Aborted.")


if __name__ == "__main__":
    app = Application()
    app.title("Batch File Executor")
    app.mainloop()
