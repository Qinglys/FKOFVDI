import queue
import threading

from views.layout import WinGUI
from controllers import img2txt, txt2img
from utils import cache_data


class Win(WinGUI):
    def __init__(self):
        super().__init__()
        self.__event_bind()
        self.cache_data = cache_data.CacheData()
        self.msg = queue.Queue()

    def __event_bind(self):
        self.tk_label_msg.bind(sequence="<Button-1>", func=self._onclick_label)
        self.tk_button_encode.bind("<Button-1>", self._onclick_encode)
        self.tk_button_decode.bind("<Button-1>", self._onclick_decode)
        self.tk_label_zip.bind("<Button-1>", self._onclick_label_zip)

    def set_msg(self, event=False):
        while True:

            # 控制auto标识
            if self.cache_data.auto_thread_flag:
                self.tk_label_auto.place(x=0, y=15, width=15, height=16)
            else:
                self.tk_label_auto.place_forget()
            
            txt = self.msg.get()
            if txt == "--refresh":
                continue
            # print(txt)
            self.tk_label_msg.config(text=txt)

    def _onclick_encode(self, event):
        if self.cache_data.mode != 0 and self.cache_data.mode != 1:
            self.msg.put("当前接收模式进行中，点此中断。")
            # print(self.cache_data.mode)
            return
        img2txt.img_2_txt(self.msg, self.cache_data)

    def _onclick_decode(self, event):
        if self.cache_data.mode != 0 and self.cache_data.mode != 2:
            self.msg.put("当前发送模式进行中，点此中断。")
            return
        txt2img.txt_2_img(self.msg, self.cache_data)

    def _onclick_label(self, event):
        if self.cache_data.mode == 0:
            self.msg.put("已经重置过了！")
            return
        # 重新初始化缓存
        self.cache_data.__init__()
        self.msg.put("已重置！")

    def _onclick_label_zip(self, event):
        if self.cache_data.is_zip:
            self.tk_label_zip.config(text="BMP")
            self.cache_data.is_zip = 0
        else:
            self.tk_label_zip.config(text="JPEG")
            self.cache_data.is_zip = 1

if __name__ == '__main__':
    win = Win()
    threading.Thread(target=win.set_msg, daemon=True).start()
    win.mainloop()