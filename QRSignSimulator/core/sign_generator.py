"""
签到码生成器模块
负责生成随机签到码
"""

import random
import string
from datetime import datetime

from QRSignSimulator.config.settings import (
    QR_TEMPLATE, ID_LENGTH, CLASS_LESSON_ID_LENGTH, DEFAULT_TIME_FORMAT
)


class SignGenerator:
    """签到码生成器类"""
    
    @staticmethod
    def generate_random_digits(length):
        """生成指定长度的随机数字字符串
        
        Args:
            length: 要生成的字符串长度
            
        Returns:
            str: 随机数字字符串
        """
        return ''.join(random.choices(string.digits, k=length))
    
    @staticmethod
    def generate_sign_data(course_name=None, custom_id=None, custom_site_id=None, custom_class_lesson_id=None):
        """生成签到数据
        
        Args:
            course_name: 课程名称，可选
            custom_id: 自定义ID，可选，如果为None或空字符串则随机生成
            custom_site_id: 自定义站点ID，可选，如果为None或空字符串则随机生成
            custom_class_lesson_id: 自定义课程ID，可选，如果为None或空字符串则随机生成
            
        Returns:
            tuple: (签到数据字符串, 当前时间, 时间格式字符串)
        """
        # 生成ID
        if custom_id and custom_id.strip():
            random_id = custom_id
        else:
            random_id = SignGenerator.generate_random_digits(ID_LENGTH)
        
        # 获取站点ID
        if custom_site_id and custom_site_id.strip():
            site_id = custom_site_id
        else:
            site_id = SignGenerator.generate_random_digits(ID_LENGTH)  # 随机生成站点ID
        
        # 生成课程ID
        if custom_class_lesson_id and custom_class_lesson_id.strip():
            class_lesson_id = custom_class_lesson_id
        else:
            class_lesson_id = SignGenerator.generate_random_digits(CLASS_LESSON_ID_LENGTH)
        
        # 获取当前时间
        now = datetime.now()
        # 格式化时间，保留3位毫秒
        time_str = now.strftime(DEFAULT_TIME_FORMAT)[:-3]
        
        # 生成签到数据
        sign_data = QR_TEMPLATE.format(
            id=random_id,
            site_id=site_id,
            create_time=time_str,
            class_lesson_id=class_lesson_id
        )
        
        return sign_data, now, time_str 