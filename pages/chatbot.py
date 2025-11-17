import streamlit as st
import os
from openai import OpenAI

st.title("🤖 AI Assistant")
st.markdown("### Your intelligent guide for secure medical data encryption")

st.markdown("---")

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.warning("⚠️ OpenAI API key not configured")
    st.info("""
    To enable the AI Assistant, you need to provide an OpenAI API key:
    
    1. Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)
    2. Add it to your Replit Secrets as `OPENAI_API_KEY`
    3. Refresh this page
    """)
    st.stop()

if 'messages' not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": """👋 Hello! I'm your AI assistant for the Secure Inter-Hospital Communication System.

I can help you with:
- 🔐 Understanding DNA encryption and how it works
- 🖼️ Learning about LSB steganography techniques
- 📊 Interpreting PSNR and SSIM metrics
- 🩺 DICOM file formats and medical imaging
- 🔒 Best practices for secure medical data transmission
- 🛠️ Navigating and using this platform

What would you like to know?"""
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything about encryption, steganography, or the system..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            client = OpenAI(api_key=OPENAI_API_KEY)
            
            system_prompt = """You are an expert AI assistant for a Secure Inter-Hospital Communication System that uses DNA encryption and LSB image steganography.

Your knowledge includes:
- DNA Encryption: Binary to DNA encoding (00→A, 01→T, 10→C, 11→G) with symmetric substitution cipher (A↔T, C↔G)
- LSB Steganography: Embedding encrypted data in image pixels using Least Significant Bit manipulation
- DICOM medical imaging format and standards
- Image quality metrics: PSNR (Peak Signal-to-Noise Ratio) and SSIM (Structural Similarity Index)
- Security best practices for medical data
- HIPAA compliance considerations

Provide clear, concise, and helpful responses. Use examples when appropriate. Be professional but friendly."""

            from typing import cast
            from openai.types.chat import ChatCompletionMessageParam
            
            messages_for_api: list[ChatCompletionMessageParam] = [
                {"role": "system", "content": system_prompt}
            ] + cast(list[ChatCompletionMessageParam], st.session_state.messages)
            
            # the newest OpenAI model is "gpt-5" which was released August 7, 2025.
            # do not change this unless explicitly requested by the user
            response = client.chat.completions.create(
                model="gpt-5",
                messages=messages_for_api,
                stream=True
            )
            
            full_response = ""
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            error_message = f"❌ Error: {str(e)}"
            message_placeholder.markdown(error_message)
            st.session_state.messages.append({"role": "assistant", "content": error_message})

st.markdown("---")

with st.expander("💡 Sample Questions"):
    st.markdown("""
    - How does DNA encryption work in this system?
    - What is LSB steganography and why is it secure?
    - What do PSNR and SSIM values mean?
    - How can I interpret the analytics data?
    - What file formats are supported for DICOM viewing?
    - What are the security considerations for medical data?
    - How do I encrypt a message step by step?
    - What makes this system secure for hospital communication?
    """)

col1, col2 = st.columns(2)

with col1:
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = [st.session_state.messages[0]]
        st.rerun()

with col2:
    if st.button("💾 Export Chat", use_container_width=True):
        chat_export = "\n\n".join([
            f"{'User' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}"
            for msg in st.session_state.messages
        ])
        st.download_button(
            label="Download Chat History",
            data=chat_export,
            file_name="chat_history.txt",
            mime="text/plain",
            use_container_width=True
        )
