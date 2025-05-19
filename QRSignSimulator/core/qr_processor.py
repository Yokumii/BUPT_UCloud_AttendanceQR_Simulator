"""
二维码处理模块
负责二维码的生成、解码和处理
"""

import qrcode
import re
import os
import io
from pyzbar.pyzbar import decode
from PIL import Image
import numpy as np
import cv2
from datetime import datetime, timedelta
from dateutil import parser

from QRSignSimulator.config.settings import (
    QR_VERSION, QR_ERROR_CORRECTION, QR_BOX_SIZE, 
    QR_BORDER, QR_FILL_COLOR, QR_BACK_COLOR
)


class QRCodeProcessor:
    """二维码处理类"""
    
    @staticmethod
    def generate_qr_code(data):
        """生成二维码图像
        
        Args:
            data: 二维码数据
            
        Returns:
            PIL.Image: 生成的二维码图像
        """
        # 设置二维码参数
        error_correction_map = {
            'L': qrcode.constants.ERROR_CORRECT_L,
            'M': qrcode.constants.ERROR_CORRECT_M,
            'Q': qrcode.constants.ERROR_CORRECT_Q,
            'H': qrcode.constants.ERROR_CORRECT_H
        }
        
        error_correction = error_correction_map.get(
            QR_ERROR_CORRECTION, 
            qrcode.constants.ERROR_CORRECT_L
        )
        
        qr = qrcode.QRCode(
            version=QR_VERSION,
            error_correction=error_correction,
            box_size=QR_BOX_SIZE,
            border=QR_BORDER,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        # 创建图像
        img = qr.make_image(fill_color=QR_FILL_COLOR, back_color=QR_BACK_COLOR)
        return img
    
    @staticmethod
    def decode_qr_from_image(image):
        """从图像中解码二维码
        
        Args:
            image: 图像数据 (PIL.Image, numpy.ndarray, 或文件路径)
            
        Returns:
            str: 解码后的二维码数据，如果解码失败则返回None
        """
        try:
            # 处理不同类型的输入
            if isinstance(image, str):
                # 文件路径
                if not os.path.exists(image):
                    return None
                
                # 获取绝对路径，解决跨平台问题
                abs_path = os.path.abspath(image)
                
                # 尝试多种方式读取图像
                img = None
                
                # 方法1: 使用cv2.imread直接读取
                img = cv2.imread(abs_path)
                
                # 方法2: 如果cv2.imread失败，尝试使用PIL读取后转换
                if img is None:
                    try:
                        pil_img = Image.open(abs_path)
                        img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
                    except Exception:
                        pass
                
                # 方法3: 如果前两种方法都失败，尝试使用文件流读取
                if img is None:
                    try:
                        with open(abs_path, 'rb') as f:
                            img_data = np.frombuffer(f.read(), np.uint8)
                            img = cv2.imdecode(img_data, cv2.IMREAD_COLOR)
                    except Exception:
                        pass
                
                if img is None:
                    return None
                
            elif isinstance(image, Image.Image):
                # PIL图像
                img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            elif isinstance(image, np.ndarray):
                # NumPy数组
                img = image
            
            else:
                return None
            
            # 解码二维码
            decoded_objects = decode(img)
            for obj in decoded_objects:
                return obj.data.decode('utf-8')
            
            return None
            
        except Exception as e:
            print(f"二维码解码错误: {str(e)}")
            return None
    
    @staticmethod
    def extract_create_time(qr_data):
        """从二维码数据中提取createTime字段
        
        Args:
            qr_data: 二维码数据字符串
            
        Returns:
            tuple: (datetime对象, 原始格式字符串)，如果提取失败则返回(None, None)
        """
        match = re.search(r'createTime=([^&]+)', qr_data)
        if not match:
            return None, None
            
        create_time_str = match.group(1)
        try:
            # 保存原始时间字符串格式
            original_format = create_time_str
            # 解析ISO格式的日期时间，不保留时区信息
            create_time = parser.parse(create_time_str)
            # 转为无时区的本地时间
            if create_time.tzinfo is not None:
                create_time = create_time.replace(tzinfo=None)
            return create_time, original_format
        except Exception as e:
            print(f"解析日期时间错误: {str(e)}")
            return None, None
    
    @staticmethod
    def update_create_time(qr_data, target_time, original_format):
        """更新二维码数据中的createTime字段
        
        Args:
            qr_data: 原始二维码数据
            target_time: 目标时间 (datetime对象)
            original_format: 原始时间格式
            
        Returns:
            str: 更新后的二维码数据
        """
        # 分析原始格式
        original_has_microseconds = '.' in original_format
        
        # 创建新的时间字符串
        if original_has_microseconds:
            # 标准格式：带毫秒不带时区 (如 2025-03-13T16:34:01.221)
            # 获取毫秒数 (保留3位)
            ms_match = re.search(r'\.(\d+)$', original_format)
            if ms_match and len(ms_match.group(1)) == 3:
                # 保持3位毫秒精度，无时区
                new_time_str = target_time.strftime('%Y-%m-%dT%H:%M:%S.') + f"{target_time.microsecond // 1000:03d}"
            else:
                # 默认毫秒格式
                new_time_str = target_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
        else:
            # 简单ISO格式，不包含微秒和时区
            new_time_str = target_time.strftime('%Y-%m-%dT%H:%M:%S')
        
        # 替换createTime字段
        return re.sub(r'createTime=[^&]+', f'createTime={new_time_str}', qr_data) 