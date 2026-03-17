# 🧾 Barkod Okuyucu (COM to Keyboard)

## 🇬🇧 English

Windows desktop application that reads barcode data from a serial port (COM) and types it into the active window as keyboard input.

### ✨ Features

- 🔎 Auto-scan and list available COM ports
- ⚙️ Configurable baud rate
- 🖥️ Real-time log output panel
- ⌨️ Sends incoming barcode text as keyboard input
- Enter mode:
  - **ACTIVE**: sends barcode text + Enter
  - **PASSIVE**: sends only barcode text
- 🧩 System tray support
- ℹ️ One-time info message on first window close (minimize-to-tray behavior)
- Tray menu actions:
  - **Show**: restore main window
  - **Exit**: fully close application
- 🖱️ Double-click tray icon to restore window

### 🧱 Project Structure

```text
Barkod Okuyucu/
├─ COM2Keyboard.py
├─ requirements.txt
├─ README.md
```

### 📌 Requirements

- Windows 10 / 11
- Python 3.10+
- A barcode scanner connected via COM/serial

### 🚀 Installation

1) Clone repository

```bash
git clone https://github.com/taskhostw/com2keyboard.git
cd "com2keyboard"
```

1) Create virtual environment (recommended)

```bash
python -m venv .venv
```

PowerShell activation:

```powershell
.\.venv\Scripts\Activate.ps1
```

1) Install dependencies

```bash
pip install -r requirements.txt
```

### ▶️ Run

```bash
python COM2Keyboard.py
```

You can also run the bundled executable `COM2Keyboard.exe`.

### 🧭 Usage

1. Open the app.
2. Click **Port Scan** (`Port Tara`).
3. Select a COM port.
4. Set baud rate if needed (default: `9600`).
5. Click **Connect** (`Bağlan`).
6. Scan a barcode.
7. Toggle Enter mode (`Enter: AKTİF/PASİF`) as needed.

### 🧩 Tray Behavior

- Clicking **System Tray** button hides the app to tray.
- Clicking window **X** does not exit; it minimizes to tray.
- On first close action, a one-time info dialog is shown.
- To fully exit, right-click tray icon and choose **Exit**.
- Double-click tray icon restores the window.

### 🛠️ Libraries

- `pyserial`
- `keyboard`
- `customtkinter`
- `pystray`
- `Pillow`

### 🧪 Troubleshooting

**COM port not visible**

- Verify the scanner is connected
- Check Device Manager for COM number
- Try running as administrator

**Data is received but not typed**

- Make sure target window is focused
- Security software may block keyboard hooks
- Try running as administrator

**Tray icon not visible**

- Check hidden tray icons (`^` menu)
- Restart the app

---

## 🇹🇷 Türkçe

Windows üzerinde çalışan bu uygulama, seri porttan (COM) gelen barkod verilerini aktif pencereye klavye girdisi olarak yazar.

### ✨ Özellikler

- 🔎 COM portlarını otomatik tarar ve listeler
- ⚙️ Baudrate değeri ayarlanabilir
- 🖥️ Gerçek zamanlı log ekranı
- ⌨️ Gelen barkod verisini klavye olarak yazar
- Enter modu:
  - **AKTİF**: barkod metni + Enter
  - **PASİF**: yalnızca barkod metni
- 🧩 Sistem tepsisi desteği
- ℹ️ İlk kapatma denemesinde tek seferlik bilgilendirme
- Tepsi menüsü:
  - **Göster**: ana pencereyi geri açar
  - **Çıkış**: uygulamayı tamamen kapatır
- 🖱️ Tepsi ikonuna çift tıklayınca pencere açılır

### 🧱 Proje Yapısı

```text
Barkod Okuyucu/
├─ COM2Keyboard.py
├─ requirements.txt
├─ README.md
```

### 📌 Gereksinimler

- Windows 10 / 11
- Python 3.10+
- COM/seri bağlantılı barkod okuyucu

### 🚀 Kurulum

1) Depoyu klonla

```bash
git clone https://github.com/taskhostw/com2keyboard.git
cd "com2keyboard"
```

1) Sanal ortam oluştur (önerilir)

```bash
python -m venv .venv
```

PowerShell aktivasyonu:

```powershell
.\.venv\Scripts\Activate.ps1
```

1) Bağımlılıkları yükle

```bash
pip install -r requirements.txt
```

### ▶️ Çalıştırma

```bash
python COM2Keyboard.py
```

İstersen doğrudan `COM2Keyboard.exe` dosyasını da çalıştırabilirsin.

### 🧭 Kullanım

1. Uygulamayı aç.
2. **Port Tara** butonuna tıkla.
3. COM port seç.
4. Gerekirse baudrate gir (varsayılan: `9600`).
5. **Bağlan** butonuna tıkla.
6. Barkod okut.
7. İhtiyaca göre `Enter: AKTİF/PASİF` modunu değiştir.

### 🧩 Tepsi Davranışı

- **Sistem Tepsisine Al** ile pencere gizlenir.
- Pencere **X** ile kapanmaz, tepsiye alınır.
- İlk seferde tek seferlik bilgilendirme mesajı gösterilir.
- Tam kapatma için tepsi ikonuna sağ tıklayıp **Çıkış** seç.
- Tepsi ikonuna çift tıklayınca pencere geri açılır.

### 🛠️ Kütüphaneler

- `pyserial`
- `keyboard`
- `customtkinter`
- `pystray`
- `Pillow`

### 🧪 Sorun Giderme

**COM port görünmüyor**

- Cihaz bağlantısını kontrol et
- Aygıt Yöneticisi’nden COM portunu doğrula
- Gerekirse yönetici olarak çalıştır

**Veri geliyor ama yazmıyor**

- Hedef pencerenin aktif olduğundan emin ol
- Güvenlik yazılımı keyboard hook’u engelliyor olabilir
- Yönetici olarak çalıştırmayı dene

**Tepsi ikonu görünmüyor**

- Gizli ikonlar menüsünü (`^`) kontrol et
- Uygulamayı yeniden başlat

---
