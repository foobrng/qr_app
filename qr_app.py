# app.py
import streamlit as st
import qrcode
import io
import base64
from urllib.parse import quote
import tempfile
import os

def generate_copy_page_html(text):
    """Generate HTML for the copy page"""
    escaped_text = text.replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br>')
    json_text = text.replace('"', '\\"').replace('\n', '\\n')
    
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
        }}
        .container {{
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            max-width: 500px;
            width: 100%;
            text-align: center;
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
        const textToCopy = "{json_text}";
        
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
    """Generate QR code image"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert PIL image to bytes
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    
    return img_buffer

def create_github_pages_url(username, repo_name, text):
    """Create URL for GitHub Pages hosted HTML file"""
    encoded_text = quote(text)
    return f"https://{username}.github.io/{repo_name}/copy.html?text={encoded_text}"

def main():
    st.set_page_config(
        page_title="QR Code Text Copier",
        page_icon="📋",
        layout="wide"
    )
    
    st.title("📋 QR Code Text Copier")
    st.markdown("Create QR codes that link to copy-friendly pages for easy text sharing")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # GitHub Pages option
        use_github_pages = st.checkbox("Use GitHub Pages for hosting", value=False)
        
        if use_github_pages:
            github_username = st.text_input("GitHub Username", placeholder="your-username")
            repo_name = st.text_input("Repository Name", placeholder="qr-text-copier")
            
            if github_username and repo_name:
                st.success(f"Pages URL: {github_username}.github.io/{repo_name}")
        else:
            st.info("Using data URL (works locally but may have limitations)")
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📝 Enter Your Text")
        
        text_content = st.text_area(
            "Text Content",
            placeholder="Enter the text you want users to easily copy...",
            height=150,
            label_visibility="collapsed"
        )
        
        if text_content:
            st.markdown("**Text Preview:**")
            with st.container():
                st.code(text_content, language=None)
            
            # Generate copy page HTML
            html_content = generate_copy_page_html(text_content)
            
            # Show HTML download
            st.download_button(
                label="📄 Download Copy Page HTML",
                data=html_content,
                file_name="copy.html",
                mime="text/html"
            )
            
            # Generate URL for QR code
            if use_github_pages and github_username and repo_name:
                qr_url = create_github_pages_url(github_username, repo_name, text_content)
                st.info(f"QR will link to: `{qr_url}`")
            else:
                # Use data URL
                html_b64 = base64.b64encode(html_content.encode()).decode()
                qr_url = f"data:text/html;base64,{html_b64}"
                st.warning("Using data URL - this may not work on all QR scanners. Consider using GitHub Pages.")
    
    with col2:
        st.header("📱 QR Code")
        
        if text_content:
            try:
                # Generate QR code
                if use_github_pages and github_username and repo_name:
                    qr_url = create_github_pages_url(github_username, repo_name, text_content)
                else:
                    html_b64 = base64.b64encode(html_content.encode()).decode()
                    qr_url = f"data:text/html;base64,{html_b64}"
                
                qr_image = create_qr_code(qr_url)
                
                # Display QR code
                st.image(qr_image, caption="Scan this QR code", width=300)
                
                # Download button for QR code
                st.download_button(
                    label="💾 Download QR Code",
                    data=qr_image.getvalue(),
                    file_name="qr-code.png",
                    mime="image/png"
                )
                
            except Exception as e:
                st.error(f"Error generating QR code: {str(e)}")
        else:
            st.info("Enter text to generate QR code")
    
    # Instructions
    st.markdown("---")
    st.header("📖 How It Works")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("**1. 📝 Enter Text**")
        st.markdown("Type the text you want users to copy")
    
    with col2:
        st.markdown("**2. 📱 Generate QR**")
        st.markdown("QR code links to copy page")
    
    with col3:
        st.markdown("**3. 🔍 User Scans**")
        st.markdown("Opens beautiful copy page")
    
    with col4:
        st.markdown("**4. 📋 One-Tap Copy**")
        st.markdown("Big button copies text instantly")
    
    # GitHub Pages setup instructions
    if use_github_pages:
        st.markdown("---")
        st.header("🚀 GitHub Pages Setup")
        st.markdown("""
        **To use GitHub Pages hosting:**
        
        1. Create a new repository on GitHub (e.g., `qr-text-copier`)
        2. Download the `copy.html` file using the button above
        3. Upload `copy.html` to your repository
        4. Enable GitHub Pages in repository settings
        5. Your copy page will be available at: `https://username.github.io/repo-name/copy.html`
        
        **Benefits of GitHub Pages:**
        - ✅ Works with all QR scanners
        - ✅ Fast loading times
        - ✅ Free hosting
        - ✅ Custom domain support
        """)

if __name__ == "__main__":
    main()