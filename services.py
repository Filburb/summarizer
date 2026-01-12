import os
import re
import time
import random
from groq import Groq
import streamlit as st

class AIService:
    def __init__(self):
        # Ambil key dari Secrets atau Environment
        try:
            env_key = st.secrets["GROQ_API_KEYS"]
        except:
            env_key = os.getenv('GROQ_API_KEYS')
            
        self.api_keys = []
        if env_key:
            self.api_keys = [k.strip() for k in env_key.split(',') if k.strip()]
        
        self.MODEL_ID = "llama-3.3-70b-versatile"
        self.CHUNK_SIZE = 45000 
        self.OVERLAP = 1500

    def _get_random_key(self):
        if not self.api_keys: return None
        return random.choice(self.api_keys)

    def summarize(self, text, length, output_format, status_callback=None):
        if not self.api_keys:
            return "Error: API Key tidak ditemukan."

        if status_callback: status_callback("Membersihkan dan memvalidasi teks...")
        
        # 1. BERSIHKAN DULU
        clean_text = self._smart_clean(text)
        
        # 2. VALIDASI INPUT (Mencegah Halusinasi)
        # Jika teks kurang dari 300 karakter, tolak langsung.
        if len(clean_text) < 300:
            return (
                "ERROR: Teks terlalu pendek atau tidak valid.\n\n"
                "Sistem tidak dapat memproses input ini karena kurangnya konteks. "
                "Mohon masukkan teks artikel/jurnal yang lengkap (minimal 300 karakter) "
                "agar hasil ringkasan akurat."
            )

        # 3. LANJUT KE PROSES JIKA LOLOS
        return self._process_strict_queue(clean_text, length, output_format, status_callback)

    def _smart_clean(self, text):
        # Hapus spasi berlebih
        text = " ".join(text.split())
        
        patterns = [r'\nDAFTAR PUSTAKA', r'\nREFERENCES', r'\nBIBLIOGRAPHY']
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match and match.start() > len(text) * 0.5: 
                text = text[:match.start()]
                break
        return text

    def _process_strict_queue(self, text, length, output_format, status_callback):
        chunks = []
        start = 0
        while start < len(text):
            end = start + self.CHUNK_SIZE
            chunks.append(text[start:end])
            start = end - self.OVERLAP
        
        if status_callback: status_callback(f"Dokumen valid. Membagi menjadi {len(chunks)} bagian analisis.")
        
        extracted_facts = []
        
        for i, chunk in enumerate(chunks):
            if status_callback: status_callback(f"Menganalisis bagian {i+1} dari {len(chunks)}...")
            
            facts = self._extract_facts(chunk)
            if facts:
                extracted_facts.append(facts)
            
            if i < len(chunks) - 1:
                time.sleep(1)

        combined_facts = "\n\n".join(extracted_facts)
        
        if status_callback: status_callback("Menyusun laporan akhir...")
        return self._generate_final_report(combined_facts, length, output_format)

    def _extract_facts(self, text):
        sys_prompt = """
        PERAN: Analis Data Ilmiah.
        TUGAS: Ekstrak data penting (Metode, Hasil, Kesimpulan).
        INSTRUKSI: Jangan ambil data dari Related Work/Penelitian orang lain.
        OUTPUT: Bahasa Indonesia.
        """
        max_attempts = len(self.api_keys) * 2
        for _ in range(max_attempts):
            key = self._get_random_key()
            client = Groq(api_key=key)
            try:
                completion = client.chat.completions.create(
                    messages=[{"role": "system", "content": sys_prompt}, {"role": "user", "content": text}],
                    model=self.MODEL_ID, temperature=0.0
                )
                return completion.choices[0].message.content
            except:
                time.sleep(1)
                continue
        return ""

    def _generate_final_report(self, text, length, output_format):
        key = self._get_random_key()
        client = Groq(api_key=key)
        
        structure = ""
        if output_format == 'terstruktur':
            structure = "Gunakan format: 1. Abstrak, 2. Masalah, 3. Metode, 4. Hasil, 5. Kesimpulan."
        elif output_format == 'formal':
            structure = "Tulis dalam satu paragraf narasi utuh yang mengalir. Jangan pakai poin-poin."
        else:
            structure = "Gunakan bullet points."

        sys_prompt = f"""
        PERAN: Editor Profesional.
        TUGAS: Ringkas teks berikut dalam Bahasa Indonesia Baku.
        PANJANG: {length}.
        FORMAT: {structure}
        """

        try:
            completion = client.chat.completions.create(
                messages=[{"role": "system", "content": sys_prompt}, {"role": "user", "content": text}],
                model=self.MODEL_ID, temperature=0.2
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"