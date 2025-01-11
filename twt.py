import time
from win32api import GetAsyncKeyState
from ctypes import windll
from queue import PriorityQueue
from random import randint

def draw_clear():
    print("\033[0m" , end = "")

def return_start():
    print("\033[F" * (camera.size[0] + 10) , end = "")
    print(f"\033[{camera.size[1] + 10}D" , end = "")

def mouse_move(st , ed) -> str:
    ret = []
    if ed[1] != st[1]:
        if ed[1] < st[1]:
            ret.append(f"\033[{(st[1] - ed[1]) * 2}D")
        else:
            ret.append(f"\033[{(ed[1] - st[1]) * 2}C")
    if ed[0] != st[0]:
        if ed[0] < st[0]:
            ret.append(f"\033[{st[0] - ed[0]}A")
        else:
            ret.append(f"\033[{ed[0] - st[0]}B")
    return "".join(ret)

class Point:
    def __init__(self , pos , color) -> None:
        self.pos = pos
        self.color = color

class Screen:
    def __init__(self) -> None:
        self.size = (200 , 400)
        self.map = []
        self.layer = -1
        for i in range(self.size[0]):
            self.map.append([])
            for j in range(self.size[1]):
                self.map[i].append(Point((i , j) , (randint(0 , 50) , randint(60 , 230) , randint(0 , 50))))
        for i in range(40 , 161):
            for j in range(40 , 361):
                self.map[i][j].color = (60 , 60 , 60)
        # for i in range(self.size[0]):
        #     self.map.append([])
        #     for j in range(self.size[1]):
        #         self.map[i].append(Point((i , j) , (255 , 255 , 255)))

    def show(self , out_frame):
        out_frame.clear()
        for i in range(camera.pos[0] , camera.pos[0] + camera.size[0]):
            out_frame.append([])
            for j in range(camera.pos[1] , camera.pos[1] + camera.size[1]):
                out_frame[i - camera.pos[0]].append(Point(self.map[i][j].pos[:] , self.map[i][j].color[:]))
                # out_frame[i - camera.pos[0]][j - camera.pos[1]].pos = self.map[i][j].pos[:]
                # out_frame[i - camera.pos[0]][j - camera.pos[1]].color = self.map[i][j].color[:]

    def show_only_myself(self):
        draw_clear()
        return_start()
        last_color = None
        out_str = []
        for i in range(camera.pos[0] , camera.pos[0] + camera.size[0]):
            for j in range(camera.pos[1] , camera.pos[1] + camera.size[1]):
                if self.map[i][j].color == last_color:
                    out_str.append("██")
                else:
                    out_str.append(f"\033[38;2;{self.map[i][j].color[0]};{self.map[i][j].color[1]};{self.map[i][j].color[2]}m██")
                    last_color = self.map[i][j].color[:]
            out_str.append("\n")
        print("".join(out_str) , end = "\033[0m")

