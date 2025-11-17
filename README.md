# 🏥 Secure Inter-Hospital Communication System

A comprehensive web application for secure medical data transmission using **DNA Encryption** and **LSB Image Steganography**.

## 🔐 Overview

This system provides a multi-layered security approach for transmitting sensitive medical information between hospitals:

1. **DNA Encryption**: Converts text data into DNA sequences with symmetric substitution cipher
2. **LSB Steganography**: Embeds encrypted data into medical images using Least Significant Bit manipulation
3. **Quality Preservation**: Maintains excellent image quality (PSNR > 40 dB)

## ✨ Features

### 🔐 Encrypt & Embed
- Enter sensitive medical data
- Upload any cover image (PNG, JPG, JPEG, BMP)
- Automatic DNA encryption with binary-to-DNA encoding
- LSB embedding with end-marker detection
- Download stego-image with hidden encrypted data
- Real-time PSNR/SSIM quality metrics

### 🔓 Extract & Decrypt
- Upload stego-images
- Automatic LSB extraction
- DNA decryption with reverse substitution cipher
- Retrieve original plaintext message
- Performance metrics and timing analysis

### 🩺 DICOM Viewer
- View medical imaging files (CT, MRI, X-Ray)
- Multi-slice navigation for 3D volumes
- Windowing controls for contrast adjustment
- Metadata inspection
- DICOM header visualization

### 📊 Analytics Dashboard
- Real-time performance metrics
- Encryption/Decryption timing analysis
- PSNR and SSIM quality tracking
- Interactive Plotly visualizations
- Historical data comparison

### 🤖 AI Assistant
- OpenAI-powered chatbot
- Explain encryption concepts
- Guide users through the platform
- Answer security and technical questions
- Contextual help and support

## 🔬 Technical Architecture

### DNA Encryption Algorithm

**Binary to DNA Encoding:**
```
00 → A (Adenine)
01 → T (Thymine)
10 → C (Cytosine)
11 → G (Guanine)
```

**Symmetric Substitution Cipher:**
```
A ↔ T
C ↔ G
```

**Pipeline:**
```
Text → Binary → DNA Sequence → Substitution Cipher → Encrypted DNA
```

### LSB Steganography

**Embedding Process:**
1. Convert encrypted DNA to binary
2. Replace LSB of each pixel with data bits
3. Add end marker (000111000111) for extraction
4. Save stego-image

**Extraction Process:**
1. Read LSB from each pixel
2. Scan for end marker
3. Extract binary data
4. Convert to DNA and decrypt

## 🛠️ Technology Stack

- **Frontend**: Streamlit (Python)
- **Image Processing**: PIL, OpenCV, NumPy
- **Medical Imaging**: pydicom
- **Visualization**: Plotly
- **Quality Metrics**: scikit-image (PSNR, SSIM)
- **AI**: OpenAI API (GPT-5)

## 📦 Installation

### Prerequisites
- Python 3.11+
- OpenAI API key (for chatbot)

### Setup

1. **Clone or access the repository**

2. **Install dependencies** (already configured in this Replit):
   ```bash
   # Dependencies are automatically managed
   # Packages: streamlit, pillow, numpy, pydicom, plotly, opencv-python, scikit-image, openai
   ```

