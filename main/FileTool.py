import json
from main.model import *

SAMPLE_POINTS_NUMS = 5 #采样频率
class FileTool():

    def __init__(self,fileurl):
        self.fileurl = fileurl

    def dict_to_json_write_file(self,coordinateDict):
        with open(self.fileurl,"w") as f:
            json.dump(coordinateDict, f,cls=ObjectEncoder)
            f.close()

    def json_to_data_read(self):
        points = []
        index = 0
        with open(self.fileurl,'r') as f:
            dict = json.load(f)
            for k,v in dict.items():
                for item in v:
                    if(index % 5 == 0):
                        point = Point(x=item['x'],y=item['y'],statue=item['statue'])
                        points.append(point)
                    index += 1

        return points

if __name__ == '__main__':
    filet = FileTool('lujing.json')

