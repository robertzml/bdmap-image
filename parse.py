import json
from piece import Piece
from PIL import Image


class Parse:
    _size = 256
    pieces = []

    # 解析har文件
    def read_file(self, file):
        fo = open(file, "r")
        json_dict = json.load(fo)

        count = len(json_dict["log"]["entries"])

        for i in range(count):
            entry = json_dict["log"]["entries"][i]
            x = ""
            y = ""

            if len(entry["request"]["queryString"]) == 0:
                continue

            if entry["request"]["queryString"][0]["name"] == "qt":
                for j in entry["request"]["queryString"]:
                    if j["name"] == "x":
                        x = j["value"]

                    if j["name"] == "y":
                        y = j["value"]

                content = entry["response"]["content"]["text"]
                # print(x, ": ", y)

                piece = Piece(x, y, content)
                piece.decode()

                self.pieces.append(piece)

        fo.close()

    # 计算图片最大格数
    def get_size(self):
        max_y = max(map(lambda r: r.y, self.pieces))
        min_y = min(map(lambda r: r.y, self.pieces))
        max_x = max(map(lambda r: r.x, self.pieces))
        min_x = min(map(lambda r: r.x, self.pieces))

        return [max_y, min_y, max_x, min_x]

    # 拼接图片到一张大图
    def joint_image(self):
        [max_y, min_y, max_x, min_x] = self.get_size()

        img = Image.new("RGBA", ((max_x - min_x + 1) * self._size, (max_y - min_y + 1) * self._size))

        for piece in self.pieces:
            x = (piece.x - min_x) * self._size
            y = -(piece.y - max_y) * self._size

            from_image = Image.open(piece.file)
            img.paste(from_image, (x, y))

        img.save('export.png')

