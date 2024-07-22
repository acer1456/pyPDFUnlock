import unlock_password as up
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
from tkinter import Toplevel
import threading
import queue
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath("./assets")

    return os.path.join(base_path, relative_path)

def truncate_text(text, max_length):
    if len(text) > max_length:
        return text[:max_length-3] + '...'
    else:
        return text

def select_files():
    filepaths = filedialog.askopenfilenames(title="選擇文件")
    if filepaths:
        for filepath in filepaths:
            if filepath not in file_list:
                file_list.append(filepath)
                add_file_to_listbox(filepath)

def add_file_to_listbox(filepath):
    frame = ttk.Frame(listbox_frame)
    frame.pack(fill=ttk.X, pady=2, padx=5)

    label = ttk.Label(frame, text=truncate_text(filepath.split('/')[-1], 35), anchor="w", width=50)
    label.pack(side=ttk.LEFT, fill=ttk.X, expand=False, padx=5)

    delete_button = ttk.Button(frame, text="刪除", command=lambda: delete_item(frame, filepath), bootstyle=DANGER)
    delete_button.pack(side=ttk.RIGHT, padx=5)

def delete_item(frame, filepath):
    frame.destroy()
    file_list.remove(filepath)

def process_files():
    progress['maximum'] = len(file_list)
    for i, filepath in enumerate(file_list):
        #解開PDF
        up.crack(filepath, filepath.replace('.pdf', 'crack.pdf'))
        # print('DONE', filepath)
        percent = (i + 1) / len(file_list) * 100
        progress_label.config(text=f"{percent:.2f}%")
        progress['value'] = i + 1
        root.update_idletasks()
    q.put("done")

def start_processing():
    if len(file_list) == 0:
        messagebox.showerror("錯誤", "目前沒有待處理的文件！")
    else:
        progress_frame.pack(pady=10)
        processing_thread = threading.Thread(target=process_files)
        processing_thread.start()
        root.after(100, check_queue)

def check_queue():
    try:
        message = q.get_nowait()
        if message == "done":
            messagebox.showinfo("完成", "所有文件已處理完成！")
            progress_frame.pack_forget()
            # listbox_frame.destroy()
            # listbox_frame.update_idletasks()
            # root.update_idletasks()
    except queue.Empty:
        root.after(100, check_queue)

current_version = 'v0.1'

# 創建主窗口
root = ttk.Window(themename="darkly")
# 设置窗口图标
root.iconbitmap(resource_path("icon.icns"))  
root.title("PDF解鎖 "+ current_version)
root.geometry("600x400")

file_list = []

# 創建選擇文件按鈕
select_button = ttk.Button(root, text="選擇文件", command=select_files, bootstyle=PRIMARY)
select_button.pack(pady=10)

# 創建顯示文件列表的框架
listbox_frame = ttk.Frame(root)
listbox_frame.pack(pady=20, fill=ttk.BOTH, expand=True, padx=10)

# 創建處理文件按鈕
process_button = ttk.Button(root, text="解鎖文件", command=start_processing, bootstyle=SUCCESS)
process_button.pack(pady=10)

# # 創建進度條
# progress = ttk.Progressbar(root, orient=ttk.HORIZONTAL, length=400, mode="determinate", bootstyle=INFO)
# progress.pack_forget()
# progress_label = ttk.Label(root, text="0%", bootstyle=INFO)

# 創建進度條和百分比標籤的框架
progress_frame = ttk.Frame(root)
progress_frame.pack_forget()  # 初始化時隱藏

# 創建進度條
progress = ttk.Progressbar(progress_frame, orient=ttk.HORIZONTAL, length=300, mode="determinate", bootstyle=INFO)
progress.pack(side=LEFT, padx=5)

# 創建進度百分比標籤
progress_label = ttk.Label(progress_frame, text="0%", bootstyle=INFO)
progress_label.pack(side=LEFT)

# 創建隊列
q = queue.Queue()

# 運行主循環
root.mainloop()