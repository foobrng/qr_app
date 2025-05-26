import streamlit as st
import qrcode
import io

def create_qr_code(data):
    """Generate QR code image from data."""
    qr = qrcode.QRCode(
        version=None, # Auto-selects the smallest version
        error_correction=qrcode.constants.ERROR_CORRECT_L, # Low error correction for maximum data capacity
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    img_buffer = io.BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)

    return img_buffer

def main():
    st.set_page_config(
        page_title="Direct Text QR Code",
        page_icon="📄",
        layout="centered"
    )

    st.title("📄 Direct Text QR Code Generator")
    st.markdown("Enter your text, and get a QR code that displays the text directly when scanned.")

    text_content = st.text_area(
        "Enter the text to embed in the QR code:",
        placeholder="e.g., Hello World! This text will appear directly when the QR is scanned.",
        height=200
    )

    if text_content:
        st.subheader("Your QR Code")
        try:
            qr_image = create_qr_code(text_content) # Directly encode the text

            st.image(qr_image, caption="Scan this QR code", width=300)

            st.download_button(
                label="💾 Download QR Code (PNG)",
                data=qr_image.getvalue(),
                file_name="qr_text.png",
                mime="image/png"
            )
            st.success("QR code generated successfully!")
            st.info("When this QR code is scanned, the text will appear directly in the scanner app or browser. The user can then copy it manually.")


        except Exception as e:
            st.error(f"Error generating QR code: {str(e)}")
            st.warning("The text might be too long to fit directly into a QR code. Try shorter text.")

    else:
        st.info("Enter some text above to generate your QR code.")

    st.markdown("---")
    st.subheader("How It Works:")
    st.markdown("""
    1.  **Enter Text:** Type or paste your desired text.
    2.  **Generate QR:** The app instantly creates a QR code containing that exact text.
    3.  **Scan & View:** When scanned, the text will simply appear in the QR reader. There's no webpage, and no "copy" button, as the text is embedded directly.
    """)
    st.markdown("This method is the most straightforward as it requires no external hosting.")

if __name__ == "__main__":
    main()
