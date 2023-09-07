from tkinter import *
from tkinter.ttk import *
from typing import Dict


class WinGUI(Tk):
    def __init__(self):
        super().__init__()
        self.__win()
        self.tk_label_msg = self.__tk_label_msg(self)
        self.tk_button_encode = self.__tk_button_encode(self)
        self.tk_button_decode = self.__tk_button_decode(self)

    def __win(self):
        self.title("F**KOFVDI")
        # 设置窗口大小、居中
        width = 322
        height = 110
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)
        self.resizable(width=False, height=False)
        # 自动隐藏滚动条

    def scrollbar_autohide(self, bar, widget):
        self.__scrollbar_hide(bar, widget)
        widget.bind("<Enter>", lambda e: self.__scrollbar_show(bar, widget))
        bar.bind("<Enter>", lambda e: self.__scrollbar_show(bar, widget))
        widget.bind("<Leave>", lambda e: self.__scrollbar_hide(bar, widget))
        bar.bind("<Leave>", lambda e: self.__scrollbar_hide(bar, widget))

    def __scrollbar_show(self, bar, widget):
        bar.lift(widget)

    def __scrollbar_hide(self, bar, widget):
        bar.lower(widget)

    def vbar(self, ele, x, y, w, h, parent):
        sw = 15  # Scrollbar 宽度
        x = x + w - sw
        vbar = Scrollbar(parent)
        ele.configure(yscrollcommand=vbar.set)
        vbar.config(command=ele.yview)
        vbar.place(x=x, y=y, width=sw, height=h)
        self.scrollbar_autohide(vbar, ele)

    def __tk_label_msg(self, parent):
        label = Label(parent, text="-", anchor="center", )
        label.place(x=19, y=10, width=280, height=30)
        return label

    def __tk_button_encode(self, parent):
        btn = Button(parent, text="编码", takefocus=False, )
        btn.place(x=40, y=64, width=100, height=30)
        return btn

    def __tk_button_decode(self, parent):
        btn = Button(parent, text="解码", takefocus=False, )
        btn.place(x=180, y=64, width=98, height=30)
        return btn


class Win(WinGUI):
    def __init__(self):
        super().__init__()
        self.__event_bind()

    def __event_bind(self):
        pass


if __name__ == "__main__":
    win = Win()
    win.mainloop()