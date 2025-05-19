"""
剪贴板处理模块
负责从剪贴板获取图像数据
"""

from PIL import ImageGrab
import numpy as np
import cv2


class ClipboardManager:
    """剪贴板管理类"""
    
    @staticmethod
    def get_clipboard_image():
        """从剪贴板获取图像
        
        Returns:
            tuple: (PIL.Image, numpy.ndarray) 或 (None, None)
        """
        try:
            # 获取剪贴板图片
            clipboard_img = ImageGrab.grabclipboard()
            
            if clipboard_img is None:
                return None, None
            
            # 转换为NumPy数组
            img_array = np.array(clipboard_img)
            
            # 如果是RGBA图像，转换为RGB
            if len(img_array.shape) == 3 and img_array.shape[2] == 4:
                img_array = cv2.cvtColor(img_array, cv2.COLOR_RGBA2RGB)
            
            return clipboard_img, img_array
            
        except Exception as e:
            print(f"剪贴板读取错误: {str(e)}")
            return None, None 