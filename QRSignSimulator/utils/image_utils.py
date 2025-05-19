"""
图像处理工具模块
负责图像转换和处理
"""

import cv2
import numpy as np
from PIL import Image, ImageTk

from QRSignSimulator.config.settings import IMAGE_MAX_WIDTH, IMAGE_MAX_HEIGHT


class ImageProcessor:
    """图像处理类"""
    
    @staticmethod
    def convert_to_tkimage(img_data):
        """将图像数据转换为Tkinter可显示的图像
        
        Args:
            img_data: 图像数据 (PIL.Image, numpy.ndarray)
            
        Returns:
            ImageTk.PhotoImage: Tkinter可显示的图像对象，转换失败则返回None
        """
        try:
            if img_data is None:
                return None
            
            # 转换为PIL图像
            if isinstance(img_data, np.ndarray):
                # 确保输入数组是有效的
                if img_data.size == 0 or img_data.ndim < 2:
                    print("无效的图像数组")
                    return None
                
                # 确保图像数据类型正确
                img_data = img_data.astype('uint8')
                
                # 单通道图像转换为RGB
                if len(img_data.shape) == 2:
                    img = Image.fromarray(img_data, mode='L')
                else:
                    img = Image.fromarray(img_data)
            elif isinstance(img_data, Image.Image):
                img = img_data
            else:
                print("不支持的图像数据类型")
                return None
            
            # 调整大小以适应显示
            img.thumbnail((IMAGE_MAX_WIDTH, IMAGE_MAX_HEIGHT))
            
            # 转换为Tkinter图像
            return ImageTk.PhotoImage(img)
        
        except Exception as e:
            print(f"图像转换错误: {str(e)}")
            return None
    
    @staticmethod
    def convert_cv_to_rgb(cv_img):
        """将OpenCV图像转换为RGB格式
        
        Args:
            cv_img: OpenCV格式的图像 (BGR)
            
        Returns:
            numpy.ndarray: RGB格式的图像
        """
        if cv_img is None:
            return None
            
        return cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    
    @staticmethod
    def convert_rgba_to_rgb(rgba_img):
        """将RGBA图像转换为RGB格式
        
        Args:
            rgba_img: RGBA格式的图像 (numpy.ndarray)
            
        Returns:
            numpy.ndarray: RGB格式的图像
        """
        if rgba_img is None:
            return None
            
        if len(rgba_img.shape) == 3 and rgba_img.shape[2] == 4:
            return cv2.cvtColor(rgba_img, cv2.COLOR_RGBA2RGB)
        
        return rgba_img 