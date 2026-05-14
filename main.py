import time
from argument import get_args
from getdata import get_lc_request, get_location_information_lists, get_length
from collections import defaultdict
from distancelist import compute_distance_list


def group_dicts_by_key(dict_list, key):  # 根据某key的value值进行分组："current_lane"
    grouped = defaultdict(list)
    for item in dict_list:
        grouped[item[key]].append(item)
    return list(grouped.values())


def sort_and_group_dicts(dict_list, group_key, sort_key=None, reverse=False):
    """
    1. 如果传入了 sort_key，先对整个列表按 sort_key 排序
    2. 再按 group_key 分组
    :param dict_list: 字典列表
    :param group_key: 分组的 key
    :param sort_key: 排序的 key（可选，如果不传则只分组不排序）
    :param reverse: 是否降序排序（默认升序）
    :return: 排序后分组的结果
    """
    # 1. 先对整个列表排序（如果传入了 sort_key）
    if sort_key:
        dict_list.sort(key=lambda x: x[sort_key], reverse=reverse)

    # 2. 再分组
    grouped = defaultdict(list)
    for item in dict_list:
        grouped[item[group_key]].append(item)

    return list(grouped.values())


def count_leading_positives(number_list):
    count = 0
    for num in number_list:
        if num > 0:
            count += 1
        else:
            break  # 遇到0或负数，终止循环
    return count


def left_right_selection(location_information_lists_target_left, location_information_lists_target_right,
                         location_information_of_ev, signal):
    print("left_right_selection")
    location_information_lists_target_left = sorted(location_information_lists_target_left,
                                                    key=lambda x: x[
                                                        'position'])
    location_information_lists_target_right = sorted(location_information_lists_target_right,
                                                     key=lambda x: x[
                                                         'position'])

    location_information_of_ev = location_information_of_ev[0]  # {EV's虚拟编号:N, 位置:x, 当前车道:L}
    position_of_ev = location_information_of_ev['position']  # EV's x 整数

    behind_location_information_lists_target_left = [d for d in location_information_lists_target_left if
                                                     d['position'] < position_of_ev]
    front_location_information_lists_target_left = [d for d in location_information_lists_target_left if
                                                    d['position'] > position_of_ev]

    behind_location_information_lists_target_right = [d for d in location_information_lists_target_right if
                                                      d['position'] < position_of_ev]
    front_location_information_lists_target_right = [d for d in location_information_lists_target_right if
                                                     d['position'] > position_of_ev]

    direction = "Left"

    if signal == 'Active':  # 策略：无车/无后车/无前车/间距：前车-后车
        if not behind_location_information_lists_target_left and not front_location_information_lists_target_left:
            direction = "Left"
        elif not behind_location_information_lists_target_right and not front_location_information_lists_target_right:
            direction = "Right"
        else:  # 此时左右都不为空
            if not behind_location_information_lists_target_left:
                direction = "Left"
            elif not behind_location_information_lists_target_right:
                direction = "Right"
            else:  # 此时左右方向后方都有车
                if not front_location_information_lists_target_left:
                    direction = "Left"
                elif not front_location_information_lists_target_right:
                    direction = "Right"
                else:  # 此时左右方向前后方都有车
                    distance_left = front_location_information_lists_target_left[0]['position'] - behind_location_information_lists_target_left[-1]['position']
                    distance_right = front_location_information_lists_target_right[0]['position'] - behind_location_information_lists_target_right[-1]['position']
                    if distance_left >= distance_right:
                        direction = "Left"
                    else:
                        direction = "Right"

    elif signal == 'Passive':  # 策略：无车/无后车/间距：变道车辆-后车
        if not behind_location_information_lists_target_left and not front_location_information_lists_target_left:
            direction = "Left"
        elif not behind_location_information_lists_target_right and not front_location_information_lists_target_right:
            direction = "Right"
        else:  # 此时左右都不为空
            if not behind_location_information_lists_target_left:
                direction = "Left"
            elif not behind_location_information_lists_target_right:
                direction = "Right"
            else:  # 此时左右方向后方都有车
                # 若两侧都有车，找后车离的远的（但仍需要判断，并不会立即变道）（因为在同一个路段，左右两侧车辆的速度差异不会太大，忽略速度以及加速度，先考虑距离）
                distance_left = position_of_ev - behind_location_information_lists_target_left[-1]['position']
                distance_right = position_of_ev - behind_location_information_lists_target_right[-1]['position']
                if distance_left >= distance_right:
                    direction = "Left"
                else:
                    direction = "Right"

    if direction == "Left":
        return location_information_lists_target_left, direction
    elif direction == "Right":
        return location_information_lists_target_right, direction


