import tkinter as tk
from tkinter import messagebox
import webbrowser
import threading
import time

class WebsiteManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Website Manager")

        self.websites = []  
        self.running = False  

        # UI Elements
        self.url_label = tk.Label(root, text="Enter URL:")
        self.url_label.grid(row=0, column=0, padx=10, pady=5)

        self.url_entry = tk.Entry(root, width=40)
        self.url_entry.grid(row=0, column=1, padx=10, pady=5)

        self.time_label = tk.Label(root, text="Enter Time (seconds):")
        self.time_label.grid(row=1, column=0, padx=10, pady=5)

        self.time_entry = tk.Entry(root, width=40)
        self.time_entry.grid(row=1, column=1, padx=10, pady=5)

        self.add_button = tk.Button(root, text="Add Website", command=self.add_website)
        self.add_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.website_listbox = tk.Listbox(root, width=60, height=10)
        self.website_listbox.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.edit_button = tk.Button(root, text="Edit Selected", command=self.edit_website)
        self.edit_button.grid(row=4, column=0, padx=10, pady=5)

        self.delete_button = tk.Button(root, text="Delete Selected", command=self.delete_website)
        self.delete_button.grid(row=4, column=1, padx=10, pady=5)

        self.start_button = tk.Button(root, text="Start", command=self.start_websites)
        self.start_button.grid(row=5, column=0, pady=10)

        self.stop_button = tk.Button(root, text="Stop", command=self.stop_websites)
        self.stop_button.grid(row=5, column=1, pady=10)

        self.about_button = tk.Button(root, text="About", command=self.show_about)
        self.about_button.grid(row=6, column=0, columnspan=2, pady=10)

    def add_website(self):
        url = self.url_entry.get().strip()
        try:
            timer = int(self.time_entry.get().strip())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid time in seconds.")
            return

        if not url:
            messagebox.showerror("Invalid Input", "URL cannot be empty.")
            return

        self.websites.append((url, timer))
        self.update_listbox()
        self.url_entry.delete(0, tk.END)
        self.time_entry.delete(0, tk.END)

    def edit_website(self):
        selected_index = self.website_listbox.curselection()
        if not selected_index:
            messagebox.showerror("No Selection", "Please select a website to edit.")
            return

        selected_index = selected_index[0]
        url, timer = self.websites[selected_index]

        self.url_entry.delete(0, tk.END)
        self.time_entry.delete(0, tk.END)
        self.url_entry.insert(0, url)
        self.time_entry.insert(0, str(timer))

        self.websites.pop(selected_index)
        self.update_listbox()

    def delete_website(self):
        selected_index = self.website_listbox.curselection()
        if not selected_index:
            messagebox.showerror("No Selection", "Please select a website to delete.")
            return

        selected_index = selected_index[0]
        self.websites.pop(selected_index)
        self.update_listbox()

    def update_listbox(self):
        self.website_listbox.delete(0, tk.END)
        for url, timer in self.websites:
            self.website_listbox.insert(tk.END, f"{url} - {timer} seconds")

    def open_website_loop(self, url, timer):
        while self.running:
            webbrowser.open(url)
            time.sleep(timer)

    def start_websites(self):
        if self.running:
            messagebox.showinfo("Already Running", "The loop is already running.")
            return

        self.running = True
        for url, timer in self.websites:
            threading.Thread(target=self.open_website_loop, args=(url, timer)).start()

    def stop_websites(self):
        if not self.running:
            messagebox.showinfo("Not Running", "The loop is not currently running.")
            return

        self.running = False

    def show_about(self):
        about_message = ("Built by Hamza Jadun\n"
                         "Visit: https://hamzajadun.github.io/about/")
        messagebox.showinfo("About", about_message)

if __name__ == "__main__":
    root = tk.Tk()
    app = WebsiteManagerApp(root)
    root.mainloop()
