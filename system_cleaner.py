#  the system cleaner the helps to clean temp files, recyling bins and chrome and browser caches.


import os
import shutil
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class SystemCleaner:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced System Cleaner")
        self.root.geometry("500x500")
        
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", font=("Helvetica", 12))
        self.style.configure("TLabel", font=("Helvetica", 12))
        self.style.configure("TEntry", font=("Helvetica", 12))
        
        self.label = ttk.Label(root, text="Advanced System Cleaner", font=("Helvetica", 18))
        self.label.pack(pady=20)
        
        self.dir_label = ttk.Label(root, text="Select Directory to Clean:")
        self.dir_label.pack(pady=5)
        
        self.dir_entry = ttk.Entry(root, width=50)
        self.dir_entry.pack(pady=5)
        
        self.browse_button = ttk.Button(root, text="Browse", command=self.browse_directory)
        self.browse_button.pack(pady=5)
        
        self.clean_button = ttk.Button(root, text="Clean System", command=self.clean_system)
        self.clean_button.pack(pady=10)
        
        self.progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=10)
        
        self.status_label = ttk.Label(root, text="", font=("Helvetica", 12))
        self.status_label.pack(pady=10)
        
        self.log_text = tk.Text(root, height=15, width=60, state='disabled')
        self.log_text.pack(pady=10)
        
    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, directory)
        
    def log_message(self, message):
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + '\n')
        self.log_text.config(state='disabled')
        self.log_text.see(tk.END)
        
    def clean_system(self):
        try:
            self.status_label.config(text="Cleaning in progress...")
            self.root.update_idletasks()
            self.progress.start(10)
            
        #    temp file clean using this function
            temp_dir = os.environ.get('TEMP', '/tmp')
            if os.path.exists(temp_dir):
                self.clean_directory(temp_dir)
                
            # Windows Prefetch folder clean
            prefetch_dir = 'C:\\Windows\\Prefetch'
            if os.path.exists(prefetch_dir):
                self.clean_directory(prefetch_dir)
            
            # Clean browser cache
            self.clean_browser_cache()
            
            # Clean Recycle Bin but there is security issue so that might be not functioning
            recycle_bin = 'C:\\$Recycle.Bin'
            if os.path.exists(recycle_bin):
                self.clean_directory(recycle_bin)
            
            # Clean selected folder and delete it.
            directory = self.dir_entry.get()
            if directory and os.path.exists(directory):
                self.clean_directory(directory)
            
            self.progress.stop()
            self.status_label.config(text="Cleaning completed!")
            messagebox.showinfo("Info", "System cleaning completed successfully.")
        except Exception as e:
            self.progress.stop()
            self.status_label.config(text="Cleaning failed!")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def clean_directory(self, directory):
        for root, dirs, files in os.walk(directory, topdown=False):
            for name in files:
                file_path = os.path.join(root, name)
                try:
                    os.remove(file_path)
                    self.log_message(f"Deleted file: {file_path}")
                except Exception as e:
                    self.log_message(f"Could not delete file {file_path}: {e}")
            for name in dirs:
                dir_path = os.path.join(root, name)
                try:
                    shutil.rmtree(dir_path)
                    self.log_message(f"Deleted directory: {dir_path}")
                except Exception as e:
                    self.log_message(f"Could not delete directory {dir_path}: {e}")
        try:
            os.rmdir(directory)
            self.log_message(f"Deleted directory: {directory}")
        except Exception as e:
            self.log_message(f"Could not delete directory {directory}: {e}")

    def clean_browser_cache(self):
      
        chrome_cache = os.path.expanduser('~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cache')
        if os.path.exists(chrome_cache):
            self.clean_directory(chrome_cache)
        
        firefox_cache = os.path.expanduser('~\\AppData\\Local\\Mozilla\\Firefox\\Profiles')
        if os.path.exists(firefox_cache):
            for profile in os.listdir(firefox_cache):
                cache_path = os.path.join(firefox_cache, profile, 'cache2')
                if os.path.exists(cache_path):
                    self.clean_directory(cache_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = SystemCleaner(root)
    root.mainloop()



#  made by Jai ghai