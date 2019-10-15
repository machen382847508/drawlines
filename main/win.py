import cv2
from main.predict_lines import *
import numpy as np

#当鼠标按下时变为 True
drawing = False
pointList = []
index = 0
pointdict = {}
saveStatue = False
PROCESSING = False
THRELD_LINES = 20
IMAGE_NAME = "image"
NEW_IMAGE = "result"
FILE_NAME = "lujing.json"

#创建失效后的函数
def draw_none(event, x, y, flags, param):
    pass

# 创建回调函数
def draw_circle(event, x, y, flags, param):
    global drawing,index,pointList,pointdict
    startX = 0
    startY = 0
    # 当按下左键是返回起始位置坐标
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(img, (x, y), 5, (255, 0, 0), -1)#设置起始点
        startX = x
        startY = y
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
                cv2.putText(img,str(index), (pointList[0].x, pointList[0].y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 1)
                pointdict[index] = pointList
            point_len = len(pointList)-1
            for s in range(point_len):
                cv2.line(img,(pointList[s].x,pointList[s].y),(pointList[s+1].x,pointList[s+1].y),(0, 0, 0), 2)
            pointList = []
            drawing = False

img = np.ones((512, 512, 3), np.uint8) * 255
cv2.namedWindow(IMAGE_NAME)
cv2.setMouseCallback(IMAGE_NAME, draw_circle)


while True:
    cv2.imshow('image', img)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:#按esc结束
        break
    elif k == ord('p') and PROCESSING == False:#按p进行分类
        if saveStatue == True:
            #分类
            print("正在分类......")
            pl = PredictLine()
            Ffile = FileTool(FILE_NAME)
            fcontents = Ffile.json_to_data_read2()
            datax, datay = pl.readData(fcontents)
            result = pl.predict_line(FILE_NAME)
            colors = []
            len_results = len(result)
            for i in range(len_results):
                print("第"+str(i+1)+"类为：",result[i])
                colors.append((np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255)))
            print("分类完成......")
            img = np.ones((512, 512, 3), np.uint8) * 255
            for i in range(len(result)):
                for item in result[i]:
                    for m in range(len(datax[item - 1]) - 1):
                        cv2.line(img, (int(datax[item - 1][m]), int(datay[item - 1][m])),
                                 (int(datax[item - 1][m + 1]), int(datay[item - 1][m + 1])), colors[i], 2)
                    cv2.putText(img, str(item), (datax[item - 1][0], datay[item - 1][0]), cv2.FONT_HERSHEY_COMPLEX, 1,
                                (0, 0, 0), 1)
            PROCESSING = True

        else:
            print("正在保存所画区域")
            #写入json文件
            file = FileTool(FILE_NAME)
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