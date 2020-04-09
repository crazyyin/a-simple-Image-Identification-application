# -*- coding: utf-8 -*-


'''
  首先需要明确一件最重要的事情： 我是一个懒人。对于写台账这种体力活，一定是需要让电脑直接去写的。
  对于台账我们可以知道的是：绝大多数数据都存在于重要事项说明书中。这就涉及到了重说数据读取
  我将重说看成最基本的图像。所面临的问题就变成了从图像中读取对应点位的数据

'''

import pytesseract,os,pythoncom,pyHook,sys,pyperclip
reload(sys)
sys.setdefaultencoding('utf8')
from PIL import Image
from PIL import ImageGrab
# 图像转文字
def ocr(path):
    image=Image.open(path)
    text = pytesseract.image_to_string(image,lang='jpn')
    print(text)
    pyperclip.copy(text)
    return text

# 文字输入到剪切板え
def put_into_clipboard(text):
    command='echo ' + text.strip() + '| clip'
    os.system(command)
# 截图e
def prt_scn(path,x,y,w,h):

    pic=ImageGrab.grab(bbox=(x,y,w,h))
    pic.save(path)

# 图片裁剪功能
def pic_cut(path_in,path_out,left,top,right,lower):
    img = Image.open(path_in)

    cropped = img.crop((left,top,right,lower))  # (left, upper, right, lower)
    cropped.save(path_out)


# 创建全局变量，以便储存鼠标Down 和 Up 时的坐标
positionDown = ()
position = ()


# 鼠标左键按下触发
def onMouseEventDown(event):
    global positionDown
    positionDown = event.Position
    return True


# 鼠标左键松开触发
def onMouseEventUp(event):
    global positionDown
    global position
    position = positionDown + event.Position
    return True


# 截屏方法e
def printScreen(position):
    im = ImageGrab.grab(position)
    im.save('C:\\Users\\user\\Desktop\\printscreen.jpg')

    return True

# 获取键盘值方法
def onKeyboardEvent(event):
    if (event.Key == 'E'):

        global position
        if position is not None:
            printScreen(position)
            ocr('C:\\Users\\user\\Desktop\\printscreen.jpg')

    return True


# 主方法
def main():
    hm = pyHook.HookManager()
    hm.KeyDown = onKeyboardEvent
    hm.MouseAllButtonsDown = onMouseEventDown
    hm.MouseAllButtonsUp = onMouseEventUp
    hm.HookMouse()
    hm.HookKeyboard()

    pythoncom.PumpMessages()


if __name__ == "__main__":
    main()



