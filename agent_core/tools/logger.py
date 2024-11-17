import logging
# 配置日志记录器
logging.basicConfig(
    level=logging.DEBUG,  # 设置日志级别为DEBUG
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'  # 设置日志格式
)
logger = logging.getLogger('../log/infor.log')
