from math import sin , sqrt , floor

LEN = 20
p = []
A = 2
K = 5

def fade(x):
    return x * x * x * (x * (x * 6 - 15) + 10)

def lerp(a , b , x):
    return (b - a) * fade(x / LEN) + a

def mul(x , y):
    return x[0] * y[0] + x[1] * y[1]

def grad(x , y):
    ret = [0 , 0]
    ret[0] = x * 127.1 + y * 311.7
    ret[1] = x * 269.5 + y * 183.3
    s1 = sin(ret[0]) * 11.4514
    s2 = sin(ret[1]) * 19.19810
    ret[0] = (s1 - floor(s1)) * 2 - 1
    ret[1] = (s2 - floor(s2)) * 2 - 1
    l = sqrt(ret[0] * ret[0] + ret[1] * ret[1])
    ret[0] *= LEN / l; ret[1] *= LEN / l
    return ret

def perlin(x , y):
    x0 = x // LEN * LEN
    y0 = y // LEN * LEN
    x1 = x0 + LEN
    y1 = y0 + LEN

    a = mul(grad(x0 , y0) , (x - x0 , y - y0))
    b = mul(grad(x0 , y1) , (x - x0 , y - y1))
    c = mul(grad(x1 , y0) , (x - x1 , y - y0))
    d = mul(grad(x1 , y1) , (x - x1 , y - y1))

    t1 = lerp(a , c , x - x0)
    t2 = lerp(b , d , x - x0)

    return lerp(t1 , t2 , y - y0)

def noise(x , y):
    t = A * ((1 << K) - 1) / (1 << (K - 1))
    p = 0
    a = A
    f = 1
    for i in range(K):
        p += a * perlin(x * f , y * f) / LEN / LEN
        a /= 2
        f *= 2
    return (p + t) / 2 / t

def get_map(size):
    ret = []
    for i in range(size[0]):
        ret.append([])
        for j in range(size[1]):
            tmp = noise(i , j)
            # if tmp <= 0:
            #     print(i , j , tmp)
            #     exit(0)
            ret[i].append((round(fade(tmp) * (190 - 0) + 0) , round(tmp * (255 - 120) + 120) , 0))
            # print(round(noise(i , j)) , end = ",")
        # print()
    return ret