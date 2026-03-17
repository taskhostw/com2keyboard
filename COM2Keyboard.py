import serial
import keyboard
import tkinter as tk
from tkinter import messagebox
import threading
import serial.tools.list_ports
import pystray
from PIL import Image, ImageDraw
import customtkinter as ctk


class BarkodOkuyucu:
    def __init__(self, root):
        self.root = root
        self.root.title("Barkod Okuyucu - COM to Keyboard")
        self.root.geometry("600x600")
        self.root.minsize(600, 600)
        self.root.protocol("WM_DELETE_WINDOW", self.pencere_kapatma_istegi)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        ctk.set_widget_scaling(1.1)
        ctk.set_window_scaling(1.1)

        self.create_tray_icon()
        self.serial_port = None
        self.is_running = False
        self.enter_aktif = False
        self.close_warning_shown = False
        self.tray_thread_started = False

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.main_frame = ctk.CTkFrame(self.root, corner_radius=14)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.main_frame.grid_rowconfigure(4, weight=1)

        self.port_label = ctk.CTkLabel(self.main_frame, text="COM Port:")
        self.port_label.grid(column=0, row=0, padx=12, pady=(16, 10), sticky="w")

        self.port_combobox = ctk.CTkComboBox(self.main_frame, width=240, values=[])
        self.port_combobox.grid(column=1, row=0, padx=12, pady=(16, 10), sticky="ew")

        self.port_tara_button = ctk.CTkButton(self.main_frame, text="Port Tara", command=self.port_tara)
        self.port_tara_button.grid(column=2, row=0, padx=12, pady=(16, 10), sticky="ew")

        self.baudrate_label = ctk.CTkLabel(self.main_frame, text="Baudrate:")
        self.baudrate_label.grid(column=0, row=1, padx=12, pady=10, sticky="w")

        self.baudrate_entry = ctk.CTkEntry(self.main_frame, width=240)
        self.baudrate_entry.grid(column=1, row=1, padx=12, pady=10, sticky="ew")
        self.baudrate_entry.insert(0, "9600")

        self.connect_button = ctk.CTkButton(self.main_frame, text="Bağlan", command=self.baglan)
        self.connect_button.grid(column=0, row=2, padx=12, pady=10, sticky="ew")

        self.disconnect_button = ctk.CTkButton(self.main_frame, text="Bağlantıyı Kes", command=self.baglanti_kes, state="disabled")
        self.disconnect_button.grid(column=1, row=2, padx=12, pady=10, sticky="ew")

        self.tray_button = ctk.CTkButton(
            self.main_frame,
            text="Sistem Tepsisine Al",
            command=self.tepsiye_al
        )
        self.tray_button.grid(column=2, row=2, padx=12, pady=10, sticky="ew")

        self.enter_button = ctk.CTkButton(
            self.main_frame,
            text="Enter: PASİF",
            command=self.enter_aktif_pasif,
            fg_color="#b42318",
            hover_color="#912018",
            text_color="#ffe4e6"
        )
        self.enter_button.grid(column=0, row=3, columnspan=3, padx=12, pady=10, sticky="ew")

        self.output_area = ctk.CTkTextbox(self.main_frame, wrap="word")
        self.output_area.grid(column=0, row=4, columnspan=3, padx=12, pady=12, sticky="nsew")

        self.footer_label = ctk.CTkLabel(
            self.main_frame,
            text="taskhostw - mail@behcet.tr",
            text_color="gray80",
            font=ctk.CTkFont(size=12, slant="italic")
        )
        self.footer_label.grid(column=0, row=5, columnspan=3, pady=(4, 14))

        self.port_tara()

    def create_tray_icon(self):
        self.icon_image = Image.new('RGBA', (64, 64), (255, 255, 255, 0))
        d = ImageDraw.Draw(self.icon_image)
        d.ellipse((16, 16, 48, 48), fill=(255, 0, 0))
        self.tray_icon = pystray.Icon(
            "Barkod Okuyucu",
            self.icon_image,
            menu=pystray.Menu(
                pystray.MenuItem("Göster", self.pencere_goster, default=True),
                pystray.MenuItem("Çıkış", self.cikis)
        ))

    def update_tray_icon(self, color):
        icon_image = Image.new('RGBA', (64, 64), (255, 255, 255, 0))
        d = ImageDraw.Draw(icon_image)
        d.ellipse((16, 16, 48, 48), fill=color)
        self.icon_image = icon_image
        self.tray_icon.icon = self.icon_image

    def log_yaz(self, mesaj):
        self.root.after(0, lambda: self._log_yaz_ui(mesaj))

    def _log_yaz_ui(self, mesaj):
        self.output_area.insert("end", mesaj)
        self.output_area.see("end")

    def port_tara(self):
        ports = [port.device for port in serial.tools.list_ports.comports()]
        self.port_combobox.configure(values=ports)
        if ports:
            self.port_combobox.set(ports[0])
            if len(ports) > 1:
                messagebox.showinfo("Uyarı", "Birden fazla COM port bulundu. Varsayılan olarak ilk port seçildi.")
        else:
            self.port_combobox.set("")

    def baglan(self):
        port = self.port_combobox.get()
        baudrate = self.baudrate_entry.get()

        if not port:
            messagebox.showerror("Hata", "Lütfen bir COM portu seçin.")
            return

        try:
            baudrate = int(baudrate)
            self.serial_port = serial.Serial(
                port=port,
                baudrate=baudrate,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=0.1
            )
            self.is_running = True
            threading.Thread(target=self.veri_okuma, daemon=True).start()
            self.connect_button.configure(state="disabled")
            self.disconnect_button.configure(state="normal")
            self.update_tray_icon((0, 200, 0, 255))
            self.log_yaz(f"{port} portuna bağlandı. Veri bekleniyor...\n")
        except ValueError:
            messagebox.showerror("Hata", "Geçersiz baudrate değeri. Lütfen sayısal bir değer girin.")
        except serial.SerialException as e:
            messagebox.showerror("Hata", f"Seri port hatası: {e}")
        except Exception as e:
            messagebox.showerror("Hata", f"Beklenmeyen bir hata oluştu: {e}")

    def baglanti_kes(self):
        self.is_running = False
        if self.serial_port:
            self.serial_port.close()
            self.serial_port = None
        self.connect_button.configure(state="normal")
        self.disconnect_button.configure(state="disabled")
        self.update_tray_icon((220, 38, 38, 255))
        self.log_yaz("Bağlantı kesildi.\n")

    def veri_okuma(self):
        while self.is_running and self.serial_port:
            try:
                if self.serial_port.in_waiting > 0:
                    data = self.serial_port.readline().decode('utf-8', errors='ignore').strip()
                    if data:
                        self.log_yaz(f"Gelen Veri: {data}\n")
                        if self.enter_aktif:
                            keyboard.write(data + '\n')
                        else:
                            keyboard.write(data)
            except Exception as e:
                self.log_yaz(f"Hata: {e}\n")
                self.baglanti_kes()

    def enter_aktif_pasif(self):
        self.enter_aktif = not self.enter_aktif
        if self.enter_aktif:
            self.enter_button.configure(
                text="Enter: AKTİF",
                fg_color="#15803d",
                hover_color="#166534",
                text_color="#f0fdf4"
            )
        else:
            self.enter_button.configure(
                text="Enter: PASİF",
                fg_color="#b42318",
                hover_color="#912018",
                text_color="#ffe4e6"
            )

    def pencere_kapatma_istegi(self):
        if not self.close_warning_shown:
            messagebox.showinfo(
                "Bilgilendirme",
                "Uygulama sistem tepsisine alındı.\n"
                "Tam kapatmak için tepsi ikonuna sağ tıklayıp 'Çıkış' seçeneğini kullanın."
            )
            self.close_warning_shown = True
        self.tepsiye_al()

    def tepsiye_al(self):
        self.root.withdraw()
        self._tepsi_thread_baslat()

    def _tepsi_thread_baslat(self):
        if self.tray_thread_started:
            return

        def _run_tray_icon():
            try:
                self.tray_icon.run()
            finally:
                self.tray_thread_started = False

        self.tray_thread_started = True
        threading.Thread(target=_run_tray_icon, daemon=True).start()

    def pencere_goster(self, icon, item):
        self.root.after(0, self.root.deiconify)

    def cikis(self, icon, item):
        self.tray_icon.stop()
        self.root.after(0, self.root.destroy)


if __name__ == "__main__":
    root = ctk.CTk()
    app = BarkodOkuyucu(root)
    root.mainloop()