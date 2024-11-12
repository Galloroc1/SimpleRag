import logging
# 配置日志记录器
logging.basicConfig(
    level=logging.DEBUG,  # 设置日志级别为DEBUG
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # 设置日志格式
    filename='answer_llm.log',  # 将日志写入文件
    filemode='w'  # 写入模式，'w' 表示覆盖现有文件
)

# 创建一个日志记录器
logger = logging.getLogger('../log/infor.log')
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(console_handler)