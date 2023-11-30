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
        notebook.add(tab1, text='Tab')

        input_label = tk.Label(tab1, text="Input:")
        input_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        input_entry = tk.Entry(tab1)
        input_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        browse_button = tk.Button(tab1, text="Browse")
        browse_button.grid(row=0, column=2, padx=10, pady=10)

        search_button = tk.Button(tab1, text="Search")
        search_button.grid(row=0, column=3, padx=10, pady=10, sticky="w")

        self.result_text = tk.Text(tab1, height=10, width=50)
        self.result_text.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        tab1.grid_columnconfigure(3, weight=1)
        tab1.grid_rowconfigure(1, weight=1)

        execute_button = tk.Button(self, text="Execute Batch File", command=self.execute_batch)
        execute_button.pack(pady=10)

        abort_button = tk.Button(self, text="Abort", command=self.abort_process)
        abort_button.pack(pady=10)
        
        notebook.pack(expand=True, fill="both")

    def execute_batch(self):
        subcommand = "explore"
        args = ["."]
        if platform.system() == "Windows":
            script_name = "kmsearch.bat"
        else:
            script_name = "kmsearch.sh"
        batch_file_path = os.path.join(os.path.dirname(__file__), "../", script_name)
        arguments = [subcommand] + args

        self.result_text.insert(tk.END, batch_file_path + "\n")

        self.process = subprocess.Popen(
            [batch_file_path] + arguments,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )

        thread = threading.Thread(target=self.handle_output)
        thread.start()

    def handle_output(self):
        for line in iter(self.process.stdout.readline, ""):
            line = line.rstrip()
            self.result_text.insert(tk.END, line + "\n")
            self.result_text.see(tk.END)

    def abort_process(self):
        if self.process:
            os.kill(self.process.pid, SIGTERM)  # Send the SIGTERM signal.
            self.result_text.insert(tk.END, "Aborted.\n")
            self.result_text.see(tk.END)


if __name__ == "__main__":
    app = Application()
    app.title("Batch File Executor")
    app.mainloop()
