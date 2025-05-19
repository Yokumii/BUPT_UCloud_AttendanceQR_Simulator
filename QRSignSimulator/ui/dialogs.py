"""
对话框模块
提供各种用户交互对话框
"""

import tkinter as tk
from tkinter import simpledialog


class InputDialogs:
    """输入对话框类"""
    
    @staticmethod
    def get_course_name(parent):
        """获取用户输入的课程名称
        
        Args:
            parent: 父窗口
            
        Returns:
            str: 用户输入的课程名称，如果取消则返回None
        """
        return simpledialog.askstring(
            title="输入课程名称",
            prompt="请输入课程名称：",
            parent=parent
        )
    
    @staticmethod
    def get_custom_id(parent, title="自定义ID", prompt="请输入自定义ID：", default=""):
        """获取用户输入的自定义ID
        
        Args:
            parent: 父窗口
            title: 对话框标题
            prompt: 提示文本
            default: 默认值
            
        Returns:
            str: 用户输入的ID，如果取消则返回None
        """
        return simpledialog.askstring(
            title=title,
            prompt=prompt,
            initialvalue=default,
            parent=parent
        )
    
    @staticmethod
    def show_advanced_settings(parent):
        """显示高级设置对话框
        
        Args:
            parent: 父窗口
            
        Returns:
            dict: 包含自定义设置的字典，如果取消则返回None
        """
        # 创建一个顶层窗口作为对话框
        dialog = tk.Toplevel(parent)
        dialog.title("高级设置")
        dialog.geometry("400x200")
        dialog.transient(parent)  # 设置为父窗口的临时窗口
        dialog.grab_set()  # 模态对话框
        
        # 设置窗口在父窗口中居中
        dialog.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - dialog.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # 创建表单
        tk.Label(dialog, text="ID (留空将随机生成):").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        id_entry = tk.Entry(dialog, width=30)
        id_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(dialog, text="站点ID (留空将随机生成):").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        site_id_entry = tk.Entry(dialog, width=30)
        site_id_entry.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(dialog, text="课程ID (留空将随机生成):").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        class_lesson_id_entry = tk.Entry(dialog, width=30)
        class_lesson_id_entry.grid(row=2, column=1, padx=10, pady=5)
        
        # 结果变量
        result = {"cancelled": True}
        
        def on_ok():
            result["cancelled"] = False
            result["id"] = id_entry.get().strip()
            result["site_id"] = site_id_entry.get().strip()
            result["class_lesson_id"] = class_lesson_id_entry.get().strip()
            dialog.destroy()
        
        def on_cancel():
            dialog.destroy()
        
        # 按钮区域
        button_frame = tk.Frame(dialog)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ok_button = tk.Button(button_frame, text="确定", command=on_ok, width=10)
        ok_button.pack(side=tk.LEFT, padx=10)
        
        cancel_button = tk.Button(button_frame, text="取消", command=on_cancel, width=10)
        cancel_button.pack(side=tk.LEFT, padx=10)
        
        # 等待对话框关闭
        parent.wait_window(dialog)
        
        # 如果用户取消，返回None
        if result["cancelled"]:
            return None
        
        return result 