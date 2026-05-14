def get_lc_request():
    return [1, 70, "Left", 3, "Active"] #在最右侧车道，即3号车道上
    #return [1, 70, "None", 2, "Active"]


"""
def protocol_mpclc(args):
    [args["request_virtual_number"],
     args["request_position"],
     args["request_lane_change_direction"],
     args["request_current_lane"],
     args["request_service_signal"]] = get_Lc_Request()
"""
def get_location_information_lists(round_id):  # protocol_mpclc

#Lane 2 一车且可通行
#1.2
    if round_id == 0:
        return [
                {'virtual_number': 3, 'position': 200, 'current_lane': 2},
                {'virtual_number': 4, 'position': 300, 'current_lane': 1},
                {'virtual_number': 1, 'position': 70, 'current_lane': 3}]
    elif round_id == 1:
        # TODO 修改
        return [
                {'virtual_number': 3, 'position': 2000, 'current_lane': 2},
                {'virtual_number': 4, 'position': 300, 'current_lane': 1},
                {'virtual_number': 1, 'position': 70, 'current_lane': 3}]
    elif round_id == 2:
        # TODO 修改
        return [
                {'virtual_number': 3, 'position': 2000, 'current_lane': 2},
                {'virtual_number': 4, 'position': 300, 'current_lane': 1},
                {'virtual_number': 1, 'position': 70, 'current_lane': 3}]


#
# #Lane 2 两车且可通行
# #1.3
#     if round_id == 0:
#         return [{'virtual_number': 2, 'position': 0, 'current_lane': 2},
#                 {'virtual_number': 3, 'position': 2000, 'current_lane': 2},
#                 {'virtual_number': 4, 'position': 300, 'current_lane': 1},
#                 {'virtual_number': 1, 'position': 70, 'current_lane': 3}]
#     elif round_id == 1:
#         # TODO 修改
#         return [{'virtual_number': 2, 'position': 0, 'current_lane': 2},
#                 {'virtual_number': 3, 'position': 2000, 'current_lane': 2},
#                 {'virtual_number': 4, 'position': 300, 'current_lane': 1},
#                 {'virtual_number': 1, 'position': 70, 'current_lane': 3}]
#     elif round_id == 2:
#         # TODO 修改
#         return [{'virtual_number': 2, 'position': 0, 'current_lane': 2},
#                 {'virtual_number': 3, 'position': 2000, 'current_lane': 2},
#                 {'virtual_number': 4, 'position': 300, 'current_lane': 1},
#                 {'virtual_number': 1, 'position': 70, 'current_lane': 3}]


#Lane 2 一车且可不可通行，随后无车可通行
#2.2
    # if round_id == 0:
    #     return [
    #             {'virtual_number': 3, 'position': 80, 'current_lane': 2},
    #             {'virtual_number': 4, 'position': 300, 'current_lane': 1},
    #             {'virtual_number': 1, 'position': 70, 'current_lane': 3}]
    # elif round_id == 1:
    #     # TODO 修改
    #     return [{'virtual_number': 3, 'position': 2000, 'current_lane': 2},
    #             {'virtual_number': 4, 'position': 300, 'current_lane': 1},
    #             {'virtual_number': 1, 'position': 70, 'current_lane': 3}]
    # elif round_id == 2:
    #     # TODO 修改
    #     return [
    #             {'virtual_number': 3, 'position': 2000, 'current_lane': 2},
    #             {'virtual_number': 4, 'position': 300, 'current_lane': 1},
    #             {'virtual_number': 1, 'position': 70, 'current_lane': 3}]

# # 2.3
#     if round_id == 0:
#         return [{'virtual_number': 2, 'position': 50, 'current_lane': 2},
#                 {'virtual_number': 3, 'position': 200, 'current_lane': 2},
#                 {'virtual_number': 4, 'position': 300, 'current_lane': 1},
#                 {'virtual_number': 1, 'position': 70, 'current_lane': 3}]
#     elif round_id == 1:
#         # TODO 修改
#         return [
#                 {'virtual_number': 3, 'position': 200, 'current_lane': 2},
#                 {'virtual_number': 4, 'position': 300, 'current_lane': 1},
#                 {'virtual_number': 1, 'position': 70, 'current_lane': 3}]
#     elif round_id == 2:
#         # TODO 修改
#         return [{'virtual_number': 2, 'position': 0, 'current_lane': 2},
#                 {'virtual_number': 3, 'position': 200, 'current_lane': 2},
#                 {'virtual_number': 4, 'position': 300, 'current_lane': 1},
#                 {'virtual_number': 1, 'position': 70, 'current_lane': 3}]


