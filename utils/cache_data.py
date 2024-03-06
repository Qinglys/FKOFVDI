class CacheData:
    __slots__ = "remainder_data", "current_frame", "all_frame", "encrypted_data", "latest_frame", "mode", "auto_thread_flag", "is_zip"
    def __init__(self):
        self.remainder_data = ""
        self.current_frame = 0
        self.all_frame = 0
        self.encrypted_data = ""
        self.latest_frame = ""
        self.mode = 0  # 0:无状态 1:发送模式 2:接收模式
        self.auto_thread_flag = 0  # 自动化线程一次只能有一个
        self.is_zip = 0 # 是否使用jpeg格式 默认用BMP
