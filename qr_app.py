import streamlit as st
import qrcode
import io
import base64
from urllib.parse import quote

def generate_copy_page_html(text):
    """Generate HTML for the copy page with improved styling and direct copy."""
    # Escape HTML to prevent injection and display correctly
    escaped_text = text.replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br>')
    # Escape for JavaScript string literal
    json_text = text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\r', '')

    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Copy Text</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #333;
        }}
        .container {{
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            max-width: 500px;
            width: 100%;
            text-align: center;
            box-sizing: border-box;
        }}
        .icon {{
            font-size: 48px;
            margin-bottom: 20px;
        }}
        h1 {{
            color: #333;
            margin-bottom: 10px;
            font-size: 24px;
        }}
        .subtitle {{
            color: #666;
            margin-bottom: 30px;
            font-size: 16px;
        }}
        .text-content {{
            background: #f8f9fa;
            border: 2px solid #e9ecef;
            border-radius: 12px;
            padding: 20px;
            margin: 20px 0;
            font-family: monospace;
            font-size: 14px;
            line-height: 1.5;
            word-break: break-all;
            text-align: left;
            max-height: 200px;
            overflow-y: auto;
            white-space: pre-wrap; /* Preserves whitespace and line breaks */
        }}
        .copy-btn {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 50px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
            display: inline-flex;
            align-items: center;
            gap: 10px;
        }}
        .copy-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        }}
        .copy-btn:active {{
            transform: translateY(0);
        }}
        .success {{
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
            box-shadow: 0 4px 15px rgba(76, 175, 80, 0.4);
        }}
        .success:hover {{
            box-shadow: 0 6px 20px rgba(76, 175, 80, 0.6);
        }}
        @media (max-width: 600px) {{
            .container {{
                margin: 10px;
                padding: 30px 20px;
            }}
            .copy-btn {{
                font-size: 16px;
                padding: 12px 25px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="icon">📋</div>
        <h1>Copy Text Content</h1>
        <p class="subtitle">Tap the button below to copy this text to your clipboard</p>

        <div class="text-content">{escaped_text}</div>

        <button class="copy-btn" id="copyBtn" onclick="copyText()">
            <span id="btnIcon">📄</span>
            <span id="btnText">Copy to Clipboard</span>
        </button>
    </div>

    <script>
        const textToCopy = `{json_text}`; // Use backticks for template literals

        function copyText() {{
            const btn = document.getElementById('copyBtn');
            const btnIcon = document.getElementById('btnIcon');
            const btnText = document.getElementById('btnText');

            if (navigator.clipboard) {{
                navigator.clipboard.writeText(textToCopy).then(() => {{
                    showSuccess();
                }}).catch(() => {{
                    fallbackCopy();
                }});
            }} else {{
                fallbackCopy();
            }}

            function showSuccess() {{
                btn.classList.add('success');
                btnIcon.textContent = '✅';
                btnText.textContent = 'Copied!';

                setTimeout(() => {{
                    btn.classList.remove('success');
                    btnIcon.textContent = '📄';
                    btnText.textContent = 'Copy to Clipboard';
                }}, 2000);
            }}

            function fallbackCopy() {{
                const textArea = document.createElement('textarea');
                textArea.value = textToCopy;
                textArea.style.position = 'fixed';
                textArea.style.left = '-999999px';
                textArea.style.top = '-999999px';
                document.body.appendChild(textArea);
                textArea.focus();
                textArea.select();

                try {{
                    document.execCommand('copy');
                    showSuccess();
                }} catch (err) {{
                    btnText.textContent = 'Copy failed - select text above';
                }}

                document.body.removeChild(textArea);
            }}
        }}
    </script>
</body>
</html>'''
    return html_content

def create_qr_code(data):
    """Generate QR code image from data."""
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
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
        page_title="Simple QR Text Copier",
        page_icon="📋",
        layout="centered" # Changed to centered for simplicity
    )

    st.title("📋 Simple QR Text Copier")
    st.markdown("Enter text below, get a QR code. When scanned, it opens a page where the text can be copied.")

    text_content = st.text_area(
        "Text to be copied:",
        placeholder="Enter the text you want users to easily copy...",
        height=200
    )

    if text_content:
        # Generate the HTML content for the copy page
        html_content = generate_copy_page_html(text_content)

        # Encode HTML content to base64 for data URL
        html_b64 = base64.b64encode(html_content.encode('utf-8')).decode('utf-8')
        qr_url = f"data:text/html;base64,{html_b64}"

        st.subheader("Your QR Code")
        try:
            qr_image = create_qr_code(qr_url)

            st.image(qr_image, caption="Scan this QR code", width=300)

            st.download_button(
                label="💾 Download QR Code (PNG)",
                data=qr_image.getvalue(),
                file_name="qr_copy_text.png",
                mime="image/png"
            )

            st.info("The QR code contains a direct link to the copy page. No external hosting needed!")

        except Exception as e:
            st.error(f"Error generating QR code: {str(e)}")
            st.warning("The text might be too long for a data URL QR code. Try shorter text or consider hosting the HTML page externally if this persists.")

    else:
        st.info("Enter some text above to generate your QR code.")

    st.markdown("---")
    st.subheader("How it works:")
    st.markdown("""
    1.  **Enter Text:** Type your desired text in the box above.
    2.  **Get QR Code:** A QR code is generated instantly.
    3.  **Scan & Copy:** When someone scans the QR code, it opens a simple web page in their browser.
    4.  **One-Tap Copy:** On that page, they can tap a button to copy your text directly to their clipboard.
    """)

if __name__ == "__main__":
    main()
