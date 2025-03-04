import os
import yt_dlp as youtube_dl
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from ttkthemes import ThemedTk
import threading
import configparser
import logging
from datetime import datetime

# Configuração do logging
logging.basicConfig(filename='download_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

class YoutubeDownloader:
    def __init__(self):
        self.root = tk.Tk()  # Usaremos tk puro com estilo customizado, sem ttkthemes
        self.root.title("YouTube Downloader")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")  # Cinza claro típico do Windows 11
        
        self.config = configparser.ConfigParser()
        self.config_file = 'config.ini'
        self.load_config()
        
        self.download_cancelled = threading.Event()
        self.setup_ui()

    def load_config(self):
        if os.path.exists(self.config_file):
            self.config.read(self.config_file)
        if 'SETTINGS' not in self.config:
            self.config['SETTINGS'] = {'last_directory': ''}

    def save_config(self):
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

    def select_directory(self):
        directory = filedialog.askdirectory(initialdir=self.config['SETTINGS']['last_directory'])
        if directory:
            self.entry_dir.delete(0, tk.END)
            self.entry_dir.insert(0, directory)
            self.config['SETTINGS']['last_directory'] = directory
            self.save_config()

    def progress_function(self, d):
        if self.download_cancelled.is_set():
            raise Exception("Download cancelado pelo usuário")
        if d['status'] == 'downloading':
            try:
                percent = (d['downloaded_bytes'] / d['total_bytes']) * 100
                self.progress_bar["value"] = percent
                self.label_status.config(text=f"Progresso: {percent:.1f}%")
            except KeyError:
                pass
        self.root.update_idletasks()

    def verify_ffmpeg(self, path):
        return os.path.exists(path) and os.path.isfile(os.path.join(path, 'ffmpeg.exe'))

    def cancel_download(self):
        self.download_cancelled.set()
        self.button_download.config(state='normal')
        self.button_cancel.config(state='disabled')
        self.label_status.config(text="Download cancelado")

    def download_video(self):
        url = self.entry_url.get().strip()
        directory = self.entry_dir.get()
        
        if not url or not directory:
            messagebox.showwarning("Aviso", "Por favor, insira a URL e selecione o diretório.")
            return
        
        if not url.startswith(('http://', 'https://')):
            messagebox.showerror("Erro", "URL inválida")
            return

        ffmpeg_path = r"C:/ffmpeg/bin"
        if not self.verify_ffmpeg(ffmpeg_path):
            messagebox.showerror("Erro", "FFmpeg não encontrado em C:/ffmpeg/bin")
            return

        self.download_cancelled.clear()
        ydl_opts = {
            'outtmpl': os.path.join(directory, '%(playlist_title)s/%(title)s.%(ext)s'),
            'format': "bestvideo+bestaudio/best",
            'progress_hooks': [self.progress_function],
            'yesplaylist': True,
            'merge_output_format': 'mp4',
            'prefer_ffmpeg': True,
            'ffmpeg_location': os.path.join(ffmpeg_path, 'ffmpeg.exe'),
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
        }

        def download_thread():
            try:
                self.button_download.config(state='disabled')
                self.button_cancel.config(state='normal')
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                if not self.download_cancelled.is_set():
                    self.root.after(0, lambda: [
                        self.label_status.config(text="Download concluído!"),
                        self.button_download.config(state='normal'),
                        self.button_cancel.config(state='disabled')
                    ])
                    logging.info(f"Download concluído: {url}")
            except Exception as e:
                self.root.after(0, lambda: [
                    messagebox.showerror("Erro", f"Falha no download: {str(e)}"),
                    self.button_download.config(state='normal'),
                    self.button_cancel.config(state='disabled')
                ])

        self.progress_bar["value"] = 0
        self.label_status.config(text="Iniciando download...")
        threading.Thread(target=download_thread, daemon=True).start()

    def setup_ui(self):
        style = ttk.Style()
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabel", background="#f0f0f0", foreground="#1a1a1a", font=("Segoe UI", 11))
        style.configure("TEntry", fieldbackground="#ffffff", foreground="#1a1a1a", borderwidth=1, relief="solid")
        style.configure("TButton", font=("Segoe UI", 10), padding=6, background="#e1e1e1", relief="flat")
        style.map("TButton", background=[('active', '#cce4ff'), ('disabled', '#e1e1e1')], 
                 foreground=[('active', '#005fb8')], relief=[('active', 'flat')])
        style.configure("TProgressbar", troughcolor="#e0e0e0", background="#005fb8", thickness=10)

        # Container principal
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(expand=True, fill="both")

        # Título
        ttk.Label(main_frame, text="YouTube Downloader", font=("Segoe UI", 16, "bold")).pack(pady=(0, 20))

        # URL
        url_frame = ttk.Frame(main_frame)
        url_frame.pack(fill="x", pady=5)
        ttk.Label(url_frame, text="URL:").pack(side="left", padx=(0, 10))
        self.entry_url = ttk.Entry(url_frame, width=50)
        self.entry_url.pack(side="left", fill="x", expand=True)
        ttk.Label(main_frame, text="Cole a URL do vídeo ou playlist", font=("Segoe UI", 8)).pack()

        # Diretório
        dir_frame = ttk.Frame(main_frame)
        dir_frame.pack(fill="x", pady=5)
        ttk.Label(dir_frame, text="Destino:").pack(side="left", padx=(0, 10))
        self.entry_dir = ttk.Entry(dir_frame, width=40)
        self.entry_dir.insert(0, self.config['SETTINGS']['last_directory'])
        self.entry_dir.pack(side="left", fill="x", expand=True)
        ttk.Button(dir_frame, text="📁", command=self.select_directory, width=3).pack(side="left", padx=5)

        # Progresso
        self.progress_bar = ttk.Progressbar(main_frame, length=400, mode='determinate')
        self.progress_bar.pack(pady=20)

        # Botões
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        self.button_download = ttk.Button(button_frame, text="Download", command=self.download_video)
        self.button_download.pack(side="left", padx=5)
        self.button_cancel = ttk.Button(button_frame, text="Cancelar", command=self.cancel_download, state='disabled')
        self.button_cancel.pack(side="left", padx=5)

        # Status
        self.label_status = ttk.Label(main_frame, text="Pronto", font=("Segoe UI", 10))
        self.label_status.pack(pady=5)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = YoutubeDownloader()
    app.run()