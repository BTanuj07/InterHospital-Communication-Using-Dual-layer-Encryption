from utils.dna_encryption import AES256DNAEncryption
from utils.lsb_steganography import LSBSteganography
from PIL import Image
import numpy as np
import base64

def create_test_image():
    img = Image.new('RGB', (400, 300), color=(100, 150, 200))
    img.save("test_cover_aes.png")
    return "test_cover_aes.png"

def test_full_aes_workflow_with_base64_key():
    print("="*70)
    print("Integration Test: Full AES-256 + DNA Workflow with Base64 Key Exchange")
    print("="*70)
    
    test_message = "Patient ID: 99999, Diagnosis: Critical Confidential Data"
    print(f"\n1. Original Message: {test_message}")
    
    print("\n2. ENCRYPTION PHASE (Simulating encrypt_embed.py)")
    print("-" * 70)
    
    enc = AES256DNAEncryption()
    encryption_key_base64 = enc.get_key_base64()
    print(f"   Generated Key (Base64): {encryption_key_base64}")
    print(f"   Key Length: {len(encryption_key_base64)} characters")
    
    encryption_result = enc.encrypt(test_message, use_aes=True)
    print(f"   Encrypted DNA: {encryption_result['encrypted_dna'][:50]}...")
    print(f"   Encryption Time: {encryption_result['encryption_time']:.4f}s")
    
    cover_image_path = create_test_image()
    lsb_steg = LSBSteganography()
    embedding_result = lsb_steg.embed(cover_image_path, encryption_result['encrypted_dna'])
    stego_image = embedding_result['stego_image']
    stego_image.save("test_stego_aes.png")
    print(f"   ✅ Stego-image created")
    
    print("\n3. KEY SHARING (User saves and provides key)")
    print("-" * 70)
    print(f"   User copies key: {encryption_key_base64}")
    user_provided_key = encryption_key_base64
    print(f"   User provides key for decryption: {user_provided_key}")
    
    print("\n4. DECRYPTION PHASE (Simulating extract_decrypt.py)")
    print("-" * 70)
    
    extraction_result = lsb_steg.extract("test_stego_aes.png")
    extracted_dna = extraction_result['extracted_data']
    print(f"   Extracted DNA: {extracted_dna[:50]}...")
    
    decoded_key = base64.b64decode(user_provided_key)
    print(f"   Decoded key from Base64")
    
    dec = AES256DNAEncryption(key=decoded_key)
    decryption_result = dec.decrypt(extracted_dna, use_aes=True)
    decrypted_text = decryption_result['decrypted_text']
    
    print(f"   Decrypted Message: {decrypted_text}")
    print(f"   Decryption Time: {decryption_result['decryption_time']:.4f}s")
    
    print("\n5. VERIFICATION")
    print("-" * 70)
    if test_message == decrypted_text:
        print(f"   ✅ SUCCESS: Messages match!")
        print(f"   Original:  {test_message}")
        print(f"   Decrypted: {decrypted_text}")
        return True
    else:
        print(f"   ❌ FAILED: Messages don't match!")
        print(f"   Original:  {test_message}")
        print(f"   Decrypted: {decrypted_text}")
        return False

if __name__ == "__main__":
    print("\n🧪 AES-256 Full Integration Test\n")
    
    success = test_full_aes_workflow_with_base64_key()
    
    print("\n" + "="*70)
    if success:
        print("🎉 INTEGRATION TEST PASSED")
        print("The encrypt and decrypt pages can successfully communicate via Base64 keys!")
    else:
        print("❌ INTEGRATION TEST FAILED")
        print("There is still a key format mismatch between encrypt and decrypt pages!")
    print("="*70 + "\n")
