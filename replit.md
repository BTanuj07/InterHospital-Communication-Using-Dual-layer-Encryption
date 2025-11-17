# Secure Inter-Hospital Communication System

## Overview

This is a web-based medical data security application that enables secure transmission of sensitive healthcare information between hospitals. The system combines DNA-inspired encryption with LSB (Least Significant Bit) image steganography to hide encrypted medical data within digital images. Built with Streamlit for the frontend and Python for the backend, it provides an intuitive interface for healthcare professionals to encrypt, embed, extract, and decrypt confidential patient data while maintaining high image quality (PSNR > 40 dB).

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture

**Framework**: Streamlit-based multi-page application
- **Rationale**: Streamlit provides rapid development of data-centric web applications with Python, eliminating the need for separate frontend/backend development
- **Page Structure**: Navigation system using `st.navigation()` with 6 distinct pages (Home, Encrypt & Embed, Extract & Decrypt, DICOM Viewer, Analytics, AI Assistant)
- **State Management**: Session state (`st.session_state`) used for maintaining encryption/decryption history and chat messages across page navigation
- **Layout Pattern**: Two-column layouts for input/output separation, with wide page configuration for better data visualization

### Encryption & Steganography Pipeline

**DNA Encryption Module** (`utils/dna_encryption.py`)
- **Binary-to-DNA Encoding**: Converts text to 8-bit binary, then maps 2-bit pairs to DNA bases (00→A, 01→T, 10→C, 11→G)
- **Symmetric Substitution Cipher**: Applies biological base-pairing (A↔T, C↔G) for reversible encryption
- **Design Decision**: DNA encoding provides an additional obfuscation layer beyond traditional cryptography, making data unrecognizable even if extracted
- **Pros**: Unique security approach, reversible cipher; **Cons**: Increases data size due to encoding overhead

**LSB Steganography Module** (`utils/lsb_steganography.py`)
- **Embedding Method**: Modifies least significant bit of each pixel in RGB image to store binary data
- **End Marker**: Uses fixed binary marker (`000111000111`) to detect end of hidden data during extraction
- **Image Processing**: Flattens 3D image array to 1D for sequential bit embedding, then reshapes back
- **Design Decision**: LSB chosen over DCT/DWT for simplicity and lossless embedding capability
- **Trade-off**: LSB is vulnerable to image compression but offers high capacity and excellent imperceptibility

**Quality Metrics** (`utils/metrics.py`)
- **PSNR (Peak Signal-to-Noise Ratio)**: Measures image degradation after embedding; target >40dB indicates minimal visual change
- **SSIM (Structural Similarity Index)**: Evaluates perceived quality by comparing luminance, contrast, and structure
- **Implementation**: Uses OpenCV and scikit-image libraries for standardized metric calculation

### Medical Imaging Support

**DICOM Viewer** (`pages/dicom_viewer.py`)
- **Purpose**: Enables viewing of medical imaging files (CT, MRI, X-Ray) in standardized DICOM format
- **Library**: PyDICOM for parsing DICOM metadata and pixel data
- **Visualization**: Normalizes pixel arrays to 0-255 range for display, provides statistical metrics (min/max/mean/std)
- **Design Rationale**: Hospitals use DICOM as standard; supporting it allows direct use of medical images as steganography covers

### Analytics & Monitoring

**Analytics Dashboard** (`pages/analytics.py`)
- **Metrics Tracked**: Encryption/decryption timing, message lengths, PSNR/SSIM quality scores
- **Visualization**: Plotly interactive charts for time-series analysis and performance comparison
- **Data Storage**: Session state stores operation history as list of dictionaries
- **Purpose**: Allows users to monitor system performance and quality degradation across multiple operations

### AI Integration

**Chatbot Assistant** (`pages/chatbot.py`)
- **Provider**: OpenAI API for conversational AI
- **Purpose**: Educates users about DNA encryption, steganography, medical imaging, and platform usage
- **Context**: System-level message provides assistant with domain knowledge about the platform's features
- **Authentication**: Uses environment variable `OPENAI_API_KEY` from Replit Secrets
- **Session Management**: Maintains conversation history in `st.session_state.messages`

### Data Flow Architecture

**Encryption Flow**:
1. User inputs plaintext medical data
2. `DNAEncryption.encrypt()` converts text→binary→DNA→substituted DNA
3. User uploads cover image
4. `LSBSteganography.embed()` hides encrypted DNA in image LSBs
5. System calculates PSNR/SSIM quality metrics
6. User downloads stego-image; metrics stored in session history

**Decryption Flow**:
1. User uploads stego-image
2. `LSBSteganography.extract()` reads LSBs until end marker detected
3. Extracted binary converted to DNA sequence
4. `DNAEncryption.decrypt()` applies reverse substitution→binary→text
5. Original plaintext displayed; performance metrics recorded

### Security Considerations

**Multi-Layer Defense**: Combines encryption (DNA substitution) with obfuscation (steganography) for defense-in-depth
- **First Layer**: DNA encoding makes data unreadable without knowledge of encoding scheme
- **Second Layer**: LSB steganography hides existence of secret data within innocent-looking images
- **Limitation**: System uses symmetric encryption without key exchange mechanism; real deployment would require secure key distribution protocol

## External Dependencies

### Core Libraries
- **Streamlit** (`streamlit`): Web application framework for building the entire frontend
- **PIL/Pillow** (`PIL`, `Image`): Image loading, manipulation, and format conversion
- **NumPy** (`numpy`): Array operations for pixel manipulation and data processing
- **OpenCV** (`cv2`): Image I/O and preprocessing for quality metrics calculation

### Medical Imaging
- **PyDICOM** (`pydicom`): Parsing and reading DICOM medical imaging files
- **Purpose**: Enables integration with hospital PACS systems and standard medical image formats

### Machine Learning & Metrics
- **scikit-image** (`skimage.metrics`): PSNR and SSIM quality assessment algorithms
- **Plotly** (`plotly.graph_objects`, `plotly.express`): Interactive data visualization for analytics dashboard
- **Pandas** (`pandas`): DataFrame operations for historical data analysis

### AI Services
- **OpenAI API** (`openai`): GPT-based conversational AI for the chatbot assistant
- **Configuration**: Requires `OPENAI_API_KEY` environment variable set in Replit Secrets
- **Usage**: Provides contextual help and educational content about encryption and steganography

### Development Tools
- **Python Standard Library**: `os`, `sys`, `time`, `io` for file operations and performance measurement
- **Note**: No traditional database used; all data stored in Streamlit session state (in-memory, non-persistent)