# # 2.4
#     if round_id == 0:
#         return [{'virtual_number': 2, 'position': 50, 'current_lane': 2},
#                 {'virtual_number': 3, 'position': 200, 'current_lane': 2},
#                 {'virtual_number': 4, 'position': 300, 'current_lane': 1},
#                 {'virtual_number': 1, 'position': 70, 'current_lane': 3}]
#     elif round_id == 1:
#         # TODO 修改
#         return [{'virtual_number': 2, 'position': 10, 'current_lane': 2},
#                 {'virtual_number': 3, 'position': 200, 'current_lane': 2},
#                 {'virtual_number': 4, 'position': 300, 'current_lane': 1},
#                 {'virtual_number': 1, 'position': 70, 'current_lane': 3}]
#     elif round_id == 2:
#         # TODO 修改
#         return [{'virtual_number': 2, 'position': 0, 'current_lane': 2},
#                 {'virtual_number': 3, 'position': 200, 'current_lane': 2},
#                 {'virtual_number': 4, 'position': 300, 'current_lane': 1},
#                 {'virtual_number': 1, 'position': 70, 'current_lane': 3}]



# # 3.4
#     if round_id == 0:
#         return [{'virtual_number': 2, 'position': 100, 'current_lane': 2},
#                 {'virtual_number': 2, 'position': 50, 'current_lane': 2},
#                 {'virtual_number': 3, 'position': 200, 'current_lane': 2},
#                 {'virtual_number': 4, 'position': 300, 'current_lane': 1},
#                 {'virtual_number': 1, 'position': 70, 'current_lane': 3}]
#     elif round_id == 1:
#         # TODO 修改
#         return [{'virtual_number': 2, 'position': 100, 'current_lane': 2},
#                 {'virtual_number': 2, 'position': 50, 'current_lane': 2},
#                 {'virtual_number': 3, 'position': 200, 'current_lane': 2},
#                 {'virtual_number': 4, 'position': 300, 'current_lane': 1},
#                 {'virtual_number': 1, 'position': 70, 'current_lane': 3}]
#     elif round_id == 2:
#         # TODO 修改
#         return [
#                 {'virtual_number': 2, 'position': 10, 'current_lane': 2},
#
#                 {'virtual_number': 4, 'position': 300, 'current_lane': 1},
#                 {'virtual_number': 1, 'position': 70, 'current_lane': 3}]


# # 3.5
#     if round_id == 0:
#         return [{'virtual_number': 2, 'position': 100, 'current_lane': 2},
#                 {'virtual_number': 2, 'position': 50, 'current_lane': 2},
#                 {'virtual_number': 3, 'position': 200, 'current_lane': 2},
#                 {'virtual_number': 4, 'position': 300, 'current_lane': 1},
#                 {'virtual_number': 1, 'position': 70, 'current_lane': 3}]
#     elif round_id == 1:
#         # TODO 修改
#         return [{'virtual_number': 2, 'position': 100, 'current_lane': 2},
#                 {'virtual_number': 2, 'position': 50, 'current_lane': 2},
#                 {'virtual_number': 3, 'position': 200, 'current_lane': 2},
#                 {'virtual_number': 4, 'position': 300, 'current_lane': 1},
#                 {'virtual_number': 1, 'position': 70, 'current_lane': 3}]
#     elif round_id == 2:
#         # TODO 修改
#         return [{'virtual_number': 2, 'position': 100, 'current_lane': 2},
#                 {'virtual_number': 2, 'position': 50, 'current_lane': 2},
#                 {'virtual_number': 3, 'position': 200, 'current_lane': 2},
#                 {'virtual_number': 4, 'position': 300, 'current_lane': 1},
#                 {'virtual_number': 1, 'position': 70, 'current_lane': 3}]


