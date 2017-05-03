import units
import draw_hm
from pyheatmap.heatmap import HeatMap
file_name = 'output_boxes.txt'

class_units = {}
class_draw = {}
class_num = 20
height = 300
width = 300
is_center = False
expand_ratio = 1
is_scale = False
heatmap_circle = False


d_height = height if is_center else height*expand_ratio
d_width = width if is_center else width*expand_ratio

for i in range(class_num):
    unit = units.Distribution(height, width, is_center=is_center, expand_ratio=expand_ratio)
    class_units[i] = unit
    draw = draw_hm.Draw(d_height, d_width)
    class_draw[i] = draw




with open(file_name,'r') as file:
    line = file.readline()
    while line:
        line = line.replace('\n','')
        items = line.split(',')
        #print(items)
        if is_scale:
            xcof = height
            ycof = width
        else:
            xcof = 1
            ycof = 1
        index = int(items[0])-1
        xmin = int(float(items[1]) * xcof)
        ymin = int(float(items[2]) * ycof)
        xmax = int(float(items[3]) * xcof)
        ymax = int(float(items[4]) * ycof)
        dict_ = {'xmin':xmin, 'ymin':ymin, 'xmax':xmax, 'ymax':ymax}
        class_units[index].update(dict_)


        line = file.readline()


for k in range(class_num):
    a = class_units[k].data
    tmp = []
    for i in range(height):
        for j in range(width):
            tmp.append((i, j, a[i,j]))
    class_draw[k].get_data(tmp)
    # hm = HeatMap(tmp)
    # hm.heatmap(save_as='heatmap_class%d.png'%(k+1))

for k in range(class_num):
    save_name = 'heatmap_class%d.png'%(k+1)
    class_draw[k].heatmap(save_name)