def protocol_lctad(x_b, x_f, direction, signal, t_interval, t_wait, t_lane_change):
    lane_change_command = None
    exit_signal = 0

    if not x_b and x_f:
        t_b = float('inf')
        step_f = count_leading_positives(x_f)
        t_f = t_interval * (step_f - 1)
        #print(f"t_b = 无穷大, t_f = {t_f}")
    elif not x_f and x_b:
        t_f = float('inf')
        step_b = count_leading_positives(x_b)
        t_b = t_interval * (step_b - 1)
        #print(f"t_b = {t_b}, t_f = 无穷大")

    elif not x_b and not x_f:
        t_b = float('inf')
        t_f = float('inf')
        #print(f"t_b = 无穷大, t_f = 无穷大")
    else:  # x_b and x_f
        step_b = count_leading_positives(x_b)
        step_f = count_leading_positives(x_f)

        t_b = t_interval * (step_b - 1)
        t_f = t_interval * (step_f - 1)
        #print(f"t_b = {t_b}, t_f = {t_f}")

    if t_b >= t_lane_change and t_f >= t_lane_change:
        lane_change_command = f"建议立即向{direction}变道"
        exit_signal = 1

    elif t_b < t_lane_change <= t_f:  # elif t_b < t_lane_change and t_f >= t_lane_change:
        lane_change_command = f"保持当前车道，并等待被{direction}方向后车超越{t_wait}秒后，再次执行变道判断"

    elif t_f < t_lane_change <= t_b:  # elif t_b >= t_lane_change and t_f < t_lane_change
        lane_change_command = f"保持当前车道，并等待超过{direction}方向前车{t_wait}秒后，再次执行变道判断"

    elif t_b < t_lane_change and t_f < t_lane_change:
        if signal == 'Active':
            lane_change_command = f"保持当前车道并适当加速，等待超过{direction}方向前车{t_wait}秒后，再次执行变道判断"
        elif signal == 'Passive':
            lane_change_command = f"保持当前车道并适当减速，等待被{direction}方向后车超越{t_wait}秒后，再次执行变道判断"

    return lane_change_command, exit_signal


def protocol_one_round(location_information_lists_target, location_information_of_ev, direction, signal, t_interval,
                       t_wait, t_max, t_lane_change, round_id):

    # 对于无前/后车情况进行讨论，找到LB LF/RB RF
    location_information_lists_target = sorted(location_information_lists_target,
                                               key=lambda x: x[
                                                   'position'])  # 按x排序后的目标道路位置信息列表(后面find_closest_elements又进行了排序，可优化)

    location_information_of_ev = location_information_of_ev[0]  # {EV's虚拟编号:N, 位置:x, 当前车道:L}
    position_of_ev = location_information_of_ev['position']  # EV's x 整数

    behind_location_information_lists_target = [d for d in location_information_lists_target if
                                                d['position'] < position_of_ev]
    front_location_information_lists_target = [d for d in location_information_lists_target if
                                               d['position'] > position_of_ev]

    if not behind_location_information_lists_target and not front_location_information_lists_target:
        print("目标车道无车，建议立刻变道")
        lane_change_command = f"建议立即向{direction}变道"
        exit_signal = 1

    elif not behind_location_information_lists_target:
        print("目标车道无后车")
        location_information_of_xf = front_location_information_lists_target[0]  # 找到LF/RF {虚拟编号:N, 位置:x, 当前车道:L}
        x_f = compute_distance_list(t_interval, t_max, location_information_of_ev, location_information_of_xf, round_id)
        x_b = None
        #print(f"x_f = {x_f}")
        #print(f"x_b = {x_b}")
        lane_change_command, exit_signal = protocol_lctad(x_b, x_f, direction, signal, t_interval, t_wait,
                                                          t_lane_change)

    elif not front_location_information_lists_target:
        #print("目标车道无前车")
        location_information_of_xb = behind_location_information_lists_target[-1]  # 找到LB/RB {虚拟编号:N, 位置:x, 当前车道:L}
        x_b = compute_distance_list(t_interval, t_max, location_information_of_ev, location_information_of_xb, round_id)
        x_f = None
        #print(f"x_f = {x_f}")
        #print(f"x_b = {x_b}")
        lane_change_command, exit_signal = protocol_lctad(x_b, x_f, direction, signal, t_interval, t_wait,
                                                          t_lane_change)

    else:
        print("目标车道前后车都存在")
        location_information_of_xb = behind_location_information_lists_target[-1]  # 找到LB/RB {虚拟编号:N, 位置:x, 当前车道:L}
        location_information_of_xf = front_location_information_lists_target[0]  # 找到LF/RF {虚拟编号:N, 位置:x, 当前车道:L}

        x_b = compute_distance_list(t_interval, t_max, location_information_of_ev, location_information_of_xb, round_id)
        x_f = compute_distance_list(t_interval, t_max, location_information_of_ev, location_information_of_xf, round_id)
        #print(f"x_f = {x_f}")
        #print(f"x_b = {x_b}")

        lane_change_command, exit_signal = protocol_lctad(x_b, x_f, direction, signal, t_interval, t_wait,
                                                          t_lane_change)
    print(f"exit_signal = {exit_signal}")
    return lane_change_command, exit_signal


