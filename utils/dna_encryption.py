import time
import base64
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

class DNAEncryption:
    def __init__(self):
        self.binary_to_dna = {
            '00': 'A',
            '01': 'T',
            '10': 'C',
            '11': 'G'
        }
        
        self.dna_to_binary = {
            'A': '00',
            'T': '01',
            'C': '10',
            'G': '11'
        }
        
        self.substitution_cipher = {
            'A': 'T',
            'T': 'A',
            'C': 'G',
            'G': 'C'
        }
        
        self.reverse_substitution = {
            'T': 'A',
            'A': 'T',
            'G': 'C',
            'C': 'G'
        }
    
    def text_to_binary(self, text):
        binary = ''.join(format(ord(char), '08b') for char in text)
        return binary
    
    def binary_to_text(self, binary):
        chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
        text = ''.join(chr(int(char, 2)) for char in chars if len(char) == 8)
        return text
    
    def binary_to_dna_sequence(self, binary):
        if len(binary) % 2 != 0:
            binary += '0'
        
        dna_sequence = ''
        for i in range(0, len(binary), 2):
            two_bits = binary[i:i+2]
            dna_sequence += self.binary_to_dna[two_bits]
        
        return dna_sequence
    
    def dna_to_binary_sequence(self, dna):
        binary = ''
        for nucleotide in dna:
            binary += self.dna_to_binary[nucleotide]
        return binary
    
    def apply_substitution(self, dna_sequence):
        encrypted = ''.join(self.substitution_cipher[nucleotide] for nucleotide in dna_sequence)
        return encrypted
    
    def reverse_substitution_cipher(self, encrypted_dna):
        decrypted = ''.join(self.reverse_substitution[nucleotide] for nucleotide in encrypted_dna)
        return decrypted
    
    def encrypt(self, text):
        start_time = time.time()
        
        binary = self.text_to_binary(text)
        dna_sequence = self.binary_to_dna_sequence(binary)
        encrypted_dna = self.apply_substitution(dna_sequence)
        
        encryption_time = time.time() - start_time
        
        return {
            'encrypted_dna': encrypted_dna,
            'original_length': len(text),
            'binary_length': len(binary),
            'dna_length': len(encrypted_dna),
            'encryption_time': encryption_time
        }
    
    def decrypt(self, encrypted_dna):
        start_time = time.time()
        
        decrypted_dna = self.reverse_substitution_cipher(encrypted_dna)
        binary = self.dna_to_binary_sequence(decrypted_dna)
        text = self.binary_to_text(binary)
        
        decryption_time = time.time() - start_time
        
        return {
            'decrypted_text': text,
            'decryption_time': decryption_time
        }


class AES256DNAEncryption(DNAEncryption):
    def __init__(self, key=None):
        super().__init__()
        if key is None:
            self.key = os.urandom(32)
        elif isinstance(key, str):
            key_bytes = key.encode('utf-8')
            if len(key_bytes) < 32:
                self.key = key_bytes.ljust(32, b'0')
            elif len(key_bytes) > 32:
                self.key = key_bytes[:32]
            else:
                self.key = key_bytes
        else:
            self.key = key
    
    def aes_encrypt(self, plaintext):
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(plaintext.encode('utf-8')) + padder.finalize()
        
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        
        return base64.b64encode(iv + ciphertext).decode('utf-8')
    
    def aes_decrypt(self, ciphertext_b64):
        ciphertext_with_iv = base64.b64decode(ciphertext_b64)
        
        iv = ciphertext_with_iv[:16]
        ciphertext = ciphertext_with_iv[16:]
        
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        
        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
        
        return plaintext.decode('utf-8')
    
    def encrypt(self, text, use_aes=True):
        start_time = time.time()
        
        if use_aes:
            aes_encrypted = self.aes_encrypt(text)
            binary = self.text_to_binary(aes_encrypted)
        else:
            binary = self.text_to_binary(text)
        
        dna_sequence = self.binary_to_dna_sequence(binary)
        encrypted_dna = self.apply_substitution(dna_sequence)
        
        encryption_time = time.time() - start_time
        
        return {
            'encrypted_dna': encrypted_dna,
            'original_length': len(text),
            'binary_length': len(binary),
            'dna_length': len(encrypted_dna),
            'encryption_time': encryption_time,
            'used_aes': use_aes
        }
    
    def decrypt(self, encrypted_dna, use_aes=True):
        start_time = time.time()
        
        decrypted_dna = self.reverse_substitution_cipher(encrypted_dna)
        binary = self.dna_to_binary_sequence(decrypted_dna)
        intermediate_text = self.binary_to_text(binary)
        
        if use_aes:
            text = self.aes_decrypt(intermediate_text)
        else:
            text = intermediate_text
        
        decryption_time = time.time() - start_time
        
        return {
            'decrypted_text': text,
            'decryption_time': decryption_time
        }
    
    def get_key_base64(self):
        return base64.b64encode(self.key).decode('utf-8')
