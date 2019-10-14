import json

class Point:
    def __init__(self,x,y,statue):
        self.x = x
        self.y = y
        self.statue = statue #S表示开始点，N表示其他正常点


class ObjectEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Point):
            return {'x':o.x,'y':o.y,'statue':o.statue}
        else:
            return json.JSONEncoder.default(self. o)