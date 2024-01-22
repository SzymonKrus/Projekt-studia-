import tkinter as tk
from tkinter import ttk
import psutil
import os
import threading
import time
import tkinter.filedialog


class SystemMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("System Monitor")

        self.tabControl = ttk.Notebook(root)

        self.tab1 = ttk.Frame(self.tabControl)
        self.tab2 = ttk.Frame(self.tabControl)
        self.tab3 = ttk.Frame(self.tabControl)
        self.tab4 = ttk.Frame(self.tabControl)
        self.tab5 = ttk.Frame(self.tabControl)
        self.tab6 = ttk.Frame(self.tabControl)

        self.tabControl.add(self.tab1, text='Monitor Procesów')
        self.tabControl.add(self.tab2, text='Analiza Pamięci')
        self.tabControl.add(self.tab3, text='Eksplorator Systemu Plików')
        self.tabControl.add(self.tab4, text='Monitor Wejścia-Wyjścia')
        self.tabControl.add(self.tab5, text='Analiza Aktywności Sieciowej')
        self.tabControl.add(self.tab6, text='Konta Użytkowników')

        self.tabControl.pack(expand=1, fill="both")

        self.create_monitor_procesow_tab()
        self.create_analiza_pamieci_tab()
        self.create_eksplorator_systemu_plikow_tab()
        self.create_monitor_wejscia_wyjscia_tab()
        self.create_analiza_aktywnosci_sieciowej_tab()
        self.create_konta_uzytkownikow_tab()

    def create_monitor_procesow_tab(self):
        self.tree = ttk.Treeview(self.tab1, columns=('ID Procesu', 'Zużycie CPU (%)', 'Zużycie Pamięci (MB)'))
        self.tree.heading('#0', text='Nazwa Procesu')
        self.tree.heading('ID Procesu', text='ID Procesu')
        self.tree.heading('Zużycie CPU (%)', text='Zużycie CPU (%)')
        self.tree.heading('Zużycie Pamięci (MB)', text='Zużycie Pamięci (MB)')
        self.tree.pack(expand=True, fill="both")
        self.update_monitor_procesow()

    def update_monitor_procesow(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        cpu_percentages = psutil.cpu_percent(interval=None, percpu=True)

        for proc in psutil.process_iter(['pid', 'cpu_percent', 'memory_info', 'name']):
            try:
                name = proc.info['name'] or 'N/A'
                pid = proc.info['pid']

                cpu_percent = cpu_percentages[pid] if pid < len(cpu_percentages) else 0.0

                memory_usage = proc.info['memory_info'].rss / (1024 * 1024)
                self.tree.insert("", 'end', text=name, values=(pid, f"{cpu_percent:.0f}", f"{memory_usage:.2f}"))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        self.root.after(1000, self.update_monitor_procesow)

    def create_analiza_pamieci_tab(self):
        self.memory_label = ttk.Label(self.tab2, text="")
        self.memory_label.pack(expand=True, fill="both")
        self.update_analiza_pamieci()

    def update_analiza_pamieci(self):
        memory_info = psutil.virtual_memory()
        swap_info = psutil.swap_memory()
        memory_text = "Zużycie pamięci operacyjnej: {}%\nZużycie pamięci wirtualnej: {}%".format(memory_info.percent, swap_info.percent)
        self.memory_label.config(text=memory_text)
        self.root.after(1000, self.update_analiza_pamieci)

    def create_eksplorator_systemu_plikow_tab(self):
        self.folder_path_entry = ttk.Entry(self.tab3)
        self.folder_path_entry.pack(side="left", expand=True, fill="both")
        self.explore_button = ttk.Button(self.tab3, text="Przeglądaj", command=self.explore_folder)
        self.explore_button.pack(side="right", expand=True, fill="both")

        self.file_tree = ttk.Treeview(self.tab3, columns=('Typ', 'Rozmiar (MB)'))
        self.file_tree.heading('#0', text='Plik/Folder')
        self.file_tree.heading('Typ', text='Typ')
        self.file_tree.heading('Rozmiar (MB)', text='Rozmiar (MB)')
        self.file_tree.pack(expand=True, fill="both")

        self.file_tree.bind("<Double-1>", self.on_double_click)

    def explore_folder(self):
        path = tkinter.filedialog.askdirectory()
        if path:
            self.folder_path_entry.delete(0, 'end')
            self.folder_path_entry.insert(0, path)
            self.update_explorer_tree(path)

    def update_explorer_tree(self, path):
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)

        try:
            files = os.listdir(path)
            for item in files:
                full_path = os.path.join(path, item)
                file_type = 'Folder' if os.path.isdir(full_path) else 'Plik'
                file_size = "{:.1f}".format(os.path.getsize(full_path) / (1024 ** 2)) if os.path.isfile(full_path) else 'N/A'
                self.file_tree.insert("", 'end', text=item, values=(file_type, file_size))
        except FileNotFoundError:
            print("Podana ścieżka nie istnieje.")

    def on_double_click(self, event):
        item = self.file_tree.selection()[0]
        path = os.path.join(self.folder_path_entry.get(), item)
        if os.path.isdir(path):
            self.update_explorer_tree(path)
            self.folder_path_entry.delete(0, 'end')
            self.folder_path_entry.insert(0, path)

    def create_monitor_wejscia_wyjscia_tab(self):
        self.io_label = ttk.Label(self.tab4, text="")
        self.io_label.pack(expand=True, fill="both")
        self.update_monitor_wejscia_wyjscia()

    def update_monitor_wejscia_wyjscia(self):
        io_counters = psutil.disk_io_counters()
        io_text = "Odczyty z dysku: {:.2f} MB\nZapisy na dysk: {:.2f} MB".format(io_counters.read_bytes / (1024 ** 2), io_counters.write_bytes / (1024 ** 2))
        self.io_label.config(text=io_text)
        self.root.after(1000, self.update_monitor_wejscia_wyjscia)

    def create_analiza_aktywnosci_sieciowej_tab(self):
        self.connections_tree = ttk.Treeview(self.tab5, columns=('Adres lokalny', 'Adres zdalny', 'Stan'))
        self.connections_tree.heading('#0', text='Proces')
        self.connections_tree.heading('Adres lokalny', text='Adres lokalny')
        self.connections_tree.heading('Adres zdalny', text='Adres zdalny')
        self.connections_tree.heading('Stan', text='Stan')
        self.connections_tree.pack(expand=True, fill="both")
        self.update_analiza_aktywnosci_sieciowej()

    def update_analiza_aktywnosci_sieciowej(self):
        for item in self.connections_tree.get_children():
            self.connections_tree.delete(item)

        connections = psutil.net_connections()
        for conn in connections:
            self.connections_tree.insert("", 'end', text=conn.pid or "N/A", values=(conn.laddr, conn.raddr, conn.status))

        self.root.after(1000, self.update_analiza_aktywnosci_sieciowej)

    def create_konta_uzytkownikow_tab(self):
        self.users_tree = ttk.Treeview(self.tab6, columns=('Użytkownik', 'Terminal', 'Czas logowania'))
        self.users_tree.heading('#0', text='Indeks')
        self.users_tree.heading('Użytkownik', text='Użytkownik')
        self.users_tree.heading('Terminal', text='Terminal')
        self.users_tree.heading('Czas logowania', text='Czas logowania')
        self.users_tree.pack(expand=True, fill="both")
        self.update_konta_uzytkownikow()

    def update_konta_uzytkownikow(self):
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)

        users = psutil.users()
        for idx, user in enumerate(users):
            self.users_tree.insert("", 'end', text=idx, values=(user.name, user.terminal or "N/A", user.started))

        self.root.after(1000, self.update_konta_uzytkownikow)


def monitor_thread():
    while True:
        time.sleep(1)


def run_system_monitor_app():
    root = tk.Tk()
    root.geometry("800x600")
    app = SystemMonitorApp(root)
    monitor_thread_instance = threading.Thread(target=monitor_thread)
    monitor_thread_instance.daemon = True
    monitor_thread_instance.start()
    root.mainloop()


if __name__ == "__main__":
    run_system_monitor_app()
