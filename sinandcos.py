import random
import math

#1570.79632679489  ^2 = 2467401.1002 = 785397.8pi  785400*pi = 2467406.87013  785420*pi = 2467469.70198 (246747)
#785408*pi = 2467432.00287
#6.28318530718
#
def secret_share(x):  #x：0~157079
    r = random.randint(0, 628317)  #2^17=131072   需要改为mod2pi(可先mod其倍数，再mod2pi)。 mod pi/二分之pi 会导致数值错误，因为sin与cos都是以2pi为周期
    print(r)
    secret_share_of_x_0 = (x - r) % 628318 #mod2pi
    secret_share_of_x_1 = r
    return secret_share_of_x_0, secret_share_of_x_1

def secret_share_multi(x):
    r = random.randint(0, 17179869183) #2^34=17179869184
    secret_share_of_x_0 = (x - r) % 17179869184
    secret_share_of_x_1 = r
    return secret_share_of_x_0, secret_share_of_x_1

def secure_sin(theta):
    theta_0, theta_1 = secret_share(theta)  #0~2^17(131072)
    print("0:",theta_0, theta_1)
    x0 = math.sin(theta_0/100000)
    y0 = math.cos(theta_0/100000)
    x1 = math.sin(theta_1/100000)
    y1 = math.cos(theta_1/100000)
    print("1:",x0, x1, y0, y1)
    print(f"sin pi = {math.sin(theta/100000)},sin *+* = {x0*y1+y0*x1}")

    # 0: 71205.0 99867
    # 1: 0.6533870421131887  0.8407516387140449  0.7570240241885182  0.5414209840776844
    # sin pi = 0.3894183423086505, sin * + * = 0.9902266442069274

    int_x0 = round(x0*100000) #0~2^17(131072)
    int_y0 = round(y0*100000)

    int_x1 = round(x1*100000)
    int_y1 = round(y1*100000)
    print("2:",int_x0, int_x1, int_y0, int_y1)


    fx0, fx1 = multi(int_x0, int_y1)
    print(f"3: fx0+fx1={(fx0+fx1) % 17179869184},int_x0 * int_y1 = {int_x0 * int_y1}")
    fy0, fy1 = multi(int_y0, int_x1)
    print("4:",fx0, fx1, fy0, fy1)

    sin_0 = fx0 + fy0
    sin_1 = fx1 + fy1
    print("5:",sin_0, sin_1)

    return sin_0, sin_1


def multi(x, y):
    # a = 2 b = 3 c = 6
    a0 = 1000
    a1 = 1000
    b0 = 2000
    b1 = 1000
    c0 = 2000000
    c1 = 4000000

    x0, x1 = secret_share_multi(x)
    y0, y1 = secret_share_multi(y)

    e0 = (x0 - a0) % 17179869184
    e1 = (x1 - a1) % 17179869184
    f0 = (y0 - b0) % 17179869184
    f1 = (y1 - b1) % 17179869184

    e = (e0 + e1) % 17179869184
    f = (f0 + f1) % 17179869184

    secret_share_0 = (c0 + e * b0 + f * a0 + e * f) % 17179869184
    secret_share_1 = (c1 + e * b1 + f * a1) % 17179869184

    return secret_share_0, secret_share_1

if __name__ == "__main__":
    # pi = 0.4*100000  #0~157079  2^18=262144 2^17=131072 2^34=17179869184
    # print(pi)
    # pi_0, pi_1 = secure_sin(pi)
    # print(f"pi={pi}, pi_0= {pi_0}, pi_1= {pi_1}")
    # print(f"sin pi={math.sin(pi/100000)}, sin *+* = {((pi_0 + pi_1) % 17179869184)/10000000000}")

    for i in range(100):
        pi = random.randint(0, 157079)
        pi_0, pi_1 = secure_sin(pi)
        print(f"sin pi={math.sin(pi / 100000)}, sin *+* = {((pi_0 + pi_1) % 17179869184) / 10000000000}")






    # print(math.sin(theta_0/100))
    # print(math.sin(theta_0))


"""
    def secure_sin(theta):
    theta_0, theta_1 = secret_share(theta)
    x0 = math.sin(theta_0)
    y0 = math.cos(theta_0)
    x1 = math.sin(theta_1)
    y1 = math.cos(theta_1)

    fx0, fx1 = multi(x0, y1)
    fy0, fy1 = multi(y0, x1)

    sin_0 = fx0 + fy0
    sin_1 = fx1 + fy1

    return sin_0, sin_1
"""

