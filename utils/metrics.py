import numpy as np
from PIL import Image
from skimage.metrics import peak_signal_noise_ratio, structural_similarity
import cv2
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

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
    
    @staticmethod
    def create_difference_heatmap(original_image_path, stego_image_path):
        img1 = cv2.imread(original_image_path)
        img2 = cv2.imread(stego_image_path)
        
        if img1 is None or img2 is None:
            return None
        
        if img1.shape != img2.shape:
            img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
        
        diff = cv2.absdiff(img1, img2)
        diff_magnitude = np.sqrt(np.sum(diff**2, axis=2))
        
        diff_normalized = (diff_magnitude - diff_magnitude.min()) / (diff_magnitude.max() - diff_magnitude.min() + 1e-8)
        diff_normalized = (diff_normalized * 255).astype(np.uint8)
        
        fig, ax = plt.subplots(figsize=(10, 8))
        im = ax.imshow(diff_normalized, cmap='hot', interpolation='nearest')
        ax.set_title('Pixel Difference Heatmap (LSB Changes)', fontsize=14, fontweight='bold')
        ax.axis('off')
        
        cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label('Difference Magnitude', rotation=270, labelpad=20)
        
        plt.tight_layout()
        
        fig.canvas.draw()
        heatmap_array = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        heatmap_array = heatmap_array.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        
        plt.close(fig)
        
        heatmap_image = Image.fromarray(heatmap_array)
        return heatmap_image
    
    @staticmethod
    def calculate_difference_stats(original_image_path, stego_image_path):
        img1 = cv2.imread(original_image_path)
        img2 = cv2.imread(stego_image_path)
        
        if img1 is None or img2 is None:
            return None
        
        if img1.shape != img2.shape:
            img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
        
        diff = cv2.absdiff(img1, img2)
        
        total_pixels = img1.shape[0] * img1.shape[1] * img1.shape[2]
        changed_pixels = np.count_nonzero(diff)
        change_percentage = (changed_pixels / total_pixels) * 100
        
        diff_magnitude = np.sqrt(np.sum(diff**2, axis=2))
        
        return {
            'total_pixels': total_pixels,
            'changed_pixels': changed_pixels,
            'change_percentage': change_percentage,
            'max_difference': np.max(diff_magnitude),
            'mean_difference': np.mean(diff_magnitude),
            'std_difference': np.std(diff_magnitude)
        }
