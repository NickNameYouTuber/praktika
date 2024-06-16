import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import time
import threading
from parser import parse_logs
from viewer import view_logs
from db import setup_database, drop_database

class LogAggregatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Apache Log Aggregator")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.parse_interval = 10
        self.parser_thread = None
        self.stop_parsing = False

        self.create_widgets()
        self.start_parsing()

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.setup_button = ttk.Button(frame, text="Setup Database", command=self.setup_database)
        self.setup_button.grid(row=0, column=0, padx=5, pady=5)

        self.drop_button = ttk.Button(frame, text="Drop Database", command=self.drop_database)
        self.drop_button.grid(row=0, column=1, padx=5, pady=5)

        self.parse_button = ttk.Button(frame, text="Parse Logs", command=self.parse_logs)
        self.parse_button.grid(row=0, column=2, padx=5, pady=5)

        self.start_date_label = ttk.Label(frame, text="Start Date (YYYY-MM-DD):")
        self.start_date_label.grid(row=1, column=0, padx=5, pady=5)

        self.start_date_entry = ttk.Entry(frame)
        self.start_date_entry.grid(row=1, column=1, padx=5, pady=5)

        self.end_date_label = ttk.Label(frame, text="End Date (YYYY-MM-DD):")
        self.end_date_label.grid(row=2, column=0, padx=5, pady=5)

        self.end_date_entry = ttk.Entry(frame)
        self.end_date_entry.grid(row=2, column=1, padx=5, pady=5)

        self.filter_label = ttk.Label(frame, text="Filter:")
        self.filter_label.grid(row=3, column=0, padx=5, pady=5)

        self.filter_combobox = ttk.Combobox(frame, values=["None", "IP", "Status"])
        self.filter_combobox.grid(row=3, column=1, padx=5, pady=5)
        self.filter_combobox.current(0)

        self.filter_value_label = ttk.Label(frame, text="Filter Value:")
        self.filter_value_label.grid(row=4, column=0, padx=5, pady=5)

        self.filter_value_entry = ttk.Entry(frame)
        self.filter_value_entry.grid(row=4, column=1, padx=5, pady=5)

        self.view_button = ttk.Button(frame, text="View Logs", command=self.view_logs)
        self.view_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        self.log_text = tk.Text(frame, width=80, height=20)
        self.log_text.grid(row=8, column=0, columnspan=3, padx=5, pady=5)
        self.log_text.tag_configure("ip", foreground="blue")
        self.log_text.tag_configure("date", foreground="green")
        self.log_text.tag_configure("status_200", foreground="green")
        self.log_text.tag_configure("status_404", foreground="red")
        self.log_text.tag_configure("status_other", foreground="orange")

        self.interval_label = ttk.Label(frame, text="Parsing Interval (seconds):")
        self.interval_label.grid(row=6, column=0, padx=5, pady=5)

        self.interval_entry = ttk.Entry(frame)
        self.interval_entry.grid(row=6, column=1, padx=5, pady=5)
        self.interval_entry.insert(0, str(self.parse_interval))

        self.update_interval_button = ttk.Button(
            frame, text="Update Interval", command=self.update_parse_interval
        )
        self.update_interval_button.grid(row=6, column=2, padx=5, pady=5)

    def setup_database(self):
        setup_database()
        self.log_text.insert(tk.END, "Database setup completed.\n")

    def drop_database(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to drop the database? This action cannot be undone."):
            drop_database()
            self.log_text.insert(tk.END, "Database dropped.\n")

    def parse_logs(self):
        parse_logs()
        self.log_text.insert(tk.END, f"Log parsing completed at {time.ctime()}\n")
        self.log_text.see(tk.END)

    def update_parse_interval(self):
        try:
            new_interval = int(self.interval_entry.get())
            if new_interval > 0:
                self.parse_interval = new_interval
                self.log_text.insert(tk.END, f"Parsing interval updated to {self.parse_interval} seconds.\n")
            else:
                self.log_text.insert(tk.END, "Invalid interval. Please enter a positive number.\n")
        except ValueError:
            self.log_text.insert(tk.END, "Invalid interval. Please enter a number.\n")

    def start_parsing(self):
        self.stop_parsing = False
        self.parser_thread = threading.Thread(target=self.parsing_loop)
        self.parser_thread.start()

    def parsing_loop(self):
        while not self.stop_parsing:
            time.sleep(self.parse_interval)
            if not self.stop_parsing:
                self.parse_logs()

    def view_logs(self):
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()
        filter_type = self.filter_combobox.get().lower()
        filter_value = self.filter_value_entry.get()

        logs = view_logs(
            start_date if start_date else None,
            end_date if end_date else None,
            filter_type if filter_type != "none" else None,
            filter_value if filter_value else None
        )
        self.log_text.delete("1.0", tk.END)
        for log in logs:
            self.log_text.insert(tk.END, log[1], "ip")
            self.log_text.insert(tk.END, " - - ")
            self.log_text.insert(tk.END, f"[{log[2]}]", "date")
            self.log_text.insert(tk.END, f' "{log[3]}" ')
            status_tag = f"status_{log[4]}" if log[4] in (200, 404) else "status_other"
            self.log_text.insert(tk.END, log[4], status_tag)
            self.log_text.insert(tk.END, f" {log[5]}\n")

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit? Parsing will continue in the background."):
            self.stop_parsing = True
            self.root.destroy()

def start_gui():
    root = tk.Tk()
    app = LogAggregatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    start_gui()