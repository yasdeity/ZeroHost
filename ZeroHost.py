import os
import tkinter as tk
from tkinter import filedialog, messagebox
import http.server
import socketserver
import threading
import webbrowser

class LocalServerThread(threading.Thread):
    def __init__(self, port, directory):
        super().__init__()
        self.port = port
        self.directory = directory

    def run(self):
        os.chdir(self.directory)
        handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", self.port), handler) as httpd:
            print(f"Serving at http://localhost:{self.port}")
            httpd.serve_forever()

class ZeroHostApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ZeroHost - Yasdeity")
        self.root.geometry("500x300")
        self.root.configure(bg="#111111")

        self.selected_folder = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="ZeroHost", fg="#00FF00", bg="#111111", font=("Arial", 24, "bold")).pack(pady=10)

        frame = tk.Frame(self.root, bg="#111111")
        frame.pack(pady=10)

        tk.Entry(frame, textvariable=self.selected_folder, width=40).pack(side=tk.LEFT, padx=10)
        tk.Button(frame, text="Klasör Seç", command=self.select_folder).pack(side=tk.LEFT)

        self.port_entry = tk.Entry(self.root, width=10)
        self.port_entry.insert(0, "8080")
        self.port_entry.pack(pady=10)

        tk.Button(self.root, text="Yayını Başlat", command=self.start_server).pack(pady=10)

        self.link_label = tk.Label(self.root, text="", fg="cyan", bg="#111111")
        self.link_label.pack(pady=5)

        tk.Label(self.root, text="Geliştirici: yasdeity", fg="gray", bg="#111111", font=("Arial", 10)).pack(side=tk.BOTTOM, pady=10)

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.selected_folder.set(folder)

    def start_server(self):
        folder = self.selected_folder.get()
        port = int(self.port_entry.get())

        if not folder:
            messagebox.showerror("Hata", "Lütfen bir klasör seçin.")
            return

        try:
            thread = LocalServerThread(port, folder)
            thread.daemon = True
            thread.start()
            link = f"http://localhost:{port}"
            self.link_label.config(text=f"Yayın: {link}")
            webbrowser.open(link)
        except Exception as e:
            messagebox.showerror("Hata", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = ZeroHostApp(root)
    root.mainloop()
