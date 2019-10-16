from main.model import *

SAMPLE_POINTS_NUMS = 2 #采样频率

class FileTool():

    def __init__(self,fileurl):
        self.fileurl = fileurl

    def dict_to_json_write_file(self,coordinateDict):
        with open(self.fileurl,"w") as f:
            json.dump(coordinateDict, f,cls=ObjectEncoder)
            f.close()

    def json_to_data_read(self):
        points = []
        point_dict = {}
        index = 0
        with open(self.fileurl,'r') as f:
            dict = json.load(f)
            for k,v in dict.items():
                for item in v:
                    if(index % SAMPLE_POINTS_NUMS == 0):
                        point = Point(x=item['x'],y=item['y'],statue=item['statue'])
                        points.append(point)
                    index += 1
                point_dict[k] = points
                points = []
            f.close()
        return point_dict

    def json_to_data_read2(self):
        points = []
        point_dict = {}
        index = 0
        with open(self.fileurl,'r') as f:
            dict = json.load(f)
            for k,v in dict.items():
                for item in v:
                    point = Point(x=item['x'],y=item['y'],statue=item['statue'])
                    points.append(point)
                    index += 1
                point_dict[k] = points
                points = []
            f.close()
        return point_dict

