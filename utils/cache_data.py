class CacheData:
    def __init__(self):
        self.remainder_data = ""
        self.current_frame = 0
        self.all_frame = 0
        self.encrypted_data = ""
        self.latest_frame = ""
        self.mode = 0  # 0:无状态 1:发送模式 2:接收模式
