import queue
import threading

from views.layout import WinGUI
from controllers import img2txt, txt2img
from utils import cache_data


class Win(WinGUI):
    def __init__(self):
        super().__init__()
        self.__event_bind()
        self.cache_date = cache_data.CacheData()
        self.msg = queue.Queue()

    def __event_bind(self):
        self.tk_label_msg.bind(sequence="<Button-1>", func=self._onclick_label)
        self.tk_button_encode.bind("<Button-1>", self._onclick_encode)
        self.tk_button_decode.bind("<Button-1>", self._onclick_decode)

    def set_msg(self, event=False):
        while True:
            txt = self.msg.get()
            print(txt)
            self.tk_label_msg.config(text=txt)

    def _onclick_encode(self, event):
        if self.cache_date.mode != 0 and self.cache_date.mode != 1:
            self.msg.put("当前接收模式进行中，点此中断。")
            # print(self.cache_date.mode)
            return
        img2txt.img_2_txt(self.msg, self.cache_date)

    def _onclick_decode(self, event):
        if self.cache_date.mode != 0 and self.cache_date.mode != 2:
            self.msg.put("当前发送模式进行中，点此中断。")
            return
        txt2img.txt_2_img(self.msg, self.cache_date)

    def _onclick_label(self, event):
        if self.cache_date.mode == 0:
            self.msg.put("已经重置过了！")
            return
        # 重新初始化一个缓存对象
        self.cache_date = cache_data.CacheData()
        self.msg.put("已重置！")


if __name__ == '__main__':
    win = Win()
    threading.Thread(target=win.set_msg, daemon=True).start()
    win.mainloop()