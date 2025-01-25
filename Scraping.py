# -------------------------------------------
# Tutorial Mendapatkan API Key dari BinderByte
# -------------------------------------------
# Untuk mendapatkan API Key dari BinderByte, ikuti langkah-langkah berikut:
#
# 1. Daftar akun di website BinderByte: https://binderbyte.com
# 2. Setelah berhasil mendaftar, login ke akun kamu.
# 3. Setelah masuk ke dashboard, pilih menu **"Pilih Paket"** di bagian bar atas.
# 4. Pilih **Paket API Wilayah Indonesia** yang gratis dengan harga RP.0.
# 5. Setelah mengaktifkan paket API Wilayah Indonesia, pilih menu **API Key** di bagian bar atas.
# 6. Salin API Key yang tersedia.
# 7. Tempelkan API Key tersebut pada kode berikut, pada bagian **API_KEY**.
# 
# Contoh:
#   API_KEY = "masukkan-api-key-anda-di-sini"
#
# Setelah itu, Anda dapat menjalankan program ini untuk mengambil data provinsi, kabupaten, dan kecamatan dari API BinderByte.
# 
# -------------------------------------------
# BY: HUM NAITSUGA
# -------------------------------------------

import requests
import pandas as pd
import os

# Fungsi untuk mendapatkan data provinsi dari API
def get_provinces(api_url, api_key):
    try:
        url = f"{api_url}?api_key={api_key}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data.get("code") == "200":
            return data.get("value", [])
        else:
            print(f"Error dari API: {data.get('messages')}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error saat mengambil data provinsi: {e}")
        return []

# Fungsi untuk mendapatkan data kabupaten/kota berdasarkan ID provinsi
def get_cities(api_url, api_key, province_id):
    try:
        url = f"{api_url}?api_key={api_key}&id_provinsi={province_id}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data.get("code") == "200":
            return data.get("value", [])
        else:
            print(f"Error dari API: {data.get('messages')}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error saat mengambil data kabupaten/kota: {e}")
        return []

# Fungsi untuk mendapatkan data kecamatan berdasarkan ID kabupaten/kota
def get_districts(api_url, api_key, city_id):
    try:
        url = f"{api_url}?api_key={api_key}&id_kabupaten={city_id}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data.get("code") == "200":
            return data.get("value", [])
        else:
            print(f"Error dari API: {data.get('messages')}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error saat mengambil data kecamatan: {e}")
        return []

# Fungsi utama untuk mendapatkan data provinsi, kabupaten, dan kecamatan, lalu menyimpannya ke Excel
def fetch_data(api_url_provinces, api_url_cities, api_url_districts, api_key, output_filename):
    provinces = get_provinces(api_url_provinces, api_key)

    if not provinces:
        print("Gagal mendapatkan data provinsi.")
        return

    all_data = []

    for province in provinces:
        province_id = province["id"]
        province_name = province["name"]

        # Mendapatkan data kota untuk provinsi ini
        cities = get_cities(api_url_cities, api_key, province_id)

        if cities:
            for city in cities:
                city_id = city["id"]
                city_name = city["name"]

                # Mendapatkan data kecamatan untuk kota ini
                districts = get_districts(api_url_districts, api_key, city_id)

                if districts:
                    for district in districts:
                        district_id = district["id"]
                        district_name = district["name"]

                        # Menambahkan data provinsi, kota, dan kecamatan ke dalam list
                        all_data.append({
                            "Provinsi": province_name,
                            "ID Provinsi": province_id,
                            "Kota/Kabupaten": city_name,
                            "ID Kota/Kabupaten": city_id,
                            "Kecamatan": district_name,
                            "ID Kecamatan": district_id
                        })
                else:
                    print(f"Tidak ada kecamatan ditemukan untuk kota {city_name} di provinsi {province_name}")
        else:
            print(f"Tidak ada kota ditemukan untuk provinsi {province_name}")

    if not all_data:
        print("Tidak ada data untuk disimpan.")
        return

    # Simpan data ke file Excel
    try:
        df = pd.DataFrame(all_data)
        df.to_excel(output_filename, index=False)
        print(f"Data provinsi, kabupaten/kota, dan kecamatan berhasil disimpan ke {output_filename}")
    except Exception as e:
        print(f"Error saat menyimpan data ke Excel: {e}")

# Konfigurasi API dan file output
API_URL_PROVINCES = "https://api.binderbyte.com/wilayah/provinsi"
API_URL_CITIES = "https://api.binderbyte.com/wilayah/kabupaten"
API_URL_DISTRICTS = "http://api.binderbyte.com/wilayah/kecamatan"
API_KEY = "masukkan-api-key-anda-di-sini"  # Ganti dengan API Key Anda
OUTPUT_FILENAME = "data_provinsi_kota_kecamatan.xlsx"

# Jalankan program
if __name__ == "__main__":
    if os.path.exists(OUTPUT_FILENAME):
        os.remove(OUTPUT_FILENAME)

    fetch_data(API_URL_PROVINCES, API_URL_CITIES, API_URL_DISTRICTS, API_KEY, OUTPUT_FILENAME)
