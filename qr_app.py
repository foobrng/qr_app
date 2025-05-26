import streamlit as st
import qrcode
import io
import base64
from urllib.parse import quote

def generate_copy_page_html(text):
    """Generate HTML for the copy page with styling and direct copy."""
    # Escape HTML to prevent injection and display correctly
    escaped_text = text.replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br>')
    # Escape for JavaScript string literal
    # Using JSON.parse to safely handle multi-line strings with quotes
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
        const textToCopy = `{json_text}`; // Use backticks for template literals to handle multi-line

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
        page_title="QR Code Text Copier (Simple)",
        page_icon="📋",
        layout="centered"
    )

    st.title("📋 QR Code Text Copier (Simple)")
    st.markdown("Create QR codes that link to a webpage where text can be copied with one tap.")

    st.subheader("1. Enter Your Text")
    text_content = st.text_area(
        "Type or paste the text you want users to copy:",
        placeholder="e.g., Your Wi-Fi password, a message, a long URL...",
        height=200
    )

    if text_content:
        st.subheader("2. Download the Copy Page HTML")
        html_content = generate_copy_page_html(text_content)

        st.download_button(
            label="⬇️ Download copy.html",
            data=html_content,
            file_name="copy.html",
            mime="text/html",
            help="Download this file and host it online (e.g., on GitHub Pages, Netlify, or your own web server)."
        )

        st.info("You need to host this `copy.html` file online so that the QR code can link to it.")

        st.subheader("3. Enter the Public URL of your Hosted HTML")
        hosted_url = st.text_input(
            "Public URL where you hosted 'copy.html':",
            placeholder="e.g., https://your-username.github.io/your-repo/copy.html"
        )

        if hosted_url:
            st.subheader("4. Your QR Code")
            try:
                qr_image = create_qr_code(hosted_url)

                st.image(qr_image, caption="Scan this QR code to access your text", width=300)

                st.download_button(
                    label="💾 Download QR Code (PNG)",
                    data=qr_image.getvalue(),
                    file_name="qr_copy_text.png",
                    mime="image/png"
                )
                st.markdown(f"**QR Code links to:** `{hosted_url}`")
                st.success("QR code generated successfully!")

            except Exception as e:
                st.error(f"Error generating QR code: {str(e)}")
                st.warning("Please ensure the URL is valid and try again. Very long URLs can still cause issues, but this is less likely than with data URLs.")
        else:
            st.warning("Please provide the public URL where you hosted your `copy.html` file to generate the QR code.")

    else:
        st.info("Enter some text above to start generating your copy page and QR code.")

    st.markdown("---")
    st.subheader("How It Works (Revised):")
    st.markdown("""
    1.  **Enter Text:** Type the text you want copied.
    2.  **Download HTML:** Get a specially designed `copy.html` file.
    3.  **Host HTML:** **Crucially**, you need to upload this `copy.html` file to a public web server (like GitHub Pages, Netlify, etc.). This makes it accessible via a short, stable URL.
    4.  **Enter Hosted URL:** Paste that public URL back into this app.
    5.  **Generate QR Code:** The app then creates a QR code that points to your hosted `copy.html` page.
    6.  **Scan & Copy:** When someone scans the QR, it opens your hosted page, where they can tap a button to copy the text.
    """)
    st.markdown("""
    **Why this approach?**
    QR codes have limited data capacity. Directly embedding a full HTML page into the QR code (via a data URL) often exceeds this limit, especially for longer texts, leading to errors like "Invalid version".
    By hosting the HTML file and linking to it, the QR code only needs to store a short URL, which is much more reliable.
    """)

if __name__ == "__main__":
    main()
