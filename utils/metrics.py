import numpy as np
from PIL import Image
from skimage.metrics import peak_signal_noise_ratio, structural_similarity
import cv2

class ImageMetrics:
    @staticmethod
    def calculate_psnr(original_image_path, stego_image_path):
        img1 = cv2.imread(original_image_path)
        img2 = cv2.imread(stego_image_path)
        
        if img1 is None or img2 is None:
            return None
        
        if img1.shape != img2.shape:
            img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
        
        psnr_value = peak_signal_noise_ratio(img1, img2)
        return psnr_value
    
    @staticmethod
    def calculate_ssim(original_image_path, stego_image_path):
        img1 = cv2.imread(original_image_path)
        img2 = cv2.imread(stego_image_path)
        
        if img1 is None or img2 is None:
            return None
        
        if img1.shape != img2.shape:
            img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
        
        img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        
        ssim_value = structural_similarity(img1_gray, img2_gray)
        return ssim_value
    
    @staticmethod
    def get_image_info(image_path):
        img = Image.open(image_path)
        return {
            'size': img.size,
            'mode': img.mode,
            'format': img.format,
            'width': img.width,
            'height': img.height
        }
