from PIL import Image
import numpy as np
from utils.dna_encryption import DNAEncryption
from utils.lsb_steganography import LSBSteganography
from utils.metrics import ImageMetrics

def create_test_image(filename="test_image.png", size=(800, 600)):
    img = Image.new('RGB', size, color=(73, 109, 137))
    
    pixels = np.array(img)
    for i in range(0, size[1], 50):
        pixels[i:i+25, :] = [200, 100, 100]
    for j in range(0, size[0], 50):
        pixels[:, j:j+25] = [100, 200, 100]
    
    img = Image.fromarray(pixels)
    img.save(filename)
    print(f"✅ Created test image: {filename}")
    return filename

def test_encryption_decryption():
    print("\n" + "="*60)
    print("🧪 Testing DNA Encryption and LSB Steganography Pipeline")
    print("="*60 + "\n")
    
    test_message = "Patient ID: 12345, Diagnosis: Test Case, Treatment: Confidential Medical Data"
    print(f"📝 Original Message: {test_message}")
    print(f"📏 Message Length: {len(test_message)} characters\n")
    
    dna_enc = DNAEncryption()
    
    print("🔬 Step 1: DNA Encryption")
    print("-" * 60)
    encryption_result = dna_enc.encrypt(test_message)
    print(f"✅ Encryption completed in {encryption_result['encryption_time']:.4f} seconds")
    print(f"   Original length: {encryption_result['original_length']} characters")
    print(f"   Binary length: {encryption_result['binary_length']} bits")
    print(f"   DNA length: {encryption_result['dna_length']} bases")
    print(f"   Encrypted DNA: {encryption_result['encrypted_dna'][:50]}...")
    
    print(f"\n🖼️  Step 2: Creating Test Image")
    print("-" * 60)
    test_image_path = create_test_image()
    
    print(f"\n🔐 Step 3: LSB Embedding")
    print("-" * 60)
    lsb_steg = LSBSteganography()
    embedding_result = lsb_steg.embed(test_image_path, encryption_result['encrypted_dna'])
    print(f"✅ Embedding completed in {embedding_result['embedding_time']:.4f} seconds")
    print(f"   Payload size: {embedding_result['payload_size']} characters")
    print(f"   Binary size: {embedding_result['binary_size']} bits")
    print(f"   Image size: {embedding_result['image_size']}")
    
    stego_image_path = "test_stego.png"
    embedding_result['stego_image'].save(stego_image_path)
    print(f"   Saved stego-image: {stego_image_path}")
    
    print(f"\n📊 Step 4: Quality Analysis")
    print("-" * 60)
    psnr = ImageMetrics.calculate_psnr(test_image_path, stego_image_path)
    ssim = ImageMetrics.calculate_ssim(test_image_path, stego_image_path)
    
    if psnr is not None and ssim is not None:
        print(f"   PSNR: {psnr:.2f} dB")
        print(f"   SSIM: {ssim:.4f}")
        
        if psnr > 40:
            print(f"   ✅ Excellent image quality!")
        elif psnr > 30:
            print(f"   ✅ Good image quality")
        else:
            print(f"   ⚠️  Image quality degraded")
    else:
        print(f"   ⚠️  Could not calculate quality metrics")
    
    print(f"\n🔍 Step 5: LSB Extraction")
    print("-" * 60)
    extraction_result = lsb_steg.extract(stego_image_path)
    print(f"✅ Extraction completed in {extraction_result['extraction_time']:.4f} seconds")
    print(f"   Binary length: {extraction_result['binary_length']} bits")
    print(f"   Extracted DNA: {extraction_result['extracted_data'][:50]}...")
    
    print(f"\n🔓 Step 6: DNA Decryption")
    print("-" * 60)
    decryption_result = dna_enc.decrypt(extraction_result['extracted_data'])
    print(f"✅ Decryption completed in {decryption_result['decryption_time']:.4f} seconds")
    print(f"   Decrypted text: {decryption_result['decrypted_text']}")
    
    print(f"\n🎯 Step 7: Verification")
    print("-" * 60)
    if test_message == decryption_result['decrypted_text']:
        print("✅ SUCCESS! Original message matches decrypted message!")
        print(f"   Original:  {test_message}")
        print(f"   Decrypted: {decryption_result['decrypted_text']}")
    else:
        print("❌ FAILED! Messages do not match!")
        print(f"   Original:  {test_message}")
        print(f"   Decrypted: {decryption_result['decrypted_text']}")
    
    total_encryption_time = encryption_result['encryption_time'] + embedding_result['embedding_time']
    total_decryption_time = extraction_result['extraction_time'] + decryption_result['decryption_time']
    
    print(f"\n📈 Performance Summary")
    print("-" * 60)
    print(f"   Total Encryption + Embedding: {total_encryption_time:.4f} seconds")
    print(f"   Total Extraction + Decryption: {total_decryption_time:.4f} seconds")
    print(f"   Total Round Trip: {total_encryption_time + total_decryption_time:.4f} seconds")
    print(f"   Image Quality (PSNR): {psnr:.2f} dB")
    print(f"   Image Quality (SSIM): {ssim:.4f}")
    
    print("\n" + "="*60)
    print("🎉 All tests completed successfully!")
    print("="*60 + "\n")

if __name__ == "__main__":
    test_encryption_decryption()
