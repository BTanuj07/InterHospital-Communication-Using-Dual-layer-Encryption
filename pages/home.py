import streamlit as st

st.title("🏥 Secure Inter-Hospital Communication System")
st.markdown("### Using DNA Encryption and LSB Image Steganography")

st.markdown("""
---

## 📋 Project Overview

This system provides a secure method for transmitting sensitive medical information between hospitals 
using advanced cryptographic techniques combined with image steganography.

### 🔐 Key Technologies

1. **DNA Encryption**
   - Converts text data into DNA sequences using binary encoding
   - Applies symmetric substitution cipher (A↔T, C↔G)
   - Provides an additional layer of biological-inspired security

2. **LSB Image Steganography**
   - Embeds encrypted data into medical images
   - Uses Least Significant Bit manipulation
   - Maintains image quality while hiding sensitive information

3. **DICOM Support**
   - Handles medical imaging formats
   - Preserves diagnostic image integrity
   - Compatible with standard hospital systems

---

## 🔄 System Architecture

### Encryption Pipeline
```
Input Text → Binary Conversion → DNA Encoding → Substitution Cipher → LSB Embedding → Stego-Image
```

### Decryption Pipeline
```
Stego-Image → LSB Extraction → Binary Data → DNA Decoding → Reverse Cipher → Original Text
```

---

## 📊 Features

""")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 🔐 Encrypt & Embed
    - Input sensitive medical data
    - Upload cover image
    - Generate stego-image
    - Download encrypted result
    """)

with col2:
    st.markdown("""
    ### 🔓 Extract & Decrypt
    - Upload stego-image
    - Extract hidden data
    - Decrypt using DNA cipher
    - View original message
    """)

with col3:
    st.markdown("""
    ### 🩺 DICOM Viewer
    - View medical images
    - Support for CT/MRI scans
    - Interactive visualization
    - Metadata inspection
    """)

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 📊 Analytics Dashboard
    - PSNR and SSIM metrics
    - Processing time analysis
    - Payload size tracking
    - Performance visualization
    """)

with col2:
    st.markdown("""
    ### 🤖 AI Assistant
    - Explain encryption concepts
    - Guide platform usage
    - Answer security questions
    - Technical support
    """)

st.markdown("---")

st.markdown("""
## 🚀 Getting Started

1. **Encrypt & Embed**: Start by encrypting your medical data and embedding it into an image
2. **Extract & Decrypt**: Retrieve and decrypt the hidden information from the stego-image
3. **DICOM Viewer**: View and analyze medical imaging files
4. **Analytics**: Monitor system performance and security metrics
5. **AI Assistant**: Get help and guidance on using the system

---

## 🔒 Security Features

- **Multi-layer Encryption**: Combines DNA encoding with LSB steganography
- **Reversible Operations**: All encryption steps can be reversed for decryption
- **Image Integrity**: Minimal visual impact on carrier images
- **End Markers**: Reliable data extraction with termination markers

---

## ⚠️ Important Notes

- This is a demonstration system for educational and research purposes
- Always use secure channels for actual medical data transmission
- Ensure compliance with HIPAA and other healthcare data regulations
- Test thoroughly before production deployment

---
""")

st.info("👈 Use the sidebar navigation to explore different features of the system")
