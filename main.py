import math
import numpy as np
import cv2

PXL = 128


class Enviroment:
    vellocity: float = 10  # pxl/s


class PhuongTrinhSong:
    px: int
    py: int
    A: float
    omega: float
    phi: float

    def __init__(self, px=0, py=0, A=0.0, omega=0.0, phi=0.0):
        self.A = A
        self.px = px
        self.py = py
        self.omega = omega
        self.phi = phi

    def dist(self, x: int, y: int) -> float:
        return math.sqrt((self.px - x) ** 2 + (self.py - y) ** 2)


# height of water is ranging in [-10,10]
def ironPallete(x):
    sc = 200
    x /= sc
    x += 0.085
    r = round(255 * (x ** 0.5))
    g = round(255 * (x ** 3))
    b = round(255 * (max(math.sin(2 * math.pi * x), 0)))
    return [b, g, r]


table = np.ndarray([PXL, PXL])

seed = [PhuongTrinhSong(5, 5, 5, 0.6, 0),
        PhuongTrinhSong(PXL - 1, PXL - 1, 3, 0.8, 0),
        PhuongTrinhSong(PXL//2, PXL//2, 4, 1, 0)]

listtime = [np.ndarray([PXL, PXL], float)]
listtime.clear()
for s in seed:
    crdist = np.ndarray([PXL, PXL], float)
    for i in range(PXL):
        for j in range(PXL):
            crdist[i][j] = s.dist(i, j)
    listtime.append(crdist)

image = np.ndarray([PXL, PXL, 3], np.uint8)


def getPT():
    def isBase10(number):
        try:
            int(number)
            return True
        except ValueError:
            return False

    s = input("[A, omega, phi]=")
    lst = []
    ss = ""
    for c in s:
        if isBase10(c):
            ss += c
        else:
            if ss != "":
                lst.append(int(ss))
            ss = ""
    if ss != "":
        lst.append(int(ss))
    return lst


timetable = np.ndarray([PXL, PXL], float)


def calculateTimeT(t: float):
    def calHeight(i: int, j: int):
        res = 0
        for d in range(len(seed)):
            dist = listtime[d][i][j]
            s = seed[d]
            time = dist / Enviroment.vellocity
            if time < t:
                res += s.A * math.cos(s.omega * (t - time) + s.phi * math.pi)
        return res

    for i in range(PXL):
        for j in range(PXL):
            table[i, j] = calHeight(i, j)


def convertToPixel():
    for i in range(PXL):
        for j in range(PXL):
            image[i, j] = ironPallete(table[i, j])


if __name__ == "__main__":
    name = "giao thoa song nuoc.mp4"
    FPS=4
    resolution = (PXL, PXL)
    videoLength=30
    out = cv2.VideoWriter(name, cv2.VideoWriter_fourcc(*"mp4v"), FPS, resolution)
    for t in range(videoLength*FPS):
        calculateTimeT(t * 1.25)
        convertToPixel()
        out.write(image)
        print("frame", t, "finished")
    out.release()

#     #print(getPT())

# # lmao = caiDCM()
# # print(lmao)

# # if(__name__=='__main__'):
# #     print(lmao)


# # def func(a,b,d={}):
# #     d[a]=b
# #     print(d)

# # func(10,10)
# # func(20,20,{})


# class bruh:
#     x:int;y:int

#     def __init__(self,x,y):
#         self.x=x
#         self.y=y

#     def dist(self,x:int,y:int)->float:
#         return math.sqrt((self.x-x)**2+(self.y-y)**2)
# br = bruh(10,10)
# # br.x=10
# # br.y=10
# print(br.dist(0,0))
