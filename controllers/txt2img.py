import pyperclip
import base64
import zlib
from PIL import Image
from queue import Queue
from utils.cache_data import CacheData
import io
import win32clipboard


def encrypt2bmp(msg: Queue, encrypt_str: str):

    # 编码 utf-16 -> ascii
    encrypt_byte = encrypt_str[2:].encode("utf-16")

    # base64 解码 ascii > 二进制
    try:
        zip_img = base64.b64decode(encrypt_byte)
    except Exception:
        msg.put("BASE64解码失败！")
        return None

    # 解压 -> JPEG格式二进制数据
    try:
        img_binary = zlib.decompress(zip_img)
    except Exception:
        msg.put("解压失败！")
        return None

    # JPEG -> Image对象
    img = Image.open(io.BytesIO(img_binary))
    # print(img.mode, type(img.mode))

    # image对象 -> 字节对象
    buffer = io.BytesIO()
    img.save(buffer, format("BMP"))

    # 返回图像字节码
    return buffer.getvalue()[14:]


def sent2clipboard(data):
    # 复制到剪切板
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)  # 开头的14个字节不需要
    win32clipboard.CloseClipboard()


def txt_2_img(msg: Queue, cache_data: CacheData):

    encrypt_str = pyperclip.paste()
    # 简单判断
    if type(encrypt_str) != str or encrypt_str == '':
        msg.put("复制内容错误！")
        return

    if cache_data.mode != 0:
        resume(msg, cache_data, encrypt_str)
    else:
        try:
            all_frame = int(encrypt_str[:2])
        except ValueError:
            msg.put("header验证错误！")
            return
        # 有多帧
        if all_frame > 1:
            cache_data.all_frame = all_frame
            cache_data.encrypted_data = encrypt_str
            cache_data.latest_frame = encrypt_str
            cache_data.mode = 2
            cache_data.current_frame = 1
            msg.put(f"接收中：{cache_data.current_frame}/{cache_data.all_frame}")
            return
        # 单帧
        else:
            data = encrypt2bmp(msg, encrypt_str)
            if data is None:
                return
            sent2clipboard(data)
            cache_data.mode = 0
            msg.put("解码完成，已复制到剪切板！")


def resume(msg: Queue, cache_data: CacheData, encrypt_str: str):

    if encrypt_str == cache_data.latest_frame:
        msg.put("已经处理过这个分片了！")
        return

    cache_data.encrypted_data += encrypt_str
    cache_data.current_frame += 1

    # 全部帧接收完成
    if cache_data.current_frame == cache_data.all_frame:
        date = encrypt2bmp(msg, cache_data.encrypted_data)
        if date is None:
            return
        sent2clipboard(date)
        cache_data.mode = 0
        msg.put("解码完成，已复制到剪切板！")
    else:
        msg.put(f"接收中：{cache_data.current_frame}/{cache_data.all_frame}")