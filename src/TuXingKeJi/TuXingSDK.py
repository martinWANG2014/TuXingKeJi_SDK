from src.TuXingKeJi.enumHelper import ATGColor, QH, AllMode, MVColor, XXFX, JXSOF, OFFON, ISRColor, ISRRT, LandStop, FliPpt, Color, \
    State, ZY, Rotate, SX, Mangtion, Direction
from src.TuXingKeJi.peripheral import Peripheral
from src.TuXingKeJi.serialHelper import hex_str


# 红外灯
# 红外灯[ISR_RT]
def get_infrared_hex_code(code: ISRRT):
    return code.value


class TuXingSDK:
    def __init__(self, peripheral: Peripheral):
        self.__peripheral = peripheral

    def start(self):
        self.__peripheral.start()

    def stop(self):
        self.__peripheral.stop()

    # 颜色判断
    # 前方颜色
    def get_current_color(self):
        color = self.__peripheral.parse_data("DDAA", "FEFE", 40, 42)
        if color == "10":
            return "红"
        elif color == "20":
            return "蓝"
        elif color == "30":
            return "黄"
        else:
            return "无"

    # 获取电压
    # 飞机电压
    def get_current_vcc(self):
        return int(self.__peripheral.parse_data("DDAA", "FEFE", 8, 12), 16)

    # 获取高度
    # 当前高度
    def get_current_height(self):
        return int(self.__peripheral.parse_data("DDAA", "FEFE", 12, 16), 16)

    # 获取二维码编号
    # 二维码ID
    def get_id_qr_code(self):
        return int(self.__peripheral.parse_data("DDAA", "FEFE", 44, 48), 16)

    # 获取版本号
    # 固件版本
    def get_version(self):
        return int(self.__peripheral.parse_data("DDAA", "FEFE", 16, 22), 16) / 100.0

    # 获取信号强度
    # 无线信号强度
    def get_wifi_strength(self):
        return str(int(self.__peripheral.parse_data("DDAA", "FEFE", 34, 36), 16)) + "%"

    # 获取openmv模式
    # 视觉模式
    def get_mode_open_mv(self):
        open_mv_mode = self.__peripheral.parse_data("DDAA", "FEFE", 42, 44)
        if open_mv_mode == "F3":
            return "循线模式"
        elif open_mv_mode == "F6":
            return "二维码模式"
        elif open_mv_mode == "F7":
            return "色块定位模式"
        else:
            return "常规模式"

    # 获取前方距离
    # TOF测距（前）cm
    def get_data_ultrason_front(self):
        return int(self.__peripheral.parse_data("DDAA", "FEFE", 38, 40), 16)

    # 获取后方距离
    # TOF测距（后）cm
    def get_data_ultrason_back(self):
        return int(self.__peripheral.parse_data("DDAA", "FEFE", 30, 32), 16)

    # 获取左方距离
    # TOF测距（左）cm
    def get_data_ultrason_left(self):
        return int(self.__peripheral.parse_data("DDAA", "FEFE", 32, 34), 16)

    # 获取右方距离
    # TOF测距（右）cm
    def get_data_ultrason_right(self):
        return int(self.__peripheral.parse_data("DDAA", "FEFE", 36, 38), 16)

    # 获取下方距离
    # TOF测距（下）cm
    def get_data_ultrason_down(self):
        return int(self.__peripheral.parse_data("DDAA", "FEFE", 28, 30), 16)

    # 位置值清零
    # 相对于[distance]号标签清除误差
    def eliminate_error_to_label(self, distance: int):
        msg = " ".join(["AA FA 45", hex_str("%04X" % distance, 4), "00 00 00 00 00 00 00 FE"])
        self.__peripheral.write(msg)

    # 怠速
    # 无人机怠速
    def idle_mode_uav(self):
        msg = "AA FA 2B 00 00 00 00 00 00 00 00 00 FE"
        self.__peripheral.write(msg)

    # 初始化
    # 无人机初-始化
    def initialize_uav(self):
        msg = "AA FA 21 00 00 00 00 00 00 00 00 00 FE"
        self.__peripheral.write(msg)

    # 起飞
    # 起飞[distance]cm
    def take_off_with_height(self, distance: int):
        msg = " ".join(["AA FA 22", hex_str("%04X" % distance, 4), "00 00 00 00 00 00 00 FE"])
        self.__peripheral.write(msg)

    # 飞行速度
    # 设置飞行速度[distance]
    def set_speed(self, distance: int):
        msg = " ".join(["AA FA 28", hex_str("%04X" % distance, 4), "00 00 00 00 00 00 00 FE"])
        self.__peripheral.write(msg)

    # 移动
    # 向 [direction] 飞[distance]cm
    def move_with_direction_and_distance(self, direction: Direction, distance: int):
        msg = " ".join(["AA FA 23", direction.value, hex_str("%04X" % distance, 4), "00 00 00 00 00 00 FE"])
        self.__peripheral.write(msg)

    # 时间移动
    # 向 [mangtion] 飞[distance]*0.01(秒)
    def move_with_direction_and_time_limitation(self, direction: Mangtion, distance: int):
        msg = " ".join(["AA FA 51", direction.value, hex_str("%04X" % distance, 4), "00 00 00 00 00 00 FE"])
        self.__peripheral.write(msg)

    # 斜线移动
    # 向[QH][qh_num][ZY][zy_num][SX][sx_num](厘米)
    def move_slash(self, qh: QH, qh_num: int, zy: ZY, zy_num: int, sx: SX, sx_num: int):
        msg = " ".join(
            ["AA FA 24", qh.value, hex_str("%04X" % qh_num, 4), zy.value, hex_str("%04X" % zy_num, 4), sx.value,
             hex_str("%04X" % sx_num, 4), "FE"])
        self.__peripheral.write(msg)

    # 旋转
    # [Rotate]旋转[distance]度
    def rotate(self, rotate: Rotate, distance: int):
        msg = " ".join(["AA FA 25", rotate.value, hex_str("%04X" % distance, 4), "00 00 00 00 00 00 FE"])
        self.__peripheral.write(msg)

    # 环绕
    # 以无人机[QH][distance]cm  [ZY][distance2]cm为中心 [Rotate]环绕[distance3]°  用时[distance4]秒
    def fly_surround(self, qh: QH, distance: int, zy: ZY, distance2: int, rotate_direction: Rotate, distance3: int,
                     distance4: int):
        msg = " ".join(["AA FA 52", qh.value, hex_str("%02X" % distance), zy.value, hex_str("%02X" % distance2),
                        hex_str("%04X" % distance3, 4), rotate_direction.value, hex_str("%02X" % distance4), "00 FE"])
        self.__peripheral.write(msg)

    # 灯光控制
    # 设置飞机大灯[clour]色[state]
    def set_light_color_mode(self, color: Color = Color.BLACK, mode: State = State.BRIGHT):
        msg = " ".join(["AA FA 26", color.value, mode.value, "00 00 00 00 00 00 00 FE"])
        self.__peripheral.write(msg)

    # 翻滚
    # 4D翻滚[flippt]
    def flip(self, direction: FliPpt):
        msg = " ".join(["AA FA 29", direction.value, "00 00 00 00 00 00 00 00 FE"])
        self.__peripheral.write(msg)

    # 降落
    # [land_stop]降落——[distance]速度
    def landing_by_mode_and_speed(self, mode: LandStop, distance: int):
        msg = " ".join(["AA FA", mode.value, hex_str("%04X" % distance, 4), "00 00 00 00 00 00 00 FE"])
        self.__peripheral.write(msg)

    # 拍照
    # 拍一张照片照
    def take_a_photo(self):
        msg = "AA FA 2C 00 00 00 00 00 00 00 00 00 FE"
        self.__peripheral.write(msg)

    # 激光定高
    # 激光定高[OFFON]
    def set_status_laser(self, status: OFFON):
        msg = " ".join(["AA FA 40 00 00 00", status.value, "00 00 00 00 00 FE"])
        self.__peripheral.write(msg)

    # 定位模式
    # 定位模式[OFFON]
    def set_status_relocation(self, status: OFFON):
        msg = " ".join(["AA FA 47 00 00 00", status.value, "00 00 00 00 00 FE"])
        self.__peripheral.write(msg)

    # 强制设定高度
    # 强制设定[distance]为当前高度
    def set_mandatory_height(self, distance: int):
        msg = " ".join(["AA FA 46 00 00 00", hex_str("%02X" % distance), "00 00 00 00 00 FE"])
        self.__peripheral.write(msg)

    # 红外发射
    # 发射红外数据[ISR_RT]
    def set_status_infrared(self, status: ISRRT):
        msg = " ".join(["AA FA 30 00", status.value, "00 00 00 00 00 FE"])
        self.__peripheral.write(msg)

    # 红外发射
    # 发射红外数据[NUMT1]
    def emit_infrared_data(self, data: str):
        msg = " ".join(["AA FA 30 00", data, "00 00 00 00 00 FE"])
        self.__peripheral.write(msg)

    # 发射红外点阵
    # 红外点阵显示[ISR_col]色单个字符[distance]
    def display_infrared_matrix_with_color_and_size(self, color: ISRColor, nb_characters: int):
        msg = " ".join(["AA FA 30 00 FF", color.value, hex_str("%02X" % nb_characters), "00 00 00 00 00 FE"])
        self.__peripheral.write(msg)

    # 数据回传
    # 数据回传[OFFON]
    def set_status_data_callback(self, status: OFFON = OFFON.ON):
        msg = " ".join(["AA FA D0", status.value, "00 00 00 00 00 00 00 00 FE"])
        self.__peripheral.write(msg)

    # 磁吸
    # 电磁铁[OFFON]
    def set_status_electromagnet(self, status: OFFON = OFFON.ON):
        msg = " ".join(["AA FA 31 00 FF FF", status.value, "00 00 00 00 00 FE"])
        self.__peripheral.write(msg)

    # 舵机
    # 舵机[distance]°
    def set_angle_steering_gear(self, distance: int):
        msg = " ".join(["AA FA 33", hex_str("%02X" % distance), "00 00 00 00 00 00 00 00 FE"])
        self.__peripheral.write(msg)

    # 机械手
    # 机械手[JXS_OF]
    def set_status_grasper_hand(self, status: JXSOF):
        msg = " ".join(["AA FA 34", status.value, "00 00 00 00 00 00 00 00 FE"])
        self.__peripheral.write(msg)

    # 机械手
    # 机械手[distance]°
    def set_angle_grasper_hand(self, distance: int):
        msg = " ".join(["AA FA 34", hex_str("%02X" % distance), "00 00 00 00 00 00 00 00 FE"])
        self.__peripheral.write(msg)

    # 激光
    # 发射激光
    def emit_laser(self):
        msg = "AA FA 35 00 00 00 00 00 00 00 00 00 FE"
        self.__peripheral.write(msg)

    # 循线方向
    # 向[XXFX]循线飞行
    def navigate_by_line_on_direction(self, direction: XXFX = XXFX.FRONT):
        msg = " ".join(["AA FA 41 00 00 00", direction.value, "00 00 00 00 00 FE"])
        self.__peripheral.write(msg)

    # 颜色定位
    # 定位颜色[MV_COLOUR]
    def point_to_color(self, color: MVColor = MVColor.RED):
        msg = " ".join(["AA FA 42 00 00 00", color.value, "00 00 00 00 00 FE"])
        self.__peripheral.write(msg)

    # 二维码模式
    # 切换为[ALL_mode]模式
    def change_mode(self, mode: AllMode = AllMode.BY_DEFAULT):
        msg = " ".join(["AA FA A0", mode.value, "00 00 00 00 00 00 00 00 FE"])
        self.__peripheral.write(msg)

    # 初始标签地址
    # 起飞点二维码编号[distance]
    def distance_for_departure_qr_code(self, distance: int):
        msg = " ".join(["AA FA A1", hex_str("%02X" % distance), "00 00 00 00 00 00 00 00 FE"])
        self.__peripheral.write(msg)

    # 标签间距，根据实际场地调整，单位cm
    # 二维码标签间距[distance]cm
    def set_distance_between_label_qr_code(self, distance: int):
        msg = " ".join(["AA FA A2", hex_str("%02X" % distance), "00 00 00 00 00 00 00 00 FE"])
        self.__peripheral.write(msg)

    # 起飞高度
    # 二维码模式起飞[distance]cm
    def take_off_by_mode_qr_code_with_distance(self, distance: int):
        msg = " ".join(["AA FA A4", hex_str("%02X" % distance), "00 00 00 00 00 00 00 00 FE"])
        self.__peripheral.write(msg)

    # 目标标签
    # 直达[distance]标签，高度[distance2]
    def go_direct_to_label_with_height(self, distance: int, distance2: int):
        msg = " ".join(["AA FA A5", hex_str("%02X" % distance), hex_str("%02X" % distance2), "00 00 00 00 00 00 00 FE"])
        self.__peripheral.write(msg)

    # 期望标签
    # 飞向[distance]标签，高度[distance2]
    def go_to_label_with_height(self, distance: int, distance2: int):
        msg = " ".join(["AA FA A7", hex_str("%04X" % distance, 4), hex_str("%02X" % distance2), "00 00 00 00 00 00 FE"])
        self.__peripheral.write(msg)

    # 定点当前标签
    # 定点当前标签，高度[distance]
    def point_to_current_label_with_height(self, distance: int):
        msg = " ".join(["AA FA A6", hex_str("%04X" % distance, 4), "00 00 00 00 00 00 00 FE"])
        self.__peripheral.write(msg)

    # 定点当前颜色
    # 定点当前颜色块，高度[distance]cm
    def point_to_current_color_block_with_height(self, distance: int):
        msg = " ".join(["AA FA A5 00", hex_str("%02X" % distance), "00 00 00 00 00 00 00 FE"])
        self.__peripheral.write(msg)

    # 颜色偏差
    # 默认定位在[ATG_COLOUR][QH]方[distance]像素
    def point_to_color_with_direction_and_distance(self, color: ATGColor, qh: QH, distance: int):
        msg = " ".join(["AA FA", color.value, "00 00", qh.value, hex_str("%02X" % distance), "00 00 00 00 00 FE"])
        self.__peripheral.write(msg)

    # 角度校准
    # 飞机航向校准
    def calibration(self):
        msg = "AA FA 2A 00 00 00 00 00 00 00 00 00 FE"
        self.__peripheral.write(msg)