# ***1.5 需要更改本文件第一个函数配置
#     if round_id == 0:
#         return [{'virtual_number': 2, 'position': 10, 'current_lane': 1},
#                 {'virtual_number': 4, 'position': 200, 'current_lane': 1},
#                 {'virtual_number': 3, 'position': 55, 'current_lane': 3},
#                 {'virtual_number': 5, 'position': 90, 'current_lane': 3},
#                 {'virtual_number': 1, 'position': 70, 'current_lane': 2}]
#     elif round_id == 1:
#         # TODO 修改
#         return [{'virtual_number': 2, 'position': 50, 'current_lane': 1},
#                 {'virtual_number': 4, 'position': 100, 'current_lane': 1},
#                 {'virtual_number': 3, 'position': 55, 'current_lane': 3},
#                 {'virtual_number': 5, 'position': 90, 'current_lane': 3},
#                 {'virtual_number': 1, 'position': 70, 'current_lane': 2}]
#     elif round_id == 2:
#         # TODO 修改
#         return [{'virtual_number': 2, 'position': 50, 'current_lane': 1},
#                 {'virtual_number': 4, 'position': 100, 'current_lane': 1},
#                 {'virtual_number': 3, 'position': 55, 'current_lane': 3},
#                 {'virtual_number': 5, 'position': 90, 'current_lane': 3},
#                 {'virtual_number': 1, 'position': 70, 'current_lane': 2}]
#



# ***2.7 需要更改本文件第一个函数配置
#     if round_id == 0:
#         return [{'virtual_number': 2, 'position': 50, 'current_lane': 1},
#                 {'virtual_number': 4, 'position': 100, 'current_lane': 1},
#                 {'virtual_number': 3, 'position': 55, 'current_lane': 3},
#                 {'virtual_number': 5, 'position': 90, 'current_lane': 3},
#                 {'virtual_number': 1, 'position': 70, 'current_lane': 2}]
#     elif round_id == 1:
#         # TODO 修改
#         return [{'virtual_number': 2, 'position': 10, 'current_lane': 1},
#                 {'virtual_number': 4, 'position': 200, 'current_lane': 1},
#                 {'virtual_number': 3, 'position': 55, 'current_lane': 3},
#                 {'virtual_number': 5, 'position': 90, 'current_lane': 3},
#                 {'virtual_number': 1, 'position': 70, 'current_lane': 2}]
#     elif round_id == 2:
#         # TODO 修改
#         return [{'virtual_number': 2, 'position': 30, 'current_lane': 1},
#                 {'virtual_number': 4, 'position': 200, 'current_lane': 1},
#                 {'virtual_number': 3, 'position': 55, 'current_lane': 3},
#                 {'virtual_number': 5, 'position': 90, 'current_lane': 3},
#                 {'virtual_number': 1, 'position': 70, 'current_lane': 2}]





# if round_id == 0:
    #     return [{'virtual_number': 2, 'position': 50, 'current_lane': 2},
    #             {'virtual_number': 3, 'position': 100, 'current_lane': 2},
    #             {'virtual_number': 4, 'position': 100, 'current_lane': 1},
    #             {'virtual_number': 1, 'position': 70, 'current_lane': 3}]
    # elif round_id == 1:
    #     # TODO 修改
    #     return [{'virtual_number': 2, 'position': 50, 'current_lane': 2},
    #             {'virtual_number': 3, 'position': 100, 'current_lane': 2},
    #             {'virtual_number': 4, 'position': 100, 'current_lane': 1},
    #             {'virtual_number': 1, 'position': 70, 'current_lane': 3}]
    # elif round_id == 2:
    #     # TODO 修改
    #     return [{'virtual_number': 2, 'position': 50, 'current_lane': 2},
    #             {'virtual_number': 3, 'position': 100, 'current_lane': 2},
    #             {'virtual_number': 4, 'position': 100, 'current_lane': 1},
    #             {'virtual_number': 1, 'position': 70, 'current_lane': 3}]

