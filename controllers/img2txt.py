from PIL import ImageGrab, Image
from io import BytesIO
from utils.cache_data import CacheData
from queue import Queue
import base64
import zlib
import math
import pyperclip
import queue

frame_length = 4090


def img_2_txt(msg: Queue, cache_data: CacheData):

    # mode不为0 续传模式
    if cache_data.mode != 0:
        resume(cache_data)
    else:

        img = ImageGrab.grabclipboard()
        if not isinstance(img, Image.Image):
            msg.put('剪切板为空或非图片！')
            return 1

        buffer = BytesIO()

        # todo: 复制贴到屏幕上的图片 无法以JPEG保存
        # 做一遍转换
        if img.mode != 'RGB':
            img = img.convert(mode="RGB")
        img.save(buffer, format='JPEG')

        # 图片再压缩一次
        compressed_data = zlib.compress(buffer.getvalue())

        # 字节码转字符串
        ret = base64.b64encode(compressed_data).decode("utf-16")

        if len(ret) / frame_length > 99:
            msg.put("文件分片超过100，算了吧。")
            return 1

        cache_data.mode = 1
        # 总分片数放在开头
        ret = "{:0>2}".format(math.ceil(len(ret)/frame_length)) + ret

        # 初始化总分片数、总加密数据
        cache_data.encrypted_data = ret
        cache_data.all_frame = math.ceil((len(ret))/frame_length)

        # 取第一分片
        cache_data.current_frame = 0
        cache_data.remainder_data = ret[frame_length:]
        cur_frame = ret[:frame_length]
        pyperclip.copy(cur_frame)
        cache_data.current_frame += 1

    # 判断传输完成
    if cache_data.current_frame == cache_data.all_frame:
        msg.put("传输完成！")
        # 初始化标志位
        cache_data.mode = 0

    else:
        msg.put(f"传输中：{cache_data.current_frame}/{cache_data.all_frame}  点击加密继续。")


def resume(cache_data: CacheData):

    cur_frame = cache_data.remainder_data[:frame_length]
    pyperclip.copy(cur_frame)
    cache_data.current_frame += 1
    cache_data.remainder_data = cache_data.remainder_data[frame_length:]


if __name__ == '__main__':
    _msg = queue.Queue()
    img_2_txt(_msg, CacheData())
