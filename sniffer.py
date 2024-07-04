import tkinter as tk
from tkinter import ttk, scrolledtext
import time
import os
import platform
import urllib.request as connection
import sys
import subprocess

# GUI Application Class
class NetworkSnifferApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Domain/URL sniffer by @AuxGrep")

        self.search_count = 0  # Track the number of searches to alternate styles

        # Set full black theme
        self.configure_styles()

        # User Interface
        self.setup_ui()

        # Maximize the window
        self.root.state('zoomed')

        # Check OS Compatibility
        if not self.os_check(['Linux', 'Windows']):
            self.update_output("Unsupported OS", "error")

    def configure_styles(self):
        style = ttk.Style()
        style.theme_use('clam')  

        # General style configurations for all widgets
        style.configure('TLabel', background='#000000', foreground='#FFFFFF')
        style.configure('TEntry', background='#333333', foreground='#FFFFFF', fieldbackground='#333333', insertcolor='#FFFFFF')
        style.configure('TButton', background='#333333', foreground='#FFFFFF', borderwidth=1)
        style.map('TButton', background=[('active', '#555555')])
        style.configure('Horizontal.TProgressbar', background='#55FF55')
        style.configure('TFrame', background='#000000')

    def setup_ui(self):
        # Frame for URL Entry and Buttons
        self.frame = ttk.Frame(self.root)
        self.frame.pack(padx=10, pady=10, fill=tk.X, expand=False)

        # URL Entry
        self.url_label = ttk.Label(self.frame, text="Enter Target Domain:")
        self.url_label.pack(side=tk.LEFT, padx=5)
        self.url_entry = ttk.Entry(self.frame, width=40)
        self.url_entry.pack(side=tk.LEFT, expand=True, padx=5)

        # Start Button
        self.start_button = ttk.Button(self.frame, text="Start", command=self.start_sniffing)
        self.start_button.pack(side=tk.RIGHT, padx=5)

        # Clear Button
        self.clear_button = ttk.Button(self.frame, text="Clear", command=self.clear_output)
        self.clear_button.pack(side=tk.RIGHT, padx=5)

        # Progress Bar
        self.progress = ttk.Progressbar(self.root, orient='horizontal', length=400, mode='indeterminate')
        self.progress.pack(padx=10, pady=10, fill=tk.X)

        # Scrolled Text Output
        self.output_text = scrolledtext.ScrolledText(self.root, height=10, wrap=tk.WORD, bg='#000000', fg='#FFFFFF', insertbackground='#FFFFFF', selectbackground='#FFA500', selectforeground='#000000')
        self.output_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def start_sniffing(self):
        target_url = self.url_entry.get()
        if target_url:
            self.progress.start()
            hostname = self.extract_hostname(target_url)
            self.insert_separator(hostname)
            self.update_output(f"Starting to sniff: {target_url}", "info")
            self.root.after(100, self.perform_sniffing, target_url)
        else:
            self.update_output("Please enter a target domain(eg: google.com).", "error")

    def clear_output(self):
        self.output_text.delete('1.0', tk.END)

    def perform_sniffing(self, target_url):
        if self.net():
            limit = "/url_list?limit=200&page=1"
            try:
                result = subprocess.check_output(
                    f'curl -s "https://otx.alienvault.com/api/v1/indicators/domain/{target_url}{limit}" | jq -r .url_list[].url',
                    shell=True,
                    stderr=subprocess.STDOUT
                ).decode()
                self.update_output(result, "info")
                # Insert completion line after fetching
                self.insert_completion_line(target_url)  
            except subprocess.CalledProcessError as e:
                self.update_output(f"Error during sniffing: {e.output.decode()}", "error")
            finally:
                self.progress.stop()
        else:
            self.update_output("Please connect your PC to the internet.", "error")

    def extract_hostname(self, url):
        from urllib.parse import urlparse
        parsed_url = urlparse(url)
        return parsed_url.netloc

    def insert_separator(self, hostname):
        self.search_count += 1
        color = '#FFA500' if self.search_count % 2 == 0 else '#55FF55'
        separator_text = f"\n{'=' * 20} Result for {hostname} {'=' * 20}\n"
        self.output_text.insert(tk.END, separator_text, 'separator')
        self.output_text.tag_configure('separator', foreground=color)

    def insert_completion_line(self, url):
        hostname = self.extract_hostname(url)
        completion_text = "Sniffing completed"
        self.output_text.insert(tk.END, completion_text + "\n", 'completion')
        self.output_text.tag_configure('completion', foreground='#00FF00')  

    def net(self):
        try:
            connection.urlopen('https://google.com')
            return True
        except:
            return False

    def os_check(self, supported_os):
        return platform.system() in supported_os

    def update_output(self, message, msg_type="info"):
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.yview(tk.END)

# Main Function to Run the Application
def main():
    root = tk.Tk()
    app = NetworkSnifferApp(root) #OG
    root.mainloop()

if __name__ == "__main__":
    main()