class Camera:
    def __init__(self) -> None:
        self.pos = [0 , 0] #行 列
        self.size = [100 , 200] #行 列
        self.show_frame = [[Point((0 , 0) , (0 , 0 , 0)) for __ in range(self.size[1] + 10)] for _ in range(self.size[0] + 10)]
        self.last_frame = [[Point((1 , 1) , (1 , 1 , 1)) for __ in range(self.size[1] + 10)] for _ in range(self.size[0] + 10)]

    def init_queue(self):
        self.output_queue = PriorityQueue()
        self.output_queue.put((screen.layer , screen.show))
        self.output_queue.put((player.layer , player.show))

    def conflate_frame(self):
        self.init_queue()
        while not self.output_queue.empty():
            self.output_queue.get()[1](self.show_frame)
        
    def display(self):
        self.conflate_frame()
        if self.last_frame == self.show_frame:
            return 
        # print(camera.show_frame == camera.last_frame , self.show_frame == self.last_frame)
        # draw_clear()
        return_start()
        last_color = (-1 , -1 , -1)
        out_str = []
        now_pos = [0 , 0]
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                out = self.show_frame[i][j].color[:]
                if self.last_frame[i][j].color[0] == out[0] and self.last_frame[i][j].color[1] == out[1] and self.last_frame[i][j].color[2] == out[2] :
                    continue
                self.last_frame[i][j].pos = self.show_frame[i][j].pos[:]
                self.last_frame[i][j].color = out
                tmp = mouse_move(now_pos , [i , j])
                if tmp != "":
                    out_str.append(tmp)
                
                if out == last_color:
                    out_str.append("██")
                else:
                    out_str.append(f"\033[38;2;{out[0]};{out[1]};{out[2]}m██")
                    last_color = out
                now_pos = [i , j + 1]
        print("".join(out_str) , end = "\033[0m" , flush = 1)

    def move(self , end):
        self.pos[0] += (end[0] - self.size[0] // 2 - self.pos[0]) / 5
        self.pos[0] = int(self.pos[0])
        self.pos[0] = max(0 , self.pos[0])
        self.pos[0] = min(screen.size[0] - self.size[0] , self.pos[0])

        self.pos[1] += (end[1] - self.size[1] // 2 - self.pos[1]) / 5
        self.pos[1] = int(self.pos[1])
        self.pos[1] = max(0 , self.pos[1])
        self.pos[1] = min(screen.size[1] - self.size[1] , self.pos[1])

class Player:
    def __init__(self) -> None:
        self.img = self.get_img()
        self.pos = [50 , 100]
        self.dpos = [0 , 0]
        self.layer = 10

    def get_img(self) -> list:
        ret = [
            Point((0 , 0) , (255 , 173 , 83)) , 
            Point((0 , 1) , (255 , 173 , 83)) , 
            Point((0 , 2) , (255 , 173 , 83)) , 
            Point((0 , 3) , (220 , 148 , 23)) , 
            Point((0 , 4) , (220 , 148 , 23)) , 
            Point((1 , 0) , (225 , 173 , 83)) , 
            Point((1 , 1) , (225 , 249 , 121)) , 
            Point((1 , 2) , (225 , 249 , 121)) , 
            Point((1 , 3) , (251 , 242 , 54)) , 
            Point((1 , 4) , (220 , 148 , 23)) , 
            Point((2 , 0) , (220 , 148 , 23)) , 
            Point((2 , 1) , (255 , 255 , 255)) , 
            Point((2 , 2) , (251 , 242 , 54)) , 
            Point((2 , 3) , (255 , 255 , 255)) , 
            Point((2 , 4) , (200 , 127 , 0)) , 
            Point((3 , 0) , (220 , 148 , 23)) , 
            Point((3 , 1) , (251 , 242 , 54)) , 
            Point((3 , 2) , (255 , 243 , 0)) , 
            Point((3 , 3) , (255 , 243 , 0)) , 
            Point((3 , 4) , (200 , 127 , 0)) , 
            Point((4 , 0) , (220 , 148 , 23)) , 
            Point((4 , 1) , (220 , 148 , 23)) , 
            Point((4 , 2) , (220 , 148 , 23)) , 
            Point((4 , 3) , (200 , 127 , 0)) , 
            Point((4 , 4) , (200 , 127 , 0)) , 
        ]
        # for i in range(5):
        #     for j in range(5):
        #         ret.append(Point((i , j) , (0 , 0 , 255))) #相对位置
        return ret

    def show(self , out_frame):
        for i in self.img: 
            h = i.pos[0] + self.pos[0]
            l = i.pos[1] + self.pos[1]
            if not camera.pos[0] <= h < camera.pos[0] + camera.size[0]:
                continue
            if not camera.pos[1] <= l < camera.pos[1] + camera.size[1]:
                continue
            out_frame[h - camera.pos[0]][l - camera.pos[1]].pos = (h , l)
            out_frame[h - camera.pos[0]][l - camera.pos[1]].color = i.color[:]
            # print(self.pos)
        # print(out_frame == camera.show_frame , camera.show_frame == camera.last_frame)

    def update(self):
        if abs(self.dpos[0]) >= 1 or abs(self.dpos[1]) >= 1:
            self.dpos[0] *= 0.9
            self.dpos[1] *= 0.9
            self.pos[0] = int(self.pos[0] + self.dpos[0])
            self.pos[1] = int(self.pos[1] + self.dpos[1])
            self.pos[0] = max(self.pos[0] , 0)
            self.pos[0] = min(self.pos[0] , screen.size[0] - 1)
            self.pos[1] = max(self.pos[1] , 0)
            self.pos[1] = min(self.pos[1] , screen.size[1] - 1)

class Objects:
    def __init__(self):
        self.img = self.getimg()

    def get_img(self):
        ret = []
        for i in range(5):
            for j in range(5):
                ret.append(Point((i , j) , (0 , 255 , 0)))

screen = Screen()
camera = Camera()
player = Player()

class Main:
    def __init__(self) -> None:
        lock = windll.LoadLibrary('user32.dll')
        lock.BlockInput(True)
        self.main()

    def main(self):
        screen.show_only_myself()
        # player.show()
        while True:
            self.input()
            self.update()
            time.sleep(1 / 60)
            # self.input()
        
    def update(self):
        camera.move(player.pos)
        player.update()
        camera.display()
        # return_start()
        # print(mouse_move((0 , 0) , (190 , 0)) , end = "")
        # print(camera.show_frame[0][6].color , end = "")

    def input(self):
        if GetAsyncKeyState(ord('W')) & 0x8000:
            player.dpos[0] = max(player.dpos[0] - 2 , -4)
        if GetAsyncKeyState(ord('S')) & 0x8000:
            player.dpos[0] = min(player.dpos[0] + 2 , 4)
        if GetAsyncKeyState(ord('A')) & 0x8000:
            player.dpos[1] = max(player.dpos[1] - 2 , -4)
        if GetAsyncKeyState(ord('D')) & 0x8000:
            player.dpos[1] = min(player.dpos[1] + 2 , 4)
        if GetAsyncKeyState(ord('Q')) & 0x8000:
            exit(0)

Main()