from os import system
from threading import Thread
import time , random
from win32api import GetAsyncKeyState
from ctypes import windll
import perlin_noise

class Screen:
    def __init__(self) -> None:
        self.size = (200 , 400)
        print("正在生成地图")
        self.map = perlin_noise.get_map(self.size)
        # exit(0)
        # for i in range(self.size[0]):
        #     self.map.append([])
        #     for j in range(self.size[1]):
        #         # self.map[i].append(Point((i , j) , (random.randint(0 , 255) , random.randint(0 , 255) , 0)))
        #         self.map[i].append((0 , random.randint(150 , 235) , 0))

    def show(self):
        for i in range(camera.pos[0] , camera.pos[0] + camera.size[0]):
            for j in range(camera.pos[1] , camera.pos[1] + camera.size[1]):
                out_map[framexor][i - camera.pos[0]][j - camera.pos[1]] = self.map[i][j]

class Camera:
    def __init__(self) -> None:
        self.pos = [-1 , -1] #行 列
        self.size = [90 , 160] #行 列
        self.zhening = False

    def move(self , end):
        self.pos[0] += (end[0] - self.size[0] // 2 - self.pos[0]) / 5
        self.pos[0] = int(self.pos[0])
        self.pos[0] = max(0 , self.pos[0])
        self.pos[0] = min(screen.size[0] - self.size[0] , self.pos[0])

        self.pos[1] += (end[1] - self.size[1] // 2 - self.pos[1]) / 5
        self.pos[1] = int(self.pos[1])
        self.pos[1] = max(0 , self.pos[1])
        self.pos[1] = min(screen.size[1] - self.size[1] , self.pos[1])
        screen.show()

    def start_zhen(self):
        if not self.zhening:
            self.zhening = True
            Thread(target = self.zhen).start()

    def zhen(self):
        for i in range(2):
            self.pos[0] += 1
            time.sleep(2 / FPS)
            self.pos[1] += 1
            time.sleep(2 / FPS)
            self.pos[0] -= 1
            time.sleep(2 / FPS)
            self.pos[1] -= 1
            time.sleep(2 / FPS)
        self.zhening = False

class Player:
    def __init__(self) -> None:
        self.img = self.get_img()
        self.pos = [50 , 100]
        self.dpos = [0 , 0]

    def get_img(self) -> list:
        ret = []
        for i in range(5):
            for j in range(5):
                ret.append([(0 , 0 , 255) , (i , j)]) #相对位置
        return ret

    def show(self):
        for i in self.img: 
            h = i[1][0] + self.pos[0]
            l = i[1][1] + self.pos[1]
            if not camera.pos[0] <= h < camera.pos[0] + camera.size[0]:
                continue
            if not camera.pos[1] <= l < camera.pos[1] + camera.size[1]:
                continue
            out_map[framexor][h - camera.pos[0]][l - camera.pos[1]] = i[0]

    def update(self):
        self.dpos[0] *= 0.85
        self.dpos[1] *= 0.85
        if abs(self.dpos[0]) <= 0.5: self.dpos[0] = 0
        if abs(self.dpos[1]) <= 0.5: self.dpos[1] = 0
        self.pos[0] = int(self.pos[0] + self.dpos[0])
        self.pos[1] = int(self.pos[1] + self.dpos[1])
        self.pos[0] = max(self.pos[0] , 0)
        self.pos[0] = min(self.pos[0] , screen.size[0] - 1)
        self.pos[1] = max(self.pos[1] , 0)
        self.pos[1] = min(self.pos[1] , screen.size[1] - 1)
        self.show()

class Bottom:
    def __init__(self):
        print(f"\033[{camera.size[0] + 2};1H" , end = "")
        print("\033[0mplayer_pos:(" , end = "")
        self.show_pos = [0 , 0]

    def update(self):
        out_str = []
        if player.pos != self.show_pos:
            self.show_pos = [*player.pos]
            out_str.append(f"\033[{camera.size[0] + 2};13H")
            out_str.append("%03d,%03d)" % (player.pos[0] , player.pos[1]))
        if FPS <= 35: out_str.append("\033[38;2;237;28;36m")
        elif FPS <= 45: out_str.append("\033[38;2;255;201;14m")
        out_str.append(f"\033[{camera.size[0] + 2};30HFPS:{round(FPS)}")
        # out_str.append("\033[48;2;200;0;0m\033[38;2;0;0;255m")
        # for i in range(25):
        #     out_str.append(f"\033[{camera.size[0] + i + 2};{camera.size[1] * 2 - 60}H")
        #     for j in range(50):
        #         out_str.append("▀▄")
        print("".join(out_str) , end = "" , flush = 1)

class Main:
    def __init__(self) -> None:
        lock = windll.LoadLibrary('user32.dll')
        lock.BlockInput(True)
        self.main()

    def main(self):
        global framexor , FPS
        screen.show()
        player.show()
        while True:
            st = time.time()
            self.input()
            self.update()
            # print("\033[1;1H\033[0m")
            # print((time.time() - st) * 60)
            # exit(0)
            time.sleep(max(1 / 60 - (time.time() - st) , 0))
            framexor ^= 1
            if framexor: FPS = 1 / (time.time() - st)
        
    def print_str(self , out_points):
        out_str = []
        last = [-114514 , -114514]
        last_color = None
        for i in out_points:
            if i[1][0] != last[0] or i[1][1] != last[1] + 1:
                out_str.append(f"\033[{i[1][0]};{i[1][1] * 2 - 1}H")
            last = i[1]
            if i[0] != last_color:
                out_str.append(f"\033[38;2;{i[0][0]};{i[0][1]};{i[0][2]}m")
            last_color = i[0]
            out_str.append("██")
        print("".join(out_str) , end = "\033[0m" , flush = 1)

    def print_screen(self):
        out_points = []
        for i in range(camera.size[0]):
            for j in range(camera.size[1]):
                if out_map[framexor][i][j] != out_map[framexor ^ 1][i][j]:
                    out_points.append([out_map[framexor][i][j] , (i + 1 , j + 1)])
        out_points.sort()
        self.print_str(out_points)

    def update(self):
        # frame_out.clear()                                         
        camera.move(player.pos)
        player.update()
        self.print_screen()                                     
        bottom.update()

    def input(self):
        if GetAsyncKeyState(ord('W')) & 0x8000:
            player.dpos[0] = max(player.dpos[0] - 1.4 , -3.5)
        if GetAsyncKeyState(ord('S')) & 0x8000:
            player.dpos[0] = min(player.dpos[0] + 1.4 , 3.5)
        if GetAsyncKeyState(ord('A')) & 0x8000:
            player.dpos[1] = max(player.dpos[1] - 1.4 , -3.5)
        if GetAsyncKeyState(ord('D')) & 0x8000:
            player.dpos[1] = min(player.dpos[1] + 1.4 , 3.5)
        if GetAsyncKeyState(ord('O')) & 0x8000:
            camera.start_zhen()
        if GetAsyncKeyState(ord('Q')) & 0x8000:
            print("\033[0m")
            system("cls")
            exit(0)

# if __name__ == "__main__":
print("\033[0m")
system("cls")
framexor = False
screen = Screen()
camera = Camera()
player = Player()
bottom = Bottom() 
FPS = 60
out_map = [[[(0 , 0 , 0) for i in range(camera.size[1])] for j in range(camera.size[0])] for z in range(2)]
Main()

#▀▄