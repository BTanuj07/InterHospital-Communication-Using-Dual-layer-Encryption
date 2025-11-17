from utils.dna_encryption import DNAEncryption, AES256DNAEncryption

def test_standard_encryption():
    print("="*60)
    print("Testing Standard DNA Encryption")
    print("="*60)
    
    dna_enc = DNAEncryption()
    test_message = "Patient ID: 12345, Diagnosis: Confidential"
    
    result = dna_enc.encrypt(test_message)
    print(f"Original: {test_message}")
    print(f"Encrypted DNA: {result['encrypted_dna'][:50]}...")
    print(f"Encryption time: {result['encryption_time']:.4f}s")
    
    decrypt_result = dna_enc.decrypt(result['encrypted_dna'])
    print(f"Decrypted: {decrypt_result['decrypted_text']}")
    print(f"Decryption time: {decrypt_result['decryption_time']:.4f}s")
    
    if test_message == decrypt_result['decrypted_text']:
        print("✅ Standard encryption/decryption PASSED")
    else:
        print("❌ Standard encryption/decryption FAILED")
    
    return test_message == decrypt_result['decrypted_text']

def test_aes_encryption():
    print("\n" + "="*60)
    print("Testing AES-256 + DNA Encryption")
    print("="*60)
    
    test_message = "Patient ID: 67890, Diagnosis: Top Secret Medical Data"
    encryption_key = "MySecureKey123456789012345678"
    
    aes_enc = AES256DNAEncryption(key=encryption_key)
    print(f"Original: {test_message}")
    print(f"Encryption Key: {encryption_key}")
    
    result = aes_enc.encrypt(test_message, use_aes=True)
    print(f"Encrypted DNA (with AES): {result['encrypted_dna'][:50]}...")
    print(f"Encryption time: {result['encryption_time']:.4f}s")
    print(f"Used AES: {result.get('used_aes', False)}")
    
    aes_dec = AES256DNAEncryption(key=encryption_key)
    decrypt_result = aes_dec.decrypt(result['encrypted_dna'], use_aes=True)
    print(f"Decrypted: {decrypt_result['decrypted_text']}")
    print(f"Decryption time: {decrypt_result['decryption_time']:.4f}s")
    
    if test_message == decrypt_result['decrypted_text']:
        print("✅ AES-256 + DNA encryption/decryption PASSED")
    else:
        print("❌ AES-256 + DNA encryption/decryption FAILED")
    
    return test_message == decrypt_result['decrypted_text']

def test_aes_with_different_keys():
    print("\n" + "="*60)
    print("Testing AES-256 with Wrong Key (Should Fail)")
    print("="*60)
    
    test_message = "Sensitive Data"
    correct_key = "CorrectKey12345678901234567890"
    wrong_key = "WrongKey123456789012345678901234"
    
    aes_enc = AES256DNAEncryption(key=correct_key)
    result = aes_enc.encrypt(test_message, use_aes=True)
    print(f"Encrypted with: {correct_key}")
    
    try:
        aes_dec = AES256DNAEncryption(key=wrong_key)
        decrypt_result = aes_dec.decrypt(result['encrypted_dna'], use_aes=True)
        print(f"❌ Should have failed with wrong key!")
        return False
    except Exception as e:
        print(f"✅ Correctly failed with wrong key: {type(e).__name__}")
        return True

if __name__ == "__main__":
    print("\n🧪 AES-256 Encryption Module Test Suite\n")
    
    test1 = test_standard_encryption()
    test2 = test_aes_encryption()
    test3 = test_aes_with_different_keys()
    
    print("\n" + "="*60)
    print("Test Results Summary")
    print("="*60)
    print(f"Standard DNA Encryption: {'✅ PASS' if test1 else '❌ FAIL'}")
    print(f"AES-256 + DNA Encryption: {'✅ PASS' if test2 else '❌ FAIL'}")
    print(f"Wrong Key Protection: {'✅ PASS' if test3 else '❌ FAIL'}")
    
    if all([test1, test2, test3]):
        print("\n🎉 All tests PASSED!")
    else:
        print("\n❌ Some tests FAILED!")
