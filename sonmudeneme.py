import psutil
import wmi
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import sqlite3
from datetime import datetime
import time
class Proje:
    @staticmethod
    def get_ram_percent():
        return psutil.virtual_memory().percent

    @staticmethod
    def get_cpu_percent():
        c = wmi.WMI()
        cpu_info = c.Win32_PerfFormattedData_PerfOS_Processor()[0]
        idle_percentage = float(cpu_info.PercentIdleTime)
        return 100.0 - idle_percentage

    @staticmethod
    def plot_pie_chart(used_percent, free_percent, ax, title):
        labels = 'Kullanılan', 'Boş'
        sizes = [used_percent, free_percent]
        colors = ['r', 'b']
        explode = (0.1, 0)

        ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
        ax.axis('equal')
        ax.set_title(title)

    @staticmethod
    def create_table_if_not_exists():
        try:

            connection = sqlite3.connect('system_monitor.db')
            cursor = connection.cursor()


            cursor.execute('''
                CREATE TABLE IF NOT EXISTS system_monitor (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT,
                    percent REAL,
                    timestamp TEXT
                )
            ''')


            connection.commit()

        except sqlite3.Error as e:
            print(f"Hata: {e}")

        finally:
            if connection:
                connection.close()

    @staticmethod
    def reset_table():
        try:

            connection = sqlite3.connect('system_monitor.db')
            cursor = connection.cursor()


            cursor.execute('DROP TABLE IF EXISTS system_monitor')


            Proje.create_table_if_not_exists()


            connection.commit()

        except sqlite3.Error as e:
            print(f"Hata: {e}")

        finally:

            if connection:
                connection.close()


class RAMPage(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("RAM Ekranı")
        self.configure(bg='lightgray')

        frame = tk.Frame(self, bg='lightgray')
        frame.pack(fill=tk.BOTH, expand=True)

        fig, ax = plt.subplots()
        self.ram_canvas = FigureCanvasTkAgg(fig, master=frame)
        self.ram_canvas_widget = self.ram_canvas.get_tk_widget()
        self.ram_canvas_widget.pack(fill=tk.BOTH, expand=True)

        self.is_monitoring_ram = False
        self.update_ram_labels()

    def update_ram_labels(self):
        Proje.create_table_if_not_exists()

        used_percent = Proje.get_ram_percent()
        free_percent = 100 - used_percent


        SQL.insert_data_to_sqlite("ram", used_percent)

        self.ram_canvas.figure.clear()
        Proje.plot_pie_chart(used_percent, free_percent, self.ram_canvas.figure.gca(), "RAM Kullanımı")
        self.ram_canvas.draw()

        self.after(1000, self.update_ram_labels)


class CPUPage(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("CPU Ekranı")
        self.configure(bg='lightgray')

        frame = tk.Frame(self, bg='lightgray')
        frame.pack(fill=tk.BOTH, expand=True)

        fig, ax = plt.subplots()
        self.cpu_canvas = FigureCanvasTkAgg(fig, master=frame)
        self.cpu_canvas_widget = self.cpu_canvas.get_tk_widget()
        self.cpu_canvas_widget.pack(fill=tk.BOTH, expand=True)

        self.is_monitoring_cpu = False
        self.update_cpu_labels()

    def update_cpu_labels(self):
        Proje.create_table_if_not_exists()

        cpu_percent = Proje.get_cpu_percent()

        SQL.insert_data_to_sqlite("cpu", cpu_percent)

        self.cpu_canvas.figure.clear()
        Proje.plot_pie_chart(cpu_percent, 100 - cpu_percent, self.cpu_canvas.figure.gca(), "CPU Kullanımı")
        self.cpu_canvas.draw()

        self.after(1000, self.update_cpu_labels)

class SQL:

    def insert_data_to_sqlite(category, percent):
        try:
            # SQLite veritabanına bağlan
            connection = sqlite3.connect('system_monitor.db')
            cursor = connection.cursor()


            insert_query = "INSERT INTO system_monitor (category, percent, timestamp) VALUES (?, ?, ?)"
            data = (category, percent, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            cursor.execute(insert_query, data)


            connection.commit()

        except sqlite3.Error as e:
            print(f"Hata: {e}")

        finally:

            if connection:
                connection.close()


class RAMCPUApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Monitor")
        root.geometry("400x300")
        self.root.configure(bg='blue')

        ram_button = ttk.Button(root, text="RAM Göster", command=self.show_ram_page)
        ram_button.pack(pady=50)

        cpu_button = ttk.Button(root, text="CPU Göster", command=self.show_cpu_page)
        cpu_button.pack(pady=75)

    def show_ram_page(self):
        ram_page = RAMPage(self.root)
        ram_page.is_monitoring_ram = True

    def show_cpu_page(self):
        cpu_page = CPUPage(self.root)
        cpu_page.is_monitoring_cpu = True


def main():
    Proje.reset_table()
    Proje.create_table_if_not_exists()

    root = tk.Tk()
    app = RAMCPUApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
