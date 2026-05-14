import random

from getdata import get_velocity_and_acceleration
from getdata import get_theta
from getdata import get_length
from getdata import get_width
import numpy as np
import math


def secret_share(x):  #x：0~157079
    r = random.randint(0, 627)  #2^17=131072   需要改为mod2pi(可先mod其倍数，再mod2pi)。 mod pi/二分之pi 会导致数值错误，因为sin与cos都是以2pi为周期
    #print(r)
    secret_share_of_x_0 = (x - r) % 628 #mod2pi
    secret_share_of_x_1 = r
    return secret_share_of_x_0, secret_share_of_x_1

def secret_share_multi(x):
    r = random.randint(0, 17179869183) #2^34=17179869184
    #print(r)
    secret_share_of_x_0 = (x - r) % 17179869184
    secret_share_of_x_1 = r
    return secret_share_of_x_0, secret_share_of_x_1

def secret_share_add(x):
    r = random.randint(0, 17179869183) #2^34=17179869184
    #print(r)
    secret_share_of_x_0 = (x - r) % 17179869184
    secret_share_of_x_1 = r
    return secret_share_of_x_0, secret_share_of_x_1

def secure_sin(theta):
    theta_0, theta_1 = secret_share(theta)  #0~2^7(128)
    x0 = math.sin(theta_0/100)
    y0 = math.cos(theta_0/100)
    x1 = math.sin(theta_1/100)
    y1 = math.cos(theta_1/100)

    int_x0 = round(x0*100) #-100~100
    int_y0 = round(y0*100)

    int_x1 = round(x1*100)
    int_y1 = round(y1*100)

    fx0, fx1 = multi(int_x0, int_y1)

    fy0, fy1 = multi(int_y0, int_x1)

    sin_0 = (fx0 + fy0)  % 17179869184
    sin_1 = (fx1 + fy1)  % 17179869184

    return sin_0, sin_1


def secure_cos(theta):
    theta_0, theta_1 = secret_share(theta)  #0~2^7(128)

    x0 = math.sin(theta_0/100)
    y0 = math.cos(theta_0/100)
    x1 = math.sin(theta_1/100)
    y1 = math.cos(theta_1/100)

    int_x0 = round(x0*100) #-100~100
    int_y0 = round(y0*100)

    int_x1 = round(x1*100)
    int_y1 = round(y1*100)

    fx0, fx1 = multi(int_x0, int_x1)

    fy0, fy1 = multi(int_y0, int_y1)

    cos_0 = (fy0 - fx0)  % 17179869184
    cos_1 = (fy1 - fx1)  % 17179869184

    return cos_0, cos_1




def multi(x, y):
    a = random.randint(0, 131071)  # 2^17=131072
    b = random.randint(0, 131071)  # 2^17=131072
    c = a*b

    a0,a1 = secret_share_multi(a)
    b0,b1 = secret_share_multi(b)
    c0,c1 = secret_share_multi(c)


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




def secret_share_comp(x):
    r = random.randint(0, 17179869183) #2^34=17179869184
    #print(r)
    secret_share_of_x_0 = (x - r) % (17179869184**2)
    secret_share_of_x_1 = r
    return secret_share_of_x_0, secret_share_of_x_1


def multi_comp(x0,x1, y0,y1):

    a = random.randint(0, 17179869183)  # 2^17=131072
    b = random.randint(0, 17179869183)  # 2^17=131072
    c = a*b

    a0,a1 = secret_share_comp(a)
    b0,b1 = secret_share_comp(b)
    c0,c1 = secret_share_comp(c)

    e0 = (x0 - a0) % (17179869184**2)
    e1 = (x1 - a1) % (17179869184**2)
    f0 = (y0 - b0) % (17179869184**2)
    f1 = (y1 - b1) % (17179869184**2)

    e = (e0 + e1) % (17179869184**2)
    f = (f0 + f1) % (17179869184**2)

    secret_share_0 = (c0 + e * b0 + f * a0 + e * f) % (17179869184**2)
    secret_share_1 = (c1 + e * b1 + f * a1) % (17179869184**2)

    return secret_share_0, secret_share_1



