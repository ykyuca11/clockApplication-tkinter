import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import winsound

class SaatUygulamasi:
    def __init__(self, root):
        self.root = root
        self.root.title("Saat Uygulaması")
        self.root.geometry("800x500")

        notebook = ttk.Notebook(root)
        notebook.pack(expand=True, fill="both")

        self.saat_frame = ttk.Frame(notebook)
        self.sayac_frame = ttk.Frame(notebook)
        self.sureolcer_frame = ttk.Frame(notebook)
        self.zamanlayici_frame = ttk.Frame(notebook)

        notebook.add(self.saat_frame, text="Mevcut Saat")
        notebook.add(self.sayac_frame, text="Sayaç")
        notebook.add(self.sureolcer_frame, text="Süreölçer")
        notebook.add(self.zamanlayici_frame, text="Zamanlayıcı")

        self.setup_saat()
        self.setup_sayac()
        self.setup_sureolcer()
        self.setup_zamanlayici()

    def setup_saat(self):
        self.mevcut_saat_label = tk.Label(self.saat_frame, text="", font=("Helvetica", 24))
        self.mevcut_saat_label.pack(pady=20)
        self.guncelle_mevcut_saat()

    def setup_sayac(self):
        self.sayac_label = tk.Label(self.sayac_frame, text="Sayaç: 00:00", font=("Helvetica", 24))
        self.sayac_label.pack(pady=20)
        self.sayac_giris = tk.Entry(self.sayac_frame, width=10, font=("Helvetica", 24))
        self.sayac_giris.pack(pady=10)
        self.sayac_button = tk.Button(self.sayac_frame, text="Sayaç Ayarla", command=self.sayac_ayarla, font=("Helvetica", 24))
        self.sayac_button.pack(pady=10)
        self.sayac_durdur_button = tk.Button(self.sayac_frame, text="Sayaç Durdur", command=self.sayac_durdur, font=("Helvetica", 24))
        self.sayac_durdur_button.pack(pady=10)

    def setup_sureolcer(self):
        self.sureolcer_label = tk.Label(self.sureolcer_frame, text="Süreölçer: 00:00:00", font=("Helvetica", 24))
        self.sureolcer_label.pack(pady=20)
        self.sureolcer_button = tk.Button(self.sureolcer_frame, text="Süreölçeri Başlat/Durdur", command=self.sureolcer_baslat_durdur, font=("Helvetica", 24))
        self.sureolcer_button.pack(pady=10)

    def setup_zamanlayici(self):
        self.zamanlayici_label = tk.Label(self.zamanlayici_frame, text="Zamanlayıcı: 00:00", font=("Helvetica", 24))
        self.zamanlayici_label.pack(pady=20)
        self.zamanlayici_giris_saat = tk.Entry(self.zamanlayici_frame, width=5, font=("Helvetica", 24))
        self.zamanlayici_giris_saat.pack(pady=5)
        self.zamanlayici_giris_dakika = tk.Entry(self.zamanlayici_frame, width=5, font=("Helvetica", 24))
        self.zamanlayici_giris_dakika.pack(pady=5)
        self.zamanlayici_button = tk.Button(self.zamanlayici_frame, text="Zamanlayıcı Ayarla", command=self.zamanlayici_ayarla, font=("Helvetica", 24))
        self.zamanlayici_button.pack(pady=10)
        self.zamanlayici_durdur_button = tk.Button(self.zamanlayici_frame, text="Zamanlayıcıyı Durdur", command=self.zamanlayici_durdur, font=("Helvetica", 24))
        self.zamanlayici_durdur_button.pack(pady=10)

    def guncelle_mevcut_saat(self):
        now = datetime.now().strftime("%H:%M:%S")
        self.mevcut_saat_label.config(text=f"Mevcut Saat: {now}")
        self.root.after(1000, self.guncelle_mevcut_saat)

    def sayac_ayarla(self):
        try:
            self.sayac_value = int(self.sayac_giris.get())
            self.sayac_durumu = True
            self.sayac_baslat()
        except ValueError:
            pass

    def sayac_baslat(self):
        if self.sayac_durumu and self.sayac_value > 0:
            self.sayac_value -= 1
            self.sayac_label.config(text=f"Sayaç: {str(timedelta(seconds=self.sayac_value))}")
            self.root.after(1000, self.sayac_baslat)
        else:
            self.sayac_label.config(text="Sayaç: Süre Doldu")
            winsound.Beep(1000, 1000)  # Beep sound with frequency 1000 Hz for 1000 ms

    def sayac_durdur(self):
        self.sayac_durumu = False
        self.sayac_label.config(text="Sayaç: Durduruldu")

    def sureolcer_baslat_durdur(self):
        if not self.sureolcer_frame:
            self.sureolcer_baslangic_zamani = datetime.now()
            self.sureolcer_frame = True
            self.sureolcer_guncelle()
        else:
            self.sureolcer_frame = False

    def sureolcer_guncelle(self):
        if self.sureolcer_frame:
            sure = datetime.now() - self.sureolcer_baslangic_zamani
            self.sureolcer_label.config(text=f"Süreölçer: {str(sure).split('.')[0]}")
            self.root.after(1000, self.sureolcer_guncelle)

    def zamanlayici_ayarla(self):
        try:
            saat = int(self.zamanlayici_giris_saat.get())
            dakika = int(self.zamanlayici_giris_dakika.get())
            self.zamanlayici_hedef = datetime.now().replace(hour=saat, minute=dakika, second=0, microsecond=0)
            if self.zamanlayici_hedef < datetime.now():
                self.zamanlayici_hedef += timedelta(days=1)
            self.zamanlayici_durumu = True
            self.zamanlayici_baslat()
        except ValueError:
            pass

    def zamanlayici_baslat(self):
        if self.zamanlayici_durumu:
            kalan_sure = self.zamanlayici_hedef - datetime.now()
            self.zamanlayici_label.config(text=f"Zamanlayıcı: {str(kalan_sure).split('.')[0]}")
            if kalan_sure.total_seconds() > 0:
                self.root.after(1000, self.zamanlayici_baslat)
            else:
                self.zamanlayici_label.config(text="Zamanlayıcı: Süre Doldu")
                self.zamanlayici_durumu = False
                winsound.Beep(1000, 1000)  # Beep sound with frequency 1000 Hz for 1000 ms

    def zamanlayici_durdur(self):
        self.zamanlayici_durumu = False
        self.zamanlayici_label.config(text="Zamanlayıcı: Durduruldu")

if __name__ == "__main__":
    root = tk.Tk()
    app = SaatUygulamasi(root)
    root.mainloop()

#
