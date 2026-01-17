# Scientific Document Summarizer with Llama-3


**Sistem Peringkas Dokumen Ilmiah Otomatis berbasis Large Language Model (Llama-3.3-70b).**

**Live Demo:** [https://summarizer-sederhana.streamlit.app/](https://summarizer-sederhana.streamlit.app/)

**Link video:** https://mikroskilacid-my.sharepoint.com/:v:/g/personal/221112207_students_mikroskil_ac_id/IQD_Ip-fw4YEQLt1xAf0To_RAZ-Mh0PgzgU8FJdXS56R-8A?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=8oZgot

**Link Laporan:** 

**Link Paper:** https://mikroskilacid-my.sharepoint.com/:w:/g/personal/221112207_students_mikroskil_ac_id/IQD9Ux2SwJtLQYuSSd3akmGQAZGAA3gN-AFjQoLfdmET5iw?e=ezLeqF

---

## Fitur

1.  **Dual Input Interface**
    Mendukung dua metode input:
    * **Upload PDF:** Ekstraksi teks dari pdf yang diupload.
    * **Paste Text:** Input manual untuk peringkasan cepat potongan teks.

2.  **Noise Reduction**
    Sistem menggunakan algoritma berbasis Regex untuk mendeteksi dan memotong otomatis bagian *References*, *Bibliography*, atau *Daftar Pustaka*. Fitur ini menghemat 15-20% penggunaan token dan mencegah model menghasilkan halusinasi dari judul referensi.

3.  **Input Validation**
    Sistem mencegah halusinasi AI dengan menolak input teks yang terlalu pendek (kurang dari 300 karakter), memastikan model hanya memproses data yang memiliki konteks cukup.

4.  **Konfigurasi Output Dinamis**
    Pengguna dapat menyesuaikan hasil ringkasan sesuai kebutuhan:
    * **Panjang:** Pendek, Sedang, Panjang.
    * **Format:** Terstruktur (Markdown), Narasi Formal, atau Poin-poin (Bullet Points).

---

## Teknologi yang Digunakan

* **Bahasa Pemrograman:** Python 3.10
* **Frontend Framework:** Streamlit
* **LLM Inference:** Groq Cloud API (Model: `llama-3.3-70b-versatile`)
* **PDF Processing:** PyPDF2
* **Data Cleaning:** Python `re` (Regular Expression)

---

## Cara Menjalankan di Lokal (Installation)

Ikuti langkah-langkah berikut jika Anda ingin menjalankan source code di komputer lokal.

### 1. Clone Repository
Buka terminal atau Command Prompt dan jalankan perintah berikut:

`
git clone [https://github.com/Filburb/summarizer.git](https://github.com/Filburb/summarizer.git)
cd summarizer
`

### 2. Install Dependencies
Install seluruh library yang dibutuhkan

`
pip install -r requirements.txt
`

### 3.Konfigurasi API Key
Aplikasi ini menggunakan Groq API. Anda harus memiliki API Key sendiri untuk menjalankannya secara lokal.
1. Dapatkan API Key di: https://console.groq.com/keys

2.  Di dalam folder proyek, buat folder baru bernama .streamlit.

3.  Di dalam folder .streamlit, buat file bernama secrets.toml.

4.  Isi file secrets.toml dengan format berikut:
    * .streamlit/secrets.toml
    * GROQ_API_KEYS = "gsk_masukkan_api_key_anda_disini"


### 4. Jalankan Aplikasi
Jalankan perintah berikut untuk memulai server Streamlit:

`
streamlit run main.py
`