def secure_compare(x, y):
    #print("x and y", x, y, x + y)
    x0, x1 = secret_share_comp(x)
    y0, y1 = secret_share_comp(y)
    r = random.randint(1, 2**17) # 2^8
    #print(f"r={r}")
    r0, r1 = secret_share_comp(r)
    #print("securecompare1:", r0, r1, x0 - y0, x1 - y1)

    r_x_y_0, r_x_y_1 = multi_comp(r0, r1, x0 - y0, x1 - y1)
    #print("securecompare2:", r_x_y_0, r_x_y_1, r_x_y_0 + r_x_y_1)
    r_x_y = (r_x_y_0 + r_x_y_1) % (17179869184**2)
    if r_x_y == 0 or r_x_y >= (17179869184**2/2) :
        return 1  #r*(x-y)为负数/0，x-y<=0，x<=y
    else:
        return 0  #x>y




def compute_distance_list(t_interval, t_max, location_information_of_ev, location_information_of_surrounding, round_id):
    xi = location_information_of_ev['position']
    xj = location_information_of_surrounding['position']

    vi, ai = get_velocity_and_acceleration(location_information_of_ev['virtual_number'], 'EV', round_id)
    vj, aj = get_velocity_and_acceleration(location_information_of_surrounding['virtual_number'], 'Surrounding',
                                           round_id)


    vi_int = vi * 1000000
    vi_0, vi_1 = secret_share_add(vi_int)
    vj_int = vj * 1000000
    vj_0, vj_1 = secret_share_add(vj_int)
    ai_int = ai * 1000000
    ai_0, ai_1 = secret_share_add(ai_int)
    aj_int = aj * 1000000
    aj_0, aj_1 = secret_share_add(aj_int)

    xi = xi * 1000000
    xj = xj * 1000000

    results = []

    p_theta = get_theta(location_information_of_ev['virtual_number'])
    pi = p_theta * 100 #0.4 * 100 = 40



    #
    # ai = -0.21
    # ai_int = ai * 1000000
    # ai_0, ai_1 = secret_share_add(ai_int)
    #
    # aj = 0.35
    # aj_int = aj * 1000000
    # aj_0, aj_1 = secret_share_add(aj_int)
    #
    # vi = 40.85
    # vi_int = vi * 1000000
    # vi_0, vi_1 = secret_share_add(vi_int)
    #
    # vj = 35.94
    # vj_int = vj * 1000000
    # vj_0, vj_1 = secret_share_add(vj_int)
    #
    # xi = 379.27 * 1000000
    # xj = 348.54 * 1000000


    if xi >= xj:
        pi_0, pi_1 = secure_cos(pi)

        li = get_length(location_information_of_ev['virtual_number'])
        li_int = li * 100
        l_p1_0, l_p1_1 = multi(li_int, pi_1)  #li_cos_0, li_cos_1

        for t in np.arange(0, t_max, t_interval):
            x_0 = int((0.5 * (ai_0 - aj_0) * t ** 2 + (vi_0 - vj_0) * t + xi  - (li_int * pi_0 + l_p1_0) )) % 17179869184
            x_1 = int((0.5 * (ai_1 - aj_1) * t ** 2 + (vi_1 - vj_1) * t - xj  - l_p1_1)) % 17179869184

            # listx_0.append(x_0)
            # listx_1.append(x_1)

            comp1 = secure_compare(17179869184 - x_1, x_0)
            if 17179869184 - x_1 <= x_0 and comp1 == 0:
                print("ERRORCOMP_0")
                exit(0)

            if 17179869184 - x_1 > x_0 and comp1 == 1:
                print("ERRORCOMP_1")
                print(x_0, x_1)
                print((x_0 + x_1 )%17179869184)
                print((0.5 * (ai_int - aj_int) * t ** 2 + (vi_int - vj_int) * t + xi - xj  - li_int * 10000 * math.cos(pi / 100)))
                #print("111111111111111111111111111111111111111111111111111111111111111111")

                exit(0)

            z = x_1

            if (comp1 == 1):
                z = z - 17179869184

            comp2 = secure_compare(z, 4294967296 - x_0)
            if z <= 4294967296 - x_0 and comp2 == 0:
                print("ERRORCOMP_2")
                exit(0)

            if z > 4294967296 - x_0 and comp2 == 1:
                print("ERRORCOMP_3")
                print(x_0, x_1,z,4294967296 - x_0 )

                if (x_0 + x_1) % 17179869184 >= 4294967296:
                    delta_x = (x_0 + x_1) % 17179869184 - 17179869184
                else:
                    delta_x = (x_0 + x_1) % 17179869184
                print(delta_x/1000000)

                delta_x_2 = (0.5 * (ai_int - aj_int) * t ** 2 + (
                            vi_int - vj_int) * t + xi - xj - li_int * 10000 * math.cos(pi / 100)) % 17179869184
                if delta_x_2 % 17179869184 >= 4294967296:
                    delta_x_2 = delta_x_2 - 17179869184
                print(delta_x_2/1000000)
                #print("3333333333333333333333333333333333333333333333333333333333333333")
                exit(0)

            results.append(comp2)


            # # 转换为负数的操作  2^32 = 4294967296
            # if (x_0 + x_1) % 17179869184 >= 4294967296:
            #     delta_x = (x_0 + x_1) % 17179869184 - 17179869184
            # else:
            #     delta_x = (x_0 + x_1) % 17179869184
            #
            # # delta_x = (x_0 + x_1) % 17179869184
            # list_delta_x.append(delta_x / 1000000)
            #
            # delta_x_2 = (0.5 * (ai_int - aj_int) * t ** 2 + (
            #             vi_int - vj_int) * t + xi - xj  - li_int * 10000 * math.cos(pi / 100)) % 17179869184
            # if delta_x_2 % 17179869184 >= 4294967296:
            #     delta_x_2 = delta_x_2 - 17179869184
            # list_delta_x_2.append(delta_x_2 / 1000000)
            #
            # if delta_x / 1000000 < 0 and comp2 == 1:
            #     print("ERRORCOMP_3.2")
            #     exit(0)
            #
            # if delta_x / 1000000 >= 0 and comp2 == 0:
            #     print("ERRORCOMP_4.2")
            #     print(x_0, x_1)
            #     print(delta_x_2 / 1000000)
            #     exit(0)




    else:
        pi_0, pi_1 = secure_sin(pi)
        lj = get_length(location_information_of_surrounding['virtual_number'])
        lj_int = lj * 1000000
        lj_0, lj_1 = secret_share_add(lj_int)

        w = get_width(location_information_of_surrounding['virtual_number'])
        w_int = w * 100
        w_p1_0, w_p1_1 = multi(w_int, pi_1)  # li_sin_0, li_sin_1

        for t in np.arange(0, t_max, t_interval):
            x_0 = int((0.5 * (aj_0 - ai_0) * t ** 2 + (vj_0 - vi_0) * t - xi - lj_0 - (w_int * pi_0 + w_p1_0) )) % 17179869184
            x_1 = int((0.5 * (aj_1 - ai_1) * t ** 2 + (vj_1 - vi_1) * t + xj - lj_1 - w_p1_1)) % 17179869184


            # listx_0.append(x_0)
            # listx_1.append(x_1)

            comp1 = secure_compare(17179869184 - x_1, x_0)
            if 17179869184 - x_1 <= x_0 and comp1 == 0:
                print("ERRORCOMP_4")
                exit(0)

            if 17179869184 - x_1 > x_0 and comp1 == 1:
                print("ERRORCOMP_5")
                exit(0)

            z = x_1

            if (comp1 == 1):
                z = z - 17179869184

            comp2 = secure_compare(z, 4294967296 - x_0)
            if z <= 4294967296 - x_0 and comp2 == 0:
                print("ERRORCOMP_6")
                exit(0)

            if z > 4294967296 - x_0 and comp2 == 1:
                print("ERRORCOMP_7")
                exit(0)

            results.append(comp2)




            # # 转换为负数的操作  2^32 = 4294967296
            # if (x_0 + x_1) % 17179869184 >= 4294967296:
            #     delta_x = (x_0 + x_1) % 17179869184 - 17179869184
            # else:
            #     delta_x = (x_0 + x_1) % 17179869184
            #
            # # delta_x = (x_0 + x_1) % 17179869184
            # list_delta_x.append(delta_x / 1000000)
            #
            # delta_x_2 = (0.5 * (aj_int - ai_int) * t ** 2 + (
            #             vj_int - vi_int) * t - xi + xj - lj_int - w_int * 10000 * math.sin(pi / 100)) % 17179869184
            # if delta_x_2 % 17179869184 >= 4294967296:
            #     delta_x_2 = delta_x_2 - 17179869184
            # list_delta_x_2.append(delta_x_2 / 1000000)
            #
            # if delta_x / 1000000 < 0 and comp2 == 1:
            #     print("ERRORCOMP_3.3")
            #     exit(0)
            #
            # if delta_x / 1000000 >= 0 and comp2 == 0:
            #     print("ERRORCOMP_4.3")
            #     print(x_0, x_1)
            #     print(delta_x_2 / 1000000)
            #     exit(0)

    #print("比较协议未产生错误")

    # print(list_delta_x)
    #
    # print("non")
    # print(list_delta_x_2)

    return results



if __name__ == '__main__':
    print(1)
