"""
主窗口UI模块
负责用户界面的构建和交互
仿照北京邮电大学教学云平台授课端的动态签到功能
"""

import tkinter as tk
from tkinter import Label, Button, Frame
import threading
import numpy as np
import time
import io
import cv2

from QRSignSimulator.config.settings import APP_TITLE, APP_WIDTH, APP_HEIGHT, REFRESH_RATE
from QRSignSimulator.core.qr_processor import QRCodeProcessor
from QRSignSimulator.core.sign_generator import SignGenerator
from QRSignSimulator.core.clipboard import ClipboardManager
from QRSignSimulator.utils.image_utils import ImageProcessor
from QRSignSimulator.utils.time_utils import TimeManager
from QRSignSimulator.ui.dialogs import InputDialogs


class MainWindow:
    """主窗口类"""
    
    def __init__(self, root):
        """初始化主窗口
        
        Args:
            root: Tkinter根窗口
        """
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        
        # 设置变量
        self.qr_template = None
        self.original_time_format = None
        self.original_time = None  # 原始时间（模板二维码中的时间或生成签到码的时间）
        self.generation_time = None  # 签到码生成的时间（仅在手动设置模式下使用）
        self.last_update_time = None
        self.is_running = False
        self.generation_thread = None
        self.course_name = None
        self.custom_id = None
        self.custom_site_id = None
        self.custom_class_lesson_id = None
        self.using_template = False  # 标记是否使用模板二维码
        
        # 创建组件
        self.qr_processor = QRCodeProcessor()
        self.image_processor = ImageProcessor()
        self.time_manager = TimeManager()
        self.sign_generator = SignGenerator()
        
        # 创建UI
        self.setup_ui()
    
    def setup_ui(self):
        """设置UI组件"""
        # 顶部控制区域
        control_frame = Frame(self.root)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 设置课程名称按钮
        self.course_btn = Button(control_frame, text="设置课程名称", command=self.set_course_name)
        self.course_btn.pack(side=tk.LEFT, padx=5)
        
        # 高级设置按钮
        self.advanced_btn = Button(control_frame, text="高级设置", command=self.show_advanced_settings)
        self.advanced_btn.pack(side=tk.LEFT, padx=5)
        
        # 生成签到码按钮
        self.generate_btn = Button(control_frame, text="生成签到码", command=self.generate_sign_code)
        self.generate_btn.pack(side=tk.LEFT, padx=5)
        
        # 从剪贴板读取图片按钮
        self.clipboard_btn = Button(control_frame, text="从剪贴板读取", command=self.read_from_clipboard)
        self.clipboard_btn.pack(side=tk.LEFT, padx=5)
        
        # 开始生成按钮
        self.start_btn = Button(control_frame, text="开始实时生成", command=self.start_generation, state=tk.DISABLED)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        # 停止生成按钮
        self.stop_btn = Button(control_frame, text="停止生成", command=self.stop_generation, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        # 状态标签
        self.status_label = Label(self.root, text="请设置课程名称或从剪贴板读取二维码")
        self.status_label.pack(pady=5)
        
        # 课程信息标签
        self.course_label = Label(self.root, text="当前课程: 未设置")
        self.course_label.pack(pady=5)
        
        # 高级设置信息标签
        self.advanced_label = Label(self.root, text="高级设置: 所有参数将随机生成")
        self.advanced_label.pack(pady=5)
        
        # 二维码信息标签
        self.qr_info_label = Label(self.root, text="")
        self.qr_info_label.pack(pady=5)
        
        # 当前时间标签
        self.time_label = Label(self.root, text="")
        self.time_label.pack(pady=5)
        
        # 二维码显示区域
        self.qr_label = Label(self.root)
        self.qr_label.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
    
    def set_course_name(self):
        """设置课程名称"""
        course_name = InputDialogs.get_course_name(self.root)
        if course_name:
            self.course_name = course_name
            self.course_label.config(text=f"当前课程: {course_name}")
            self.status_label.config(text="课程名称已设置，请点击\"生成签到码\"按钮")
            # 重置模板标记
            self.using_template = False
        else:
            self.status_label.config(text="未输入课程名称")
    
    def show_advanced_settings(self):
        """显示高级设置对话框"""
        settings = InputDialogs.show_advanced_settings(self.root)
        if settings:
            self.custom_id = settings["id"] if settings["id"] else None
            self.custom_site_id = settings["site_id"] if settings["site_id"] else None
            self.custom_class_lesson_id = settings["class_lesson_id"] if settings["class_lesson_id"] else None
            
            # 更新高级设置标签
            advanced_info = []
            if self.custom_id:
                advanced_info.append(f"ID: {self.custom_id}")
            if self.custom_site_id:
                advanced_info.append(f"站点ID: {self.custom_site_id}")
            if self.custom_class_lesson_id:
                advanced_info.append(f"课程ID: {self.custom_class_lesson_id}")
            
            if advanced_info:
                self.advanced_label.config(text=f"高级设置: {', '.join(advanced_info)}")
            else:
                self.advanced_label.config(text="高级设置: 所有参数将随机生成")
            
            self.status_label.config(text="高级设置已更新")
            # 重置模板标记
            self.using_template = False
    
    def generate_sign_code(self):
        """生成签到码"""
        try:
            # 生成签到数据
            sign_data, now, time_str = self.sign_generator.generate_sign_data(
                course_name=self.course_name,
                custom_id=self.custom_id,
                custom_site_id=self.custom_site_id,
                custom_class_lesson_id=self.custom_class_lesson_id
            )
            
            # 保存模板和原始格式
            self.qr_template = sign_data
            self.original_time_format = time_str
            self.original_time = now
            self.generation_time = now  # 保存生成时间，用于手动设置模式
            
            # 显示二维码信息
            self.qr_info_label.config(text=f"签到码: {sign_data[:50]}...")
            
            # 生成并显示二维码
            self.generate_and_display(now)
            
            # 启用开始按钮
            self.start_btn.config(state=tk.NORMAL)
            self.status_label.config(text="签到码已生成，点击\"开始实时生成\"按钮")
            
            # 重置模板标记
            self.using_template = False
            
        except Exception as e:
            self.status_label.config(text=f"生成签到码错误: {str(e)}")
    
    def read_from_clipboard(self):
        """从剪贴板读取图片并识别二维码"""
        try:
            # 禁用按钮，防止多次点击
            self.clipboard_btn.config(state=tk.DISABLED)
            
            self.status_label.config(text="正在从剪贴板读取图片...")
            self.root.update()
            
            # 获取剪贴板图片
            clipboard_img, img_array = ClipboardManager.get_clipboard_image()
            
            if clipboard_img is None:
                self.status_label.config(text="剪贴板中没有图片")
                self.clipboard_btn.config(state=tk.NORMAL)
                return
            
            # 显示剪贴板图片
            img_tk = self.image_processor.convert_to_tkimage(img_array)
            if img_tk:
                self.qr_label.config(image=img_tk)
                self.qr_label.image = img_tk
            
            # 使用临时文件保存剪贴板图片
            with io.BytesIO() as output:
                clipboard_img.save(output, format="PNG")
                img_data = output.getvalue()
            
            # 尝试解码
            img_cv2 = cv2.imdecode(np.frombuffer(img_data, np.uint8), cv2.IMREAD_COLOR)
            if img_cv2 is None:
                self.status_label.config(text="无法处理剪贴板图片")
                self.clipboard_btn.config(state=tk.NORMAL)
                return
            
            qr_data = self.qr_processor.decode_qr_from_image(img_cv2)
            if not qr_data:
                self.status_label.config(text="未在剪贴板图片中检测到二维码")
                self.clipboard_btn.config(state=tk.NORMAL)
                return
            
            # 处理读取到的二维码数据
            self.process_qr_data(qr_data)
            
        except Exception as e:
            self.status_label.config(text=f"剪贴板读取错误: {str(e)}")
        finally:
            # 确保按钮重新启用
            self.clipboard_btn.config(state=tk.NORMAL)
    
    def process_qr_data(self, qr_data):
        """处理解码后的二维码数据
        
        Args:
            qr_data: 二维码数据字符串
        """
        if not qr_data:
            self.status_label.config(text="未能解码二维码")
            return
        
        # 提取createTime
        original_time, original_format = self.qr_processor.extract_create_time(qr_data)
        if not original_time:
            self.status_label.config(text="无法提取createTime")
            return
        
        # 保存模板和原始格式
        self.qr_template = qr_data
        self.original_time_format = original_format
        self.original_time = original_time
        self.generation_time = None  # 清除生成时间，因为使用模板
        
        # 设置模板标记
        self.using_template = True
        
        # 更新UI显示
        self.qr_info_label.config(text=f"模板二维码: {qr_data[:50]}... (createTime: {original_time})")
        
        # 更新课程和高级设置标签，显示正在使用模板二维码
        self.course_label.config(text="正在使用剪贴板中的模板二维码")
        self.advanced_label.config(text="使用模板二维码中的原始参数")
        
        # 启用开始按钮
        self.start_btn.config(state=tk.NORMAL)
        self.status_label.config(text="二维码模板已加载，点击\"开始实时生成\"按钮")
    
    def start_generation(self):
        """开始实时生成二维码"""
        if not self.qr_template:
            return
        
        self.is_running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.course_btn.config(state=tk.DISABLED)
        self.advanced_btn.config(state=tk.DISABLED)
        self.generate_btn.config(state=tk.DISABLED)
        self.clipboard_btn.config(state=tk.DISABLED)
        
        # 启动实时生成线程
        self.generation_thread = threading.Thread(target=self.real_time_generation, daemon=True)
        self.generation_thread.start()
    
    def stop_generation(self):
        """停止实时生成"""
        self.is_running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.course_btn.config(state=tk.NORMAL)
        self.advanced_btn.config(state=tk.NORMAL)
        self.generate_btn.config(state=tk.NORMAL)
        self.clipboard_btn.config(state=tk.NORMAL)
        
        # 根据当前模式更新状态标签
        if self.using_template:
            self.status_label.config(text="二维码生成已停止，继续使用模板二维码")
        else:
            self.status_label.config(text="二维码生成已停止")
    
    def real_time_generation(self):
        """实时生成二维码线程"""
        while self.is_running:
            try:
                # 获取当前北京时间
                beijing_now = self.time_manager.get_beijing_time()
                
                # 选择合适的基准时间
                base_time = self.original_time
                if not self.using_template and self.generation_time:
                    # 如果是手动设置模式，使用生成签到码的时间作为基准
                    base_time = self.generation_time
                
                # 计算目标时间
                target_time, next_target, countdown = self.time_manager.calculate_target_time(
                    base_time, beijing_now
                )
                
                # 更新倒计时显示
                self.root.after(0, lambda c=countdown, t=beijing_now: self.time_label.config(
                    text=f"当前时间: {self.time_manager.format_datetime(t)} (下一个二维码将在 {c} 秒后生成)"
                ))
                
                # 判断是否需要更新二维码 - 如果当前target_time与上次不同
                if self.last_update_time is None or target_time != self.last_update_time:
                    # 生成新的二维码
                    self.last_update_time = target_time
                    
                    # 生成二维码并显示
                    self.root.after(0, lambda t=target_time: self.generate_and_display(t))
                
                # 等待更短的时间，提高响应精度
                time.sleep(REFRESH_RATE)
                
            except Exception as e:
                print(f"实时生成错误: {str(e)}")
                # 在UI线程中显示错误
                self.root.after(0, lambda: self.status_label.config(text=f"生成错误: {str(e)}"))
                break
    
    def generate_and_display(self, target_time):
        """生成二维码并在UI上显示
        
        Args:
            target_time: 目标时间 (datetime对象)
        """
        try:
            # 更新状态
            self.status_label.config(text=f"正在生成 {self.time_manager.format_datetime(target_time)} 的二维码")
            
            # 更新二维码数据中的createTime
            new_data = self.qr_processor.update_create_time(
                self.qr_template, target_time, self.original_time_format
            )
            
            # 生成二维码
            qr_img = self.qr_processor.generate_qr_code(new_data)
            
            # 转换为可显示的格式
            img_array = np.array(qr_img)
            img_tk = self.image_processor.convert_to_tkimage(img_array*255)  # 二值图像需要乘以255
            
            # 在UI上显示
            self.qr_label.config(image=img_tk)
            self.qr_label.image = img_tk  # 保持引用，防止垃圾回收
            
        except Exception as e:
            print(f"生成二维码错误: {str(e)}")
            self.status_label.config(text=f"生成二维码错误: {str(e)}") 