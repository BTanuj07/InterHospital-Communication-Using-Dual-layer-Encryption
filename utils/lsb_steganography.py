import numpy as np
from PIL import Image
import time

class LSBSteganography:
    def __init__(self):
        self.end_marker = '000111000111'
    
    def text_to_binary(self, text):
        binary = ''.join(format(ord(char), '08b') for char in text)
        return binary
    
    def binary_to_text(self, binary):
        chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
        text = ''.join(chr(int(char, 2)) for char in chars if len(char) == 8)
        return text
    
    def embed(self, image_path, secret_data):
        start_time = time.time()
        
        img = Image.open(image_path)
        img = img.convert('RGB')
        img_array = np.array(img)
        
        original_shape = img_array.shape
        flat_img = img_array.flatten()
        
        binary_data = self.text_to_binary(secret_data)
        binary_data_with_marker = binary_data + self.end_marker
        
        data_length = len(binary_data_with_marker)
        max_bytes = len(flat_img)
        
        if data_length > max_bytes:
            raise ValueError(f"Image too small. Need {data_length} pixels, have {max_bytes}")
        
        for i in range(data_length):
            flat_img[i] = (flat_img[i] & 0xFE) | int(binary_data_with_marker[i])
        
        stego_array = flat_img.reshape(original_shape)
        stego_img = Image.fromarray(stego_array.astype('uint8'), 'RGB')
        
        embedding_time = time.time() - start_time
        
        return {
            'stego_image': stego_img,
            'payload_size': len(secret_data),
            'binary_size': len(binary_data),
            'embedding_time': embedding_time,
            'image_size': original_shape
        }
    
    def extract(self, stego_image_path):
        start_time = time.time()
        
        img = Image.open(stego_image_path)
        img = img.convert('RGB')
        img_array = np.array(img)
        
        flat_img = img_array.flatten()
        
        binary_data = ''
        for pixel_value in flat_img:
            binary_data += str(pixel_value & 1)
            
            if len(binary_data) >= len(self.end_marker):
                if binary_data[-len(self.end_marker):] == self.end_marker:
                    binary_data = binary_data[:-len(self.end_marker)]
                    break
        
        secret_data = self.binary_to_text(binary_data)
        
        extraction_time = time.time() - start_time
        
        return {
            'extracted_data': secret_data,
            'extraction_time': extraction_time,
            'binary_length': len(binary_data)
        }