def protocol_mpclc(args):
    [args["request_virtual_number"],
     args["request_position"],
     args["request_lane_change_direction"],
     args["request_current_lane"],
     args["request_service_signal"]] = get_lc_request()  # 获取变道申请信息[虚拟编号, 位置, 变道方向, 当前车道, 服务信号]

    exit_signal = 0

    for i in range(args["maximum_iteration"]):
        print(f"————————————————现在为第{i}轮循环——————————————————————————————————————————————————————")
        lane_change_command = None

        location_information_lists = get_location_information_lists(
            i)  # 附近车辆将自己车辆的位置信息Location Information ={虚拟编号:N, 位置:x, 当前车道:L} 发送给RSU
        # location_information_lists中每个元素为字典{虚拟编号:N, 位置:x, 当前车道:L}

        location_information_of_ev = [d for d in location_information_lists if
                                      d.get('virtual_number') == args["request_virtual_number"]]  # 注意格式多一层列表
        #print(f"location_information_of_ev:{location_information_of_ev}")

        location_information_lists = sort_and_group_dicts(location_information_lists, 'current_lane', 'current_lane')
        #print(f"location_information_lists:{location_information_lists}")

        if args["request_lane_change_direction"] == "Left":
            location_information_lists_target = location_information_lists[args["request_current_lane"] - 2]
            #print(f"location_information_lists_target:{location_information_lists_target}")
            print("变道方向:Left")

            lane_change_command, exit_signal = protocol_one_round(location_information_lists_target,
                                                                  location_information_of_ev,
                                                                  args["request_lane_change_direction"],
                                                                  args["request_service_signal"],
                                                                  args["interval_time"],
                                                                  args["waiting_time"],
                                                                  args["maximum_detection_time"],
                                                                  args[
                                                                      "time_required_to_change_lanes"],
                                                                  i)  # Location Information lists, EV’s Location Information, D, S, Δt, Twait, Tmax

        elif args["request_lane_change_direction"] == "Right":
            location_information_lists_target = location_information_lists[args["request_current_lane"]]
            #print(f"location_information_lists_target:{location_information_lists_target}")
            print("变道方向:Right")
            lane_change_command, exit_signal = protocol_one_round(location_information_lists_target,
                                                                  location_information_of_ev,
                                                                  args["request_lane_change_direction"],
                                                                  args["request_service_signal"],
                                                                  args["interval_time"],
                                                                  args["waiting_time"],
                                                                  args[
                                                                      "maximum_detection_time"],
                                                                  args[
                                                                      "time_required_to_change_lanes"],
                                                                  i)  # Location Information lists, EV’s Location Information, D, S, Δt, Twait, Tmax

        elif args["request_lane_change_direction"] == "None":
            location_information_lists_target_left = location_information_lists[args["request_current_lane"] - 2]
            location_information_lists_target_right = location_information_lists[args["request_current_lane"]]
            print("不定向变道")



            # 判断哪边车辆稀疏
            location_information_lists_target, args["request_lane_change_direction"] = left_right_selection(
                location_information_lists_target_left,
                location_information_lists_target_right,
                location_information_of_ev,
                args["request_service_signal"])

            #print(f"location_information_lists_target:{location_information_lists_target}")
            print(f'变道方向:{args["request_lane_change_direction"]}')


            lane_change_command, exit_signal = protocol_one_round(location_information_lists_target,
                                                                  location_information_of_ev,
                                                                  args["request_lane_change_direction"],
                                                                  args["request_service_signal"],
                                                                  args["interval_time"],
                                                                  args["waiting_time"],
                                                                  args[
                                                                      "maximum_detection_time"],
                                                                  args[
                                                                      "time_required_to_change_lanes"],
                                                                  i)  # Location Information lists, EV’s Location Information, D, S, Δt, Twait, Tmax

        if exit_signal == 1:
            return lane_change_command
        elif exit_signal == 0:
            print(f"等待指令：{lane_change_command}")  # 这里的lane_change_command为等待指令，可变更名称

    if exit_signal == 0:
        lane_change_command = "道路拥堵，不可变道"
        return lane_change_command


def main(args):
    lane_change_command = protocol_mpclc(args)
    print(f"lane_change_command = {lane_change_command}")


if __name__ == '__main__':

    args = get_args()

    start = 9
    stop = 50
    step = 1
    l =[]

    for i in range(start,stop,step):
        args["interval_time"] = args["interval_time"] + 0.01
        #print(args["interval_time"])
        time1 = time.time()
        for _ in range(1000):
            main(args)
        time2 = time.time()
        print("实验用时：{:.5f}秒".format(time2 - time1))
        l.append(time2 - time1)

    print(l)






    # for _ in range(1000):
    #     main(args)
    # # main(args)
    # time2 = time.time()
    # print("实验用时：{:.5f}秒".format(time2 - time1))
