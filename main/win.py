import cv2
import numpy as np
from main.filetool import *
from main.predict_lines import *

#当鼠标按下时变为 True
drawing = False
pointList = []
index = 0
pointdict = {}
saveStatue = False
PROCESSING = False
THRELD_LINES = 20
IMAGE_NAME = "image"

#创建失效后的函数
def draw_none(event, x, y, flags, param):
    pass

# 创建回调函数
def draw_circle(event, x, y, flags, param):
    global drawing,index,pointList,pointdict
    # 当按下左键是返回起始位置坐标
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(img, (x, y), 5, (255, 0, 0), -1)#设置起始点
        point = Point(x,y,'S')
        pointList.append(point)
        drawing = True
    elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
        if drawing == True:
            cv2.circle(img, (x, y), 2, (0, 0, 0), -1)
            point = Point(x, y, 'N')
            pointList.append(point)
    elif event == cv2.EVENT_LBUTTONUP:
        if drawing == True:
            if len(pointList) > THRELD_LINES:#点数超过20个才选为合理区域
                index += 1
                pointdict[index] = pointList
            point_len = len(pointList)-1
            for s in range(point_len):
                cv2.line(img,(pointList[s].x,pointList[s].y),(pointList[s+1].x,pointList[s+1].y),(0, 0, 0), 2)
            pointList = []
            drawing = False

img = np.ones((512, 512, 3), np.uint8) * 255
cv2.namedWindow(IMAGE_NAME)
cv2.setMouseCallback(IMAGE_NAME, draw_circle)


while (True):
    cv2.imshow('image', img)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:#按esc结束
        break
    elif k == ord('p') and PROCESSING == False:#按p进行分类
        if saveStatue == True:
            #分类
            print("正在分类......")
            pl = PredictLine()
            result = pl.predict_line("lujing.json")

            print("分类完成......")
            PROCESSING = True
        else:
            print("正在保存所画区域")
            #写入json文件
            file = FileTool("lujing.json")
            file.dict_to_json_write_file(pointdict)
            # 设置鼠标画图失效
            cv2.setMouseCallback(IMAGE_NAME, draw_none)
            saveStatue = True
            print("保存完成共"+str(index)+"条路径，请重新按p键分类")
    elif k == ord('c'):#清空画图区域
        img = np.ones((512, 512, 3), np.uint8) * 255
        cv2.setMouseCallback(IMAGE_NAME, draw_circle)
        pointdict.clear()
        index=0
        saveStatue = False
        PROCESSING = False

cv2.destroyAllWindows()