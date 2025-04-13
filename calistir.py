import os
import subprocess

def run_command(command):
    """Terminalde (subprocess) komut çalıştırır."""
    print(f"[Komut Çalışıyor]: {command}")
    process = subprocess.Popen(command, shell=True)
    process.communicate()

def create_venv():
    """1) Sanal ortamı oluşturur (yoksa)."""
    if not os.path.exists("venv"):
        print("Sanal ortam oluşturuluyor...")
        run_command("python -m venv venv")
    else:
        print("Sanal ortam zaten mevcut. Oluşturma atlanıyor.")

def install_requirements():
    """2) google-image/requirements.txt içindeki paketleri sanal ortama kurar."""
    print("Kütüphaneler yükleniyor (google-image/requirements.txt)...")
    run_command(r"venv\Scripts\python -m pip install --upgrade pip")  # pip'i opsiyonel güncelle
    run_command(r"venv\Scripts\python -m pip install -r google-image\requirements.txt --upgrade")

def run_main_script():
    """3) google-image/main.py dosyasını çalıştırır."""
    print("Ana script (main.py) çalıştırılıyor...")
    run_command(r"venv\Scripts\python google-image\main.py")

def main():
    create_venv()           # Venv yoksa oluştur
    install_requirements()  # Paketleri kur
    run_main_script()       # Uygulamayı çalıştır

if __name__ == "__main__":
    main()
