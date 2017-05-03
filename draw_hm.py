"""
yux
2017/5/2

"""
from PIL import Image
from PIL import ImageDraw2
import os
def mk_colors(n=240):
    '''
    生成色盘，色盘范围 0-n(240)
    :param n:
    :return: list[0-n]
    '''
    colors = []
    n1 = int(n * 0.4)
    n2 = n - n1
    for i in range(n1):
        color = "hsl(240, 100%%, %d%%)" % (100 * (n1 - i / 2) / n1)
        colors.append(color)
    for i in range(n2):
        color = "hsl(%.0f, 100%%, 50%%)" % (240 * (1.0 - float(i) / n2))
        colors.append(color)

    return colors

class Draw:
    def __init__(self, height, width, is_heatmap_circle=True,heat_range=240):
        self.height = height
        self.width = width
        self.heat_range = heat_range
        self.heatmap_circle = is_heatmap_circle


    def get_data(self, data):
        """
        :param data: [(x,y,n)...]
        :return:
        """
        assert len(data) == self.height * self.width
        self.data = data

    def __mk_img(self):
        """
        生成临时图片
        :return:
        """
        self.__im = Image.new("RGBA", (self.width, self.height), (0,0,0,0))

    def __heat(self, heat_data, x, y, n, template):
        l = len(heat_data)
        height = self.height
        p = x * height + y

        if self.heatmap_circle:
            for ip, iv in template:
                p2 = p + ip
                if 0 <= p2 < l:
                    heat_data[p2] += iv * n
        else:
            heat_data[p] += n


    def __save(self):
        save_as = os.path.join(os.getcwd(), self.save_as)
        folder, fn = os.path.split(save_as)
        if not os.path.isdir(folder):
            os.makedirs(folder)

        self.__im.save(save_as)
        self.__im = None


    def __print_heat(self, heat_data, colors):
        import re

        im = self.__im
        rr = re.compile(", (\d+)%\)")
        dr = ImageDraw2.ImageDraw.Draw(im)
        width = self.width
        height = self.height

        max_v = max(heat_data)
        if max_v <= 0:
            return

        r = 240.0 / max_v
        heat_data2 = [int(i * r) - 1 for i in heat_data]

        size = width * height
        for p in range(size):
            v = heat_data2[p]
            if v > 0:
                x, y = p % width, p // width
                color = colors[v]
                alpha = int(rr.findall(color)[0])
                if alpha > 50:
                    al = 255 - 255 * (alpha - 50) // 50
                    im.putpixel((x, y), (0, 0, 255, al))
                else:
                    dr.point((x, y), fill=color)




    def heatmap(self, save_as=None):
        self.__mk_img()
        heat_data = [0] * self.height * self.width
        circle =  mk_circle(10, self.height)
        data = self.data
        assert data!=None
        for hit in data:
            x, y, n  = hit
            if x < 0 or x >= self.height or y < 0 or y >= self.width:
                continue
            self.__heat(heat_data, x, y, n, circle)

        self.__print_heat(heat_data, mk_colors())
        if save_as:
            self.save_as = save_as
            self.__save()









def mk_circle(r, w):
    """
    根据半径r以及图片宽度 w ，产生一个圆的list
    """

    # __clist = set()
    __tmp = {}

    def c8(ix, iy, v=1):
        # 8对称性
        ps = (
            (ix, iy),
            (-ix, iy),
            (ix, -iy),
            (-ix, -iy),
            (iy, ix),
            (-iy, ix),
            (iy, -ix),
            (-iy, -ix),
        )
        for x2, y2 in ps:
            p = w * y2 + x2
            __tmp.setdefault(p, v)

    # 中点圆画法
    x = 0
    y = r
    d = 3 - (r << 1)
    while x <= y:
        for _y in range(x, y + 1):
            c8(x, _y, y + 1 - _y)
        if d < 0:
            d += (x << 2) + 6
        else:
            d += ((x - y) << 2) + 10
            y -= 1
        x += 1


    return __tmp.items()