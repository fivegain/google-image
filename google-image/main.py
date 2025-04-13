# main.py
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 11:02:06 2020
@author:
"""
import os
import concurrent.futures
import pandas as pd
import re

from GoogleImageScraper import GoogleImageScraper
from patch import webdriver_executable

def read_search_keys_from_file(filename="search_keys.txt"):
    """
    `search_keys.txt` içeriğini satır satır okuyup liste olarak döndürür.
    Dosya aynı klasörde durmuyorsa tam yol belirtmen gerekebilir.
    """
    script_dir = os.path.dirname(__file__)
    txt_path = os.path.join(script_dir, filename)

    keys = []
    try:
        with open(txt_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:  # satır boş değilse ekle
                    keys.append(line)
    except FileNotFoundError:
        print(f"Dosya bulunamadı: {txt_path}. Varsayılan kelimeler kullanılacak.")
    return list(set(keys))

def sanitize_search_key(search_key):
    """
    Windows’ta yasaklı karakterler: < > : " / \ | ? *
    Bu regex ifadesiyle hepsini '_' karakterine dönüştürüyoruz.
    Örn: "ROBOT FIRÇA NO:3" -> "ROBOT FIRÇA NO_3"
    """
    return re.sub(r'[<>:"/\\|?*]', '_', search_key)

def worker_thread(search_key):
    """
    Her bir 'search_key' için GoogleImageScraper'ı çalıştırır,
    bulduğu görselleri indirir ve (search_key, url, local_path) şeklinde döndürür.
    """
    # Geçersiz karakterleri temizle, sonra GoogleImageScraper'a ver
    safe_key = sanitize_search_key(search_key)

    image_scraper = GoogleImageScraper(
        webdriver_path,
        image_path,
        safe_key,          # Temizlenmiş klasör adı
        number_of_images,
        headless,
        min_resolution,
        max_resolution,
        max_missed
    )

    image_urls = image_scraper.find_image_urls()
    downloaded_images = image_scraper.save_images(image_urls, keep_filenames)

    # downloaded_images => [(url, local_path), (url, local_path), ...]
    result = []
    for (url, local_path) in downloaded_images:
        # Excel'e orijinal search_key'i (temizlenmemiş metni) kaydetmek istersen:
        # result.append((search_key, url, local_path))
        #
        # Ama hangi klasörde olduğunu da tam bilmek istersen safe_key yazabilirsin.
        result.append((search_key, url, local_path))

    del image_scraper
    return result

def backup_excel_if_exists(excel_name="image_urls.xlsx", backup_folder="backup"):
    """
    Eğer 'excel_name' dosyası varsa, 'backup_folder' içine otomatik numaralandırarak taşır.
    Örn: image_urls.xlsx => backup/image_urls_001.xlsx, backup/image_urls_002.xlsx, ...
    """
    if os.path.exists(excel_name):
        # backup klasörü yoksa oluştur
        if not os.path.exists(backup_folder):
            os.makedirs(backup_folder)

        existing_backups = os.listdir(backup_folder)  # ['image_urls_001.xlsx', ...]
        version_nums = []
        for f in existing_backups:
            # f örn: "image_urls_003.xlsx"
            if f.startswith("image_urls_") and f.endswith(".xlsx"):
                try:
                    num_str = f.replace("image_urls_", "").replace(".xlsx", "")
                    version_nums.append(int(num_str))
                except ValueError:
                    pass

        next_num = 1 if not version_nums else max(version_nums) + 1
        backup_name = f"image_urls_{next_num:03d}.xlsx"  # Örn: image_urls_003.xlsx
        backup_path = os.path.join(backup_folder, backup_name)

        print(f"[INFO] Eski Excel dosyası bulundu. Yedekleniyor: {backup_path}")
        os.rename(excel_name, backup_path)

if __name__ == "__main__":
    # 1) WebDriver yolu
    webdriver_path = os.path.normpath(
        os.path.join(os.getcwd(), 'webdriver', webdriver_executable())
    )
    # 2) Görsellerin kaydedileceği klasör
    image_path = os.path.normpath(os.path.join(os.getcwd(), 'photos'))

    # 3) Aranacak kelimeleri 'search_keys.txt' üzerinden okumaya çalış
    search_keys = read_search_keys_from_file("search_keys.txt")

    print("DEBUG | Dosyadan gelen search_keys:", search_keys)
    if not search_keys:
        search_keys = ["car", "stars"]
        print("DEBUG | search_keys.txt boş veya bulunamadı. Varsayılan listeye geçildi:", search_keys)

    # Parametreler
    number_of_images = 5      # İndirilecek görsel sayısı
    headless = False          # True => Chrome arayüzünü kapatır
    min_resolution = (0, 0)
    max_resolution = (9999, 9999)
    max_missed = 10
    number_of_workers = 15    # Kaç iş parçacığı (thread) kullanılacak
    keep_filenames = False

    # Tüm sonuçları tutmak için liste
    all_results = []

    # Thread havuzu
    with concurrent.futures.ThreadPoolExecutor(max_workers=number_of_workers) as executor:
        for single_result in executor.map(worker_thread, search_keys):
            all_results.extend(single_result)

    # DataFrame: search_key | image_url | local_path
    df = pd.DataFrame(all_results, columns=["search_key", "image_url", "local_path"])

    # Eski Excel varsa backup klasörüne taşı (numaralandırarak)
    backup_excel_if_exists("image_urls.xlsx", "backup")

    # Yeni Excel'i kaydet
    df.to_excel("image_urls.xlsx", index=False)
    print("Tüm arama sonuçları 'image_urls.xlsx' dosyasına kaydedildi.")
