import streamlit as st
import interface
import services
import utils

def main():
    # 1. Setup
    interface.setup_page()
    interface.render_header()

    # 2. Render Form Utama (Sesuai Screenshot)
    text_input, uploaded_file, length, fmt = interface.render_form()
    
    # 3. Tombol Eksekusi (Full Width secara visual di layout centered)
    if st.button("Ringkas Teks", type="primary", use_container_width=True):
        
        # Logika Prioritas Input: Teks Manual > PDF
        final_text = ""
        
        if text_input.strip():
            final_text = text_input
        elif uploaded_file:
            with st.spinner("Membaca file PDF..."):
                extracted = utils.extract_text_from_pdf(uploaded_file)
                if extracted:
                    final_text = extracted
                else:
                    st.error("Gagal membaca file PDF.")
                    return
        
        if not final_text:
            st.warning("Mohon masukkan teks atau upload file PDF.")
            return

        # 4. Proses AI
        ai_service = services.AIService()
        status_box = st.empty()
        
        try:
            def update_status(msg):
                status_box.info(msg)

            summary = ai_service.summarize(
                text=final_text,
                length=length,
                output_format=fmt,
                status_callback=update_status
            )
            
            status_box.empty()
            st.markdown("### Hasil Ringkasan")
            st.markdown("---")
            st.markdown(summary)
            
        except Exception as e:
            status_box.empty()
            st.error(f"Terjadi kesalahan: {str(e)}")

if __name__ == "__main__":
    main()