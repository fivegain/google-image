import os
import subprocess

def run_command(command):
    """Verilen komutu terminalde çalıştırır."""
    print(f"[Komut Çalışıyor]: {command}")
    process = subprocess.Popen(command, shell=True)
    process.communicate()

def create_venv():
    """1) Sanal ortamı oluşturur."""
    if not os.path.exists("venv"):
        print("Sanal ortam oluşturuluyor...")
        run_command("python -m venv venv")
    else:
        print("Sanal ortam zaten mevcut.")

def clone_repo():
    """2) Git deposunu indirir."""
    repo_url = "https://github.com/fivegain/google-image.git"
    repo_name = "google-image"
    
    if not os.path.exists(repo_name):
        print(f"Git deposu '{repo_name}' indiriliyor...")
        run_command(f"git clone {repo_url}")
    else:
        print(f"'{repo_name}' klasörü zaten mevcut, klonlama atlanıyor.")

def install_packages():
    """3) requirements.txt içerisindeki paketleri yükler."""
    print("Kütüphaneler requirements.txt üzerinden yükleniyor...")
    # Burada requirements.txt 'google-image' klasörü içindeyse:
    run_command("venv\\Scripts\\python -m pip install -r google-image/requirements.txt")
    # Eğer proje ana dizininde ise:
    # run_command("venv\\Scripts\\python -m pip install -r requirements.txt")

def create_webdriver_directory():
    """4) webdriver klasörünü oluşturur (mkdir -p webdriver)."""
    webdriver_dir = "webdriver"
    if not os.path.exists(webdriver_dir):
        print(f"{webdriver_dir} klasörü oluşturuluyor...")
        os.makedirs(webdriver_dir)
    else:
        print(f"{webdriver_dir} klasörü zaten mevcut.")

def main():
    create_venv()                # 1) Sanal ortam oluştur
    clone_repo()                 # 2) Git deposu klonla
    install_packages()           # 3) Kütüphaneleri yükle
    create_webdriver_directory() # 4) webdriver klasörü oluştur

if __name__ == "__main__":
    main()
