# sync_excel.py
import os
import pandas as pd

def sync_excel_with_folder(excel_file="image_urls.xlsx"):
    # Excel'i oku
    df = pd.read_excel(excel_file)

    valid_rows = []
    for idx, row in df.iterrows():
        local_path = row["local_path"]
        # Dosya hâlâ duruyorsa sakla, yoksa atla
        if os.path.exists(local_path):
            valid_rows.append(row)
        else:
            print(f"[INFO] Silinmiş dosya tespit edildi: {local_path}")

    new_df = pd.DataFrame(valid_rows, columns=df.columns)
    new_df.to_excel(excel_file, index=False)
    print(f"{excel_file} güncellendi. Silinmiş dosyalar çıkarıldı.")

if __name__ == "__main__":
    sync_excel_with_folder()
