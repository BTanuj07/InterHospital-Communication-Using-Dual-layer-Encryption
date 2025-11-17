import time

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