# 附近车辆将自己车辆的位置信息Location Information ={虚拟编号:N, 位置:x, 当前车道:L} 发送给RSU
# location_information_lists中每个元素为字典{虚拟编号:N, 位置:x, 当前车道:L}
# def get_location_information_lists(round_id):  # protocol_mpclc
#
#     if round_id == 0:
#         return [{'virtual_number': 2, 'position': 50, 'current_lane': 2},
#                 {'virtual_number': 3, 'position': 100, 'current_lane': 2},
#                 {'virtual_number': 4, 'position': 100, 'current_lane': 1},
#                 {'virtual_number': 1, 'position': 70, 'current_lane': 3}]
#     elif round_id == 1:
#         # TODO 修改
#         return [{'virtual_number': 2, 'position': 50, 'current_lane': 2},
#                 {'virtual_number': 3, 'position': 100, 'current_lane': 2},
#                 {'virtual_number': 4, 'position': 100, 'current_lane': 1},
#                 {'virtual_number': 1, 'position': 70, 'current_lane': 3}]
#     elif round_id == 2:
#         # TODO 修改
#         return [{'virtual_number': 2, 'position': 50, 'current_lane': 2},
#                 {'virtual_number': 3, 'position': 100, 'current_lane': 2},
#                 {'virtual_number': 4, 'position': 100, 'current_lane': 1},
#                 {'virtual_number': 1, 'position': 70, 'current_lane': 3}]

#
# def get_location_information_lists(round_id):  # protocol_mpclc
# #若没有第一条车道的车，就会出错在按currentLANE进行字典元素分类的时候做的不好
#     if round_id == 0:
#         return [{'virtual_number': 2, 'position': 50, 'current_lane': 1},
#                 {'virtual_number': 4, 'position': 100, 'current_lane': 1},
#                 {'virtual_number': 3, 'position': 55, 'current_lane': 3},
#                 {'virtual_number': 5, 'position': 90, 'current_lane': 3},
#                 {'virtual_number': 1, 'position': 70, 'current_lane': 2}]
#     elif round_id == 1:
#         # TODO 修改
#         return [{'virtual_number': 2, 'position': 50, 'current_lane': 1},
#                 {'virtual_number': 4, 'position': 100, 'current_lane': 1},
#                 {'virtual_number': 3, 'position': 55, 'current_lane': 3},
#                 {'virtual_number': 5, 'position': 90, 'current_lane': 3},
#                 {'virtual_number': 1, 'position': 70, 'current_lane': 2}]
#     elif round_id == 2:
#         # TODO 修改
#         return [{'virtual_number': 2, 'position': 50, 'current_lane': 1},
#                 {'virtual_number': 4, 'position': 100, 'current_lane': 1},
#                 {'virtual_number': 3, 'position': 55, 'current_lane': 3},
#                 {'virtual_number': 5, 'position': 90, 'current_lane': 3},
#                 {'virtual_number': 1, 'position': 70, 'current_lane': 2}]




# 创造所有临近车辆的dataframe 横列：虚拟编号:N。 纵列：第0轮速度:v, 第0轮加速度:a,第1轮速度:v, 第1轮加速度:a,第2轮速度:v, 第2轮加速度:a...
# 每个车辆可创造一个字典列表，需要的时候就按照虚拟编号查找
def get_velocity_and_acceleration(surrounding_vehicle_virtual_number, type,
                                  round_id):  # protocol_one_round 中的 compute_distance_list
    # TODO
    if round_id == 0:
        if type == 'EV':
            return 25.94, 0.35
        elif type == 'Surrounding':
            return 40.85, -0.21
    elif round_id == 1:
        if type == 'EV':
            return 25.94, 0.35
        elif type == 'Surrounding':
            return 40.85, -0.21
    elif round_id == 2:
        if type == 'EV':
            return 25.94, 0.35
        elif type == 'Surrounding':
            return 40.85, -0.21

    # if round_id == 0:
    #     if type == 'EV':
    #         return 40.85, -0.21
    #     elif type == 'Surrounding':
    #         return 35.94, 0.35
    # elif round_id == 1:
    #     if type == 'EV':
    #         return 40.85, -0.21
    #     elif type == 'Surrounding':
    #         return 35.94, 0.35
    # elif round_id == 2:
    #     if type == 'EV':
    #         return 40.85, -0.21
    #     elif type == 'Surrounding':
    #         return 35.94, 0.35

def get_theta(location_information_of_ev):
    return 0.4


# 可创造一个字典列表，[{虚拟编号:N, 长度:length},{虚拟编号:N, 长度:length}...]需要的时候就按照虚拟编号查找对应长度
def get_length(num):  # protocol_lctad
    return 10

def get_width(num):  # protocol_lctad
    return 5


if __name__ == '__main__':
    print(1)