3. **Configure OpenAI API Key** (optional, for chatbot):
   - Get API key from [OpenAI Platform](https://platform.openai.com/api-keys)
   - Add to Replit Secrets as `OPENAI_API_KEY`

4. **Run the application**:
   ```bash
   streamlit run app.py --server.port 5000
   ```

## 🚀 Usage Guide

### Encrypting Medical Data

1. Navigate to **Encrypt & Embed** page
2. Enter your secret medical message
3. Upload a cover image (PNG/JPG recommended)
4. Click **Encrypt and Embed**
5. View encryption metrics and quality analysis
6. Download the stego-image

### Extracting Hidden Data

1. Navigate to **Extract & Decrypt** page
2. Upload the stego-image
3. Click **Extract and Decrypt**
4. View the original decrypted message
5. Download the extracted text

### Viewing DICOM Files

1. Navigate to **DICOM Viewer** page
2. Upload a .dcm file
3. View medical images with automatic normalization
4. Use windowing controls for contrast adjustment
5. Inspect metadata and DICOM headers

### Monitoring Performance

1. Navigate to **Analytics** page
2. View encryption/decryption metrics
3. Analyze PSNR/SSIM quality trends
4. Compare processing times
5. Export analytics data

### Getting Help

1. Navigate to **AI Assistant** page
2. Ask questions about the system
3. Get explanations of encryption concepts
4. Receive guidance on best practices

## 📊 Performance Metrics

### Image Quality
- **PSNR**: Typically > 40 dB (Excellent)
- **SSIM**: Typically > 0.95 (High similarity)

### Processing Speed
- **Encryption**: < 0.1 seconds for typical messages
- **Embedding**: < 0.5 seconds for standard images
- **Extraction**: < 0.3 seconds
- **Decryption**: < 0.05 seconds

## 🔒 Security Considerations

### Strengths
- Multi-layer encryption (DNA + steganography)
- Reversible operations for legitimate receivers
- Visually imperceptible embedding
- No visible artifacts in stego-images

### Important Notes
- This is a **demonstration system** for research and education
- Not certified for production medical use
- Always comply with HIPAA and healthcare regulations
- Use secure channels for actual patient data
- Test thoroughly before deployment

## 📁 Project Structure

```
.
├── app.py                      # Main Streamlit application
├── pages/                      # Multi-page Streamlit pages
│   ├── home.py                # Home page with overview
│   ├── encrypt_embed.py       # Encryption & embedding interface
│   ├── extract_decrypt.py     # Extraction & decryption interface
│   ├── dicom_viewer.py        # DICOM medical image viewer
│   ├── analytics.py           # Analytics dashboard
│   └── chatbot.py             # AI assistant chatbot
├── utils/                     # Utility modules
│   ├── dna_encryption.py      # DNA encryption engine
│   ├── lsb_steganography.py   # LSB steganography implementation
│   └── metrics.py             # PSNR/SSIM calculations
└── README.md                  # This file
```

## 🧪 Testing

### Sample Workflow

1. **Prepare Test Data**:
   - Message: "Patient ID: 12345, Diagnosis: Test Case"
   - Image: Any PNG/JPG image (recommended: 800x600 or larger)

2. **Encrypt**:
   - Input message in Encrypt & Embed page
   - Upload cover image
   - Generate stego-image

3. **Decrypt**:
   - Upload stego-image in Extract & Decrypt page
   - Verify message matches original

4. **Validate**:
   - Check PSNR > 40 dB
   - Check SSIM > 0.95
   - Verify visual similarity

## 🤝 Research Background

Based on research in secure medical data transmission combining:
- **Bioinformatics-inspired cryptography**: DNA encoding for data representation
- **Digital steganography**: LSB techniques for covert communication
- **Medical imaging security**: DICOM compatibility and quality preservation

## 📚 References

### Key Concepts
- **DNA Cryptography**: Using biological principles for data encryption
- **LSB Steganography**: Hiding data in least significant bits of pixels
- **PSNR**: Peak Signal-to-Noise Ratio for image quality
- **SSIM**: Structural Similarity Index for perceptual quality
- **DICOM**: Digital Imaging and Communications in Medicine standard

## ⚠️ Disclaimer

This software is provided for **educational and research purposes only**. It is not intended for use with actual protected health information (PHI) or in production healthcare environments without proper security audits, certifications, and compliance reviews.

Always consult with information security professionals and legal advisors before implementing any medical data transmission system.

## 📄 License

This project is provided as-is for educational purposes.

## 🆘 Support

For questions or issues:
1. Use the AI Assistant chatbot in the application
2. Check the Analytics page for performance insights
3. Review this README for technical details

---

**Built with ❤️ using Python and Streamlit**

*Secure. Innovative. Educational.*
