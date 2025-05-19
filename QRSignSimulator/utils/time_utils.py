"""
时间处理工具模块
负责时间相关的计算和转换
"""

from datetime import datetime, timedelta
import pytz

from QRSignSimulator.config.settings import TIME_ZONE, UPDATE_INTERVAL


class TimeManager:
    """时间管理类"""
    
    @staticmethod
    def get_beijing_time():
        """获取北京时间
        
        Returns:
            datetime: 无时区信息的北京时间
        """
        beijing_tz = pytz.timezone(TIME_ZONE)
        # 返回无时区信息的时间
        now = datetime.now(beijing_tz)
        return now.replace(tzinfo=None)
    
    @staticmethod
    def calculate_target_time(original_time, current_time=None):
        """计算目标时间（最接近当前时间的指定间隔倍数）
        
        Args:
            original_time: 原始时间 (datetime对象)
            current_time: 当前时间 (datetime对象)，如果为None则使用当前北京时间
            
        Returns:
            tuple: (目标时间, 下一个目标时间, 倒计时秒数)
        """
        if current_time is None:
            current_time = TimeManager.get_beijing_time()
        
        # 计算从原始时间开始，最接近当前时间的间隔倍数
        time_diff = (current_time - original_time).total_seconds()
        # 向下取整到最近的间隔倍数
        adjusted_diff = int(time_diff // UPDATE_INTERVAL * UPDATE_INTERVAL)
        
        # 计算目标时间
        target_time = original_time + timedelta(seconds=adjusted_diff)
        
        # 计算下一个间隔倍数的时间
        next_target = original_time + timedelta(seconds=adjusted_diff + UPDATE_INTERVAL)
        
        # 计算到下一个目标时间的倒计时
        seconds_to_next = max(0, (next_target - current_time).total_seconds())
        countdown = int(seconds_to_next) + 1
        
        return target_time, next_target, countdown
    
    @staticmethod
    def format_datetime(dt, format_str='%Y-%m-%d %H:%M:%S'):
        """格式化日期时间
        
        Args:
            dt: 日期时间对象
            format_str: 格式化字符串
            
        Returns:
            str: 格式化后的日期时间字符串
        """
        if dt is None:
            return ""
        return dt.strftime(format_str) 