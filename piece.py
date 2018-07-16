import base64


class Piece:
    x = 0
    y = 0
    file = ""

    def __init__(self, x, y, text):
        self.x = int(x)
        self.y = int(y)
        self._text = text

    # 解码base64图片
    def decode(self):
        img_raw_data = base64.b64decode(self._text)
        self.file = "data\\" + str(self.y) + "-" + str(self.x) + ".png"

        t = open(self.file, "wb")
        t.write(img_raw_data)
        t.close()

