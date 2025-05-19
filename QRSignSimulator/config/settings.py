"""
应用程序配置文件
"""

# 应用程序设置
APP_TITLE = "动态签到码模拟生成器"
APP_WIDTH = 800
APP_HEIGHT = 600

# 二维码设置
QR_VERSION = 1
QR_ERROR_CORRECTION = "L"  # L, M, Q, H
QR_BOX_SIZE = 10
QR_BORDER = 4
QR_FILL_COLOR = "black"
QR_BACK_COLOR = "white"

# 图像设置
IMAGE_MAX_WIDTH = 600
IMAGE_MAX_HEIGHT = 400

# 时间设置
TIME_ZONE = 'Asia/Shanghai'
UPDATE_INTERVAL = 5  # 更新间隔（秒）
REFRESH_RATE = 0.1  # 刷新率（秒）

# 签到二维码设置
QR_TEMPLATE = "checkwork|id={id}&siteId={site_id}&createTime={create_time}&classLessonId={class_lesson_id}"
ID_LENGTH = 19  # ID长度
CLASS_LESSON_ID_LENGTH = 19  # 课程ID长度
DEFAULT_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"  # 默认时间格式 