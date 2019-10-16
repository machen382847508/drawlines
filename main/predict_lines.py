from main.filetool import *
import numpy as np
import cv2

THRESHOLD_SIZE = 41.2
NEW_IMAGE = "result"

class PredictLine:
    #从data的points中获取X轴和Y轴的数据
    def __init__(self):
        pass

    #获取图中所有值写入dataMat中
    def readData(self,points:dict):
        dataMatX = []
        dataMatY = []

        for k,v in points.items():
            datax = []  # 存放一组路径的x值
            datay = []  # 存放一组路径的y值
            for item in v:
                datax.append(item.x)
                datay.append(item.y)
            dataMatX.append(datax)
            dataMatY.append(datay)

        return dataMatX,dataMatY

    def featureScal(self,dataMat):
        for row in range(len(dataMat)):
            dataArray = np.array(dataMat[row])
            maxNum = np.max(dataArray)
            # minNum = np.min(dataArray)
            # divNum = maxNum - minNum
            # minMat = np.ones(len(dataMat[row])) * minNum
            b = np.ones(len(dataMat[row])) * maxNum
            dataMat[row] = dataArray / b
        return dataMat

    #计算欧式距离
    def cal2dotsdistance(self,dot1,dot2):
        d1 = np.array(dot1)
        d2 = np.array(dot2)
        #ou = np.linalg.norm(d1 - d2, ord=1)
        ou = np.linalg.norm(d1 - d2)
        return ou

    #求两条路径最小距离DTW算法
    def calDisMat(self,dataMatX1,dataMatX2,dataMatY1,dataMatY2):
        len1 = np.size(dataMatX1)
        len2 = np.size(dataMatX2)
        pointDist = np.zeros([len1,len2])
        for i in range(len1):
            for j in range(len2):
                pointDist[i, j] = self.cal2dotsdistance([dataMatX1[i],dataMatY1[i]],[dataMatX2[j],dataMatY2[j]])
        realmax = 1000
        cost = np.ones([len1, len2]) * realmax
        cost[0, 0] = pointDist[0, 0]
        for i in range(1,len1):
            for j in range(len2):
                cost1 = cost[i-1,j]
                if j >= 1:
                    cost2 = cost[i,j-1]
                else:
                    cost2 = realmax
                if(i>=1 and j>=1):
                    cost3 = cost[i-1,j-1]
                else:
                    cost3 = realmax
                cost[i,j] = pointDist[i,j] + np.min([cost1,cost2,cost3])
        result = cost[len1-1,len2-1]/(len1+len2) * 2
        return result

    def getPathSorted(self, pathAlike):
        lenMatrx = len(pathAlike)
        used = []
        for x in range(lenMatrx):
            used.append(1)
        pathClass = []
        for i in range(lenMatrx):
            a2 = []
            if (used[i] == 1):
                a2.append(i)
                used[i] = 0  # 标记为被使用
            for j in range(i + 1, lenMatrx):
                if (pathAlike[i, j] == 1):
                    if (j not in a2 and used[j] == 1):
                        a2.append(j)
                        used[j] = 0
                    for x in range(0, lenMatrx):
                        if (pathAlike[j, x] == 1):
                            if (x not in a2 and used[x] == 1):
                                a2.append(x)
                                used[x] = 0  # 标记为被使用
            if (len(a2)):
                pathClass.append(a2)

        for i in range(len(pathClass)):
            pathClass[i] = [i + 1 for i in pathClass[i]]
        return pathClass


    def predict_line(self,file):
        filet = FileTool(file)
        pl = PredictLine()
        ll = filet.json_to_data_read2()
        dmx, dmy = pl.readData(ll)
        # dmx = pl.featureScal(dmx)
        # dmy = pl.featureScal(dmy)
        pNum = len(dmx)
        pathSorted = np.zeros([pNum,pNum])
        for i in range(pNum):
            for j in range(pNum):
                pathDis = self.calDisMat(dmx[i], dmx[j], dmy[i], dmy[j])
                # print(i+1,"-",j+1,":",pathDis)
                if pathDis < float(THRESHOLD_SIZE):
                    pathSorted[i,j] = 1
        pathClass = self.getPathSorted(pathSorted)
        return pathClass

if __name__ == '__main__':
    pl = PredictLine()
    result = pl.predict_line("lujing.json")
    newimage = np.ones((512, 512, 3), np.uint8) * 255
    cv2.namedWindow(NEW_IMAGE)

    Ffile = FileTool("lujing.json")
    pointsdict = Ffile.json_to_data_read2()
    datax,datay = pl.readData(pointsdict)
    len_data = len(datax)
    colors = []
    for i in range(len(result)):
        print("第" + str(i + 1) + "类为：", result[i])
        colors.append((np.random.randint(0,255),np.random.randint(0,255),np.random.randint(0,255)))

    for i in range(len(result)):
        for item in result[i]:
            for m in range(len(datax[item-1])-1):
                cv2.line(newimage,(int(datax[item-1][m]),int(datay[item-1][m])),(int(datax[item-1][m+1]),int(datay[item-1][m+1])),colors[i], 2)
            cv2.putText(newimage, str(item), (datax[item - 1][0], datay[item - 1][0]), cv2.FONT_HERSHEY_COMPLEX, 1,
                    (0, 0, 0), 1)
    cv2.imshow(NEW_IMAGE, newimage)
    k = cv2.waitKey(0) & 0xFF