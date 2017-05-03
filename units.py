"""
yux
2017/4/28
"""
import numpy as np

class Distribution:
    def __init__(self, height, width, is_center = True, expand_ratio = 2 ):
        self.height = height
        self.width = width
        self.is_center = is_center
        self.expand_ratio = expand_ratio
        if is_center:
            self.data = np.array(np.zeros((height, width)), dtype=float)
        else:
            self.data = np.array(np.zeros((height*expand_ratio, width*expand_ratio)), dtype=float)
    def update(self, dict_coordinates):
        '''
        :param dict_coordinates: {'xmin':
                                  'ymin':
                                  'xmax':
                                  'ymax':}
        :return:
        '''
        if self.is_center:
            x = (dict_coordinates['xmin']+dict_coordinates['xmax'])//2
            y = (dict_coordinates['ymin']+dict_coordinates['ymax'])//2
            self.data[x,y] += 1
        else:
            offset_ratio = self.expand_ratio - 1
            offset_x = int(self.height*offset_ratio)
            offset_y = int(self.width*offset_ratio)
            x1 = int(dict_coordinates['xmin'] + offset_x)
            x2 = int(dict_coordinates['xmax'] + offset_x)+1
            y1 = int(dict_coordinates['ymin'] + offset_y)
            y2 = int(dict_coordinates['ymax'] + offset_y)+1
            if x1<0:
                x1 = 0
            if x2>=self.height:
                x2 = self.height-1
            if y1<0:
                y1 = 0
            if y2>=self.width:
                y2 = self.width-1

            for i in range(x1, x2):
                for j in range(y1, y2):
                    self.data[i,j] += 1

    def scale(self, ran):
        '''
        :param ran: [from, to]
        :return:
        '''
        shape = self.data.shape
        dim_x = shape[0]
        dim_y = shape[1]
        min = self.data[0, 0]
        max = 0
        for i in range(0, dim_x):
            for j in range(0, dim_y):
                if self.data[i,j] > max:
                    max = self.data[i,j]
                if self.data[i,j] < min:
                    min = self.data[i,j]

        distance = max - min
        distance_ = ran[1] - ran[0]
        scale = distance/distance_

        for i in range(0, dim_x):
            for j in range(0, dim_y):
                self.data[i,j] = (self.data[i,j] - min)*scale + ran[0]

    def getData(self):
        return self.data







