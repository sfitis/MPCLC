import argparse

def get_args():
    parser = argparse.ArgumentParser()
    # ------- 全局参数
    parser.add_argument("--maximum_iteration", default=3,
                        help="")
    parser.add_argument("--time_required_to_change_lanes", default=3,
                        help="time required to complete lane change")
    parser.add_argument("--waiting_time", default=4,
                        help="")
    parser.add_argument("--maximum_detection_time", default=4,
                        help="")
    parser.add_argument("--interval_time", default=0.1,
                        help="")
    parser.add_argument("--total_number_of_lanes", default=3,
                        help="")

    # ------- 变道申请参数Lc_Request
    parser.add_argument("--request_virtual_number", default=1,
                        help="")
    parser.add_argument("--request_position", default=0,
                        help="")
    parser.add_argument("--request_lane_change_direction", default="None",
                        choices=["None", "Left", "Right"],
                        help="")
    parser.add_argument("--request_current_lane", default=2,
                        help="")
    parser.add_argument("--request_service_signal", default="Passive",
                        choices=["Active", "Passive"],
                        help="")


    args = vars(parser.parse_args())
    return args