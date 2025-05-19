"""
动态签到码模拟生成器应用程序入口
"""

import tkinter as tk
import sys
import os

# 确保可以导入模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from QRSignSimulator.ui.main_window import MainWindow


def main():
    """应用程序主入口"""
    # 创建主窗口
    root = tk.Tk()
    app = MainWindow(root)
    
    # 启动事件循环
    root.mainloop()


if __name__ == "__main__":
    main() 