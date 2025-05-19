# BUPT_UCloud_AttendanceQR_Simulator

这是一个动态签到二维码模拟生成器程序，仿照北京邮电大学教学云平台授课端的动态签到功能。该程序可以根据用户输入的课程名称和相关参数自动生成签到二维码（仅为模拟，并没有实际作用），或者从剪贴板读取现有二维码，并实时更新二维码中的时间戳。

## 功能特点

- 仿照北邮教学云平台授课端的动态签到二维码
- 支持手动设置课程名称并生成随机签到码
- 支持自定义ID、站点ID和课程ID（留空时自动随机生成）
- 支持从剪贴板读取现有二维码图像
- 实时更新二维码中的时间戳，保持签到码动态刷新
- 自动计算并显示倒计时

## 项目结构

```
QRSignSimulator/
├── __init__.py
├── app.py              # 应用程序入口
├── config/             # 配置模块
│   ├── __init__.py
│   └── settings.py     # 应用程序设置
├── core/               # 核心功能模块
│   ├── __init__.py
│   ├── clipboard.py    # 剪贴板管理
│   ├── sign_generator.py # 签到码生成器
│   └── qr_processor.py # 二维码处理
├── ui/                 # 用户界面模块
│   ├── __init__.py
│   ├── dialogs.py      # 对话框
│   └── main_window.py  # 主窗口UI
└── utils/              # 工具模块
    ├── __init__.py
    ├── image_utils.py  # 图像处理工具
    └── time_utils.py   # 时间处理工具
```

## 依赖项

- Python 3.6+
- OpenCV
- qrcode
- Pillow
- numpy
- pytz
- python-dateutil

## 安装

1. 克隆仓库：

```bash
git clone https://github.com/Yokumii/BUPT_UCloud_AttendanceQR_Simulator.git
cd BUPT_UCloud_AttendanceQR_Simulator
```

2. 安装依赖：

```bash
pip install -r requirements.txt
```

## 使用方法

运行主程序：

```bash
python main.py
```

### 方法一：手动设置课程名称（仅为模拟，并没有实际作用）
1. 点击"设置课程名称"按钮，在弹出的对话框中输入课程名称
2. (可选) 点击"高级设置"按钮，可以自定义ID、站点ID和课程ID，留空将自动随机生成
3. 点击"生成签到码"按钮，系统会自动生成签到码
4. 点击"开始实时生成"按钮，应用程序将实时更新二维码中的时间戳

### 方法二：从剪贴板读取
1. 复制一个包含二维码的图像到剪贴板
2. 点击"从剪贴板读取"按钮，系统会自动识别二维码
3. 点击"开始实时生成"按钮，应用程序将实时更新二维码中的时间戳
4. 点击"停止生成"按钮停止生成

## 运行效果

1. 从剪切板中读取二维码；

![](https://cdn.jsdelivr.net/gh/Yokumii/MyPicBucket@img/img/202505191735291.png)

2. 程序会自动计算并更新后续的二维码；

![](https://cdn.jsdelivr.net/gh/Yokumii/MyPicBucket@img/img/202505191736242.png)

3. 可以通过企业微信扫描并验证 **（注意，仅验证功能的正确性，不得用于其他不合规的用途）**；

![](https://cdn.jsdelivr.net/gh/Yokumii/MyPicBucket@img/img/202505191738146.png)

## 开发进度

详细的版本更新记录请查看 [CHANGELOG.md](./CHANGELOG.md)

目前最新版本：v1.0.0 (2025-05-19)
- 完成基本功能开发
- 实现二维码生成与实时更新
- 支持从剪贴板读取现有二维码
- 在 MacOS 系统上测试通过

## 注意事项

本项目仅供学习使用，模拟了北京邮电大学教学云平台的动态签到码的生成。如因个人的不当或不合规的使用产生期望之外的后果，与作者无关。