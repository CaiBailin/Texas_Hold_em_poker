'''
手机横屏ppi=600
德州扑克计数器第一版
todo
1. 支持横竖屏切换
2. 支持历史记录查看
3. 支持多人不同数据记录或者在线实时处理
'''
import flet as ft
from datetime import datetime

class Count_page:
    def __init__(self):
        self.player_num_upper = 10                                      # 最多玩家数目
        self.new_player_name = "Player"                                 # 默认玩家名称
        self.people_index_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.people_hand_num_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]     # 各玩家初始手数
        self.people_init_index = 0                                      # 初始化玩家索引
        self.default_num_hand_now = 100                                   # 默认当前每手数值
        self.default_multi_power_now = 10                                # 默认当前倍率数值
        self.default_res_chip = 0                                       # 默认剩余码量
        self.default_sur_chip = -1                                      # 默认结余码量
        self.default_p_l = -1                                           # 默认盈亏
        self.default_log_disp = "德州扑克计分"                # log框默认显示
        self.coff   = 0.34
        self.width0 = int(350 * self.coff)
        self.width1 = int(700 * self.coff)
        self.width2 = int(300 * self.coff)
        self.width3 = int(420 * self.coff)
        self.width4 = int(100 * self.coff)
        self.height0 = int(150* self.coff)
        self.page = None
        self.head_info = None
        self.people_list = None
        self.last_line = None
        self.hand_num_change_log = []
        self.game_is_starting = False

    def create_text_0(self, name, width, height=25, size=15):
        '''创建文本-预设0
        '''
        return ft.Text(name, width=width, height=height, text_align=ft.TextAlign.CENTER, size=size)

    def create_tfiled_0(self, name, width, height=25, disable=False, size=15):
        '''创建文本框-预设0
        '''
        return ft.TextField(value=name, width=width, height=height, \
                            text_align=ft.TextAlign.CENTER, disabled=disable, text_size=size,\
                            border=ft.InputBorder.NONE, filled=True,)

    async def button_sub_clicked(self, e):
        '''按钮减功能
        ---
        减少对应索引人员的手数
        '''
        index = e.control.data
        self.people_list.controls[index].controls[1].controls[1].value -= 1
        if (self.game_is_starting is True):
            player_name = str(self.people_list.controls[index].controls[0].value)
            now_time = str(datetime.now().strftime("%m-%d %H:%M:%S "))
            now_hand_num = str(self.people_list.controls[index].controls[1].controls[1].value)
            log = ft.TextField(disabled=True, value=now_time + player_name + "手数 - 1,当前手数:" + now_hand_num, width=int(self.width3 * 3), \
                               height=self.height0, text_align=ft.TextAlign.CENTER, text_size=15)
            self.hand_num_change_log.append(log)
            self.last_line.controls[1].controls.insert(1, log)
        self.page.update()
    
    async def button_add_clicked(self, e):
        '''按钮加功能
        ---
        增加对应索引人员的手数
        '''
        index = e.control.data
        self.people_list.controls[index].controls[1].controls[1].value += 1
        if (self.game_is_starting is True):
            player_name = str(self.people_list.controls[index].controls[0].value)
            now_time = str(datetime.now().strftime("%m-%d %H:%M:%S "))
            now_hand_num = str(self.people_list.controls[index].controls[1].controls[1].value)
            log = ft.TextField(disabled=True, value=now_time + player_name + "手数 + 1,当前手数:" + now_hand_num, \
                               width=int(self.width3 * 3), \
                               height=self.height0, text_align=ft.TextAlign.CENTER, text_size=15)
            self.hand_num_change_log.append(log)
            self.last_line.controls[1].controls.insert(1, log)
        self.page.update()

    async def log_filt_button_callback(self, e):
        '''filter按钮功能
        '''
        if (self.hand_num_change_log != None):
            player_name = str(self.people_list.controls[e.control.data].controls[0].value)
            filted_log = []
            for log in self.hand_num_change_log:
                if player_name in log.value:
                    filted_log.append(log)
            del self.last_line.controls[1].controls[1:]
            self.page.update()
            # print(filted_log[::-1])
            self.last_line.controls[1].controls.extend(filted_log[::-1])
            self.page.update()

    def create_a_people(self, name, hand_num, res_chip, width, icon_width=50, height=25, index=0):
        '''创建一个玩家列表
        ---
        index: 序号，用来索引self.people_list数值
        '''
        p_name = self.create_tfiled_0(name, width, height=height)
        p_hand_num = self.create_tfiled_0(hand_num, int(width-2*icon_width), disable=True, height=height)
        p_hand_num_block = ft.Row([
            ft.IconButton(ft.Icons.REMOVE, width=icon_width, height=height, data=index, on_click=self.button_sub_clicked),
            p_hand_num,
            ft.IconButton(ft.Icons.ADD, width=icon_width, height=height, data=index, on_click=self.button_add_clicked)
        ], spacing=0)
        p_res_chip = self.create_tfiled_0(res_chip, width, height=height)
        p_sur_chip = self.create_tfiled_0(self.default_sur_chip, width, disable=True, height=height)
        p_p_l_chip = self.create_tfiled_0(self.default_p_l, width, disable=True, height=height)
        log_filt_button = ft.TextButton(text="filter", width=self.width2, height=self.height0,\
                                          data=index, adaptive=True, on_click=self.log_filt_button_callback)
        people = ft.Row([
            p_name, p_hand_num_block, p_res_chip, p_sur_chip, p_p_l_chip, log_filt_button
        ], spacing=0)

        return people

    async def add_people2sheet(self, e):
        '''添加玩家到表格中
        ---
        e.control.data 输入是人员索引 self.people_init_index
        但是 e.control.data 和 self.people_init_index 内存分离
        '''
        if (self.people_init_index < self.player_num_upper):
            people_i = self.create_a_people(self.new_player_name+str(self.people_index_list[self.people_init_index]), \
                                            self.people_hand_num_list[self.people_init_index], self.default_res_chip, \
                                            self.width3, index=self.people_init_index, height=self.height0)
            self.people_init_index += 1
            self.people_list.controls.append(people_i)
            self.page.update()

    def count_sur_chip(self, player_i:int):
        '''计算结余码量
        '''
        res_chip = int(self.people_list.controls[player_i].controls[2].value)
        every_hand_num_now = int(self.head_info.controls[0].value)
        hand_num = int(self.people_list.controls[player_i].controls[1].controls[1].value)
        return int(res_chip - every_hand_num_now * hand_num)
    
    def count_p_l(self, player_i:int):
        '''计算盈亏
        '''
        sur_chip = int(self.people_list.controls[player_i].controls[3].value)
        multi_power_now = int(self.head_info.controls[1].value)
        return int(sur_chip / multi_power_now)

    async def reset_button_callback(self, e):
        '''重置按钮回调函数
        ---
        '''
        if (self.game_is_starting is False):
            del self.people_list.controls[0:]
            self.people_init_index = 0
            self.hand_num_change_log = []
            del self.last_line.controls[1].controls[1:]
            del self.page.controls[0:]
            count_page = self.create_count_page()
            self.page.add(count_page)
            self.last_line.controls[1].controls[0].value = "重置成功"

        elif (self.game_is_starting is True):
            self.last_line.controls[1].controls[0].value = "无法重置，请先停止游戏"
        self.page.update()

    async def start_button_callback(self, e):
        '''开始按钮回调函数
        ---
        单击开始按钮，会判断当前所有数值然后对各玩家结余码量和盈亏进行数据更新，同时log显示会提示游戏开始
        '''
        if (self.game_is_starting is False):
            for i in range(self.people_init_index):
                sur_chip_data = self.count_sur_chip(i)
                self.people_list.controls[i].controls[3].value = sur_chip_data
                p_l_data = self.count_p_l(i)
                self.people_list.controls[i].controls[4].value = p_l_data
            self.last_line.controls[1].controls[0].value = "玩的愉快"
            if (len(self.last_line.controls[1].controls) > 1):
                del self.last_line.controls[1].controls[1:]
            self.hand_num_change_log = []
            self.last_line.controls[2].text = "Finish"
            self.game_is_starting = True
        elif (self.game_is_starting is True):
            for i in range(self.people_init_index):
                sur_chip_data = self.count_sur_chip(i)
                self.people_list.controls[i].controls[3].value = sur_chip_data
                p_l_data = self.count_p_l(i)
                self.people_list.controls[i].controls[4].value = p_l_data
            self.last_line.controls[1].controls[0].value = "游戏结束"
            self.last_line.controls[2].text = "Start!"
            self.game_is_starting = False
        self.page.update()

    async def logo_cont_callback(self, e):
        if (e.control.data == 0):
            e.control.bgcolor = ft.Colors.RED_700
        elif (e.control.data == 1):
            e.control.bgcolor = ft.Colors.PINK_700
        elif (e.control.data == 2):
            e.control.bgcolor = ft.Colors.PURPLE_700
        elif (e.control.data == 3):
            e.control.bgcolor = ft.Colors.DEEP_PURPLE_700
        elif (e.control.data == 4):
            e.control.bgcolor = ft.Colors.INDIGO_700
        elif (e.control.data == 5):
            e.control.bgcolor = ft.Colors.BLUE_700
        elif (e.control.data == 6):
            e.control.bgcolor = ft.Colors.LIGHT_BLUE_700
        elif (e.control.data == 7):
            e.control.bgcolor = ft.Colors.CYAN_700
        elif (e.control.data == 8):
            e.control.bgcolor = ft.Colors.TEAL_700
        elif (e.control.data == 9):
            e.control.bgcolor = ft.Colors.GREEN_700
        elif (e.control.data == 10):
            e.control.bgcolor = ft.Colors.LIGHT_GREEN_700
        elif (e.control.data == 11):
            e.control.bgcolor = ft.Colors.LIME_700
        elif (e.control.data == 12):
            e.control.bgcolor = ft.Colors.YELLOW_700
        elif (e.control.data == 13):
            e.control.bgcolor = ft.Colors.AMBER_700
        elif (e.control.data == 14):
            e.control.bgcolor = ft.Colors.ORANGE_700
        else:
            e.control.bgcolor = ft.Colors.DEEP_ORANGE_700
        e.control.data += 1
        if (e.control.data >= 16):
            e.control.data = 0
        self.page.update()

    def create_count_page(self):
        '''创建记数界面
        '''
        # 顶部显示
        hand_num_now_tfiled = ft.TextField(label="当前每手", border="underline", \
                                           disabled=False, value=self.default_num_hand_now, \
                                           width=self.width0, height=self.height0, \
                                           text_align=ft.TextAlign.CENTER, text_size=15)
        multi_power_now_tfiled = ft.TextField(label="当前倍率", border="underline", \
                                              disabled=False, value=self.default_multi_power_now, width=self.width0, \
                                              height=self.height0, text_align=ft.TextAlign.CENTER, text_size=15)
        logo_text = ft.Text("xx出品 V1.3", \
                            # width=self.width1-10, height=self.height0-10, text_align=ft.TextAlign.CENTER, \
                            # size=20, color=ft.Colors.WHITE, bgcolor=ft.Colors.BLUE_600 \
                            )
        logo_text_cont = ft.Container(
                    content=logo_text,
                    margin=5,
                    padding=5,
                    alignment=ft.alignment.center,
                    bgcolor=ft.Colors.PINK_ACCENT_200,
                    width=self.width1,
                    height=self.height0,
                    data=0,
                    ink=True,
                    on_click=self.logo_cont_callback,
                )
        reset_buttom = ft.TextButton(text="Reset", data=0, width=self.width3, height=self.height0,\
                                     on_click=self.reset_button_callback, adaptive=True)
        self.head_info = ft.Row([hand_num_now_tfiled, multi_power_now_tfiled, logo_text_cont, reset_buttom
                            ], vertical_alignment=ft.CrossAxisAlignment.END, spacing=0)
        # 表头显示
        sheet_head_name = ft.TextField(value="昵称", width=self.width3, height=self.height0, text_align=ft.TextAlign.CENTER, text_size=15,\
                                       border=ft.InputBorder.NONE, filled=True, disabled=True)
        sheet_head_hand_num = ft.TextField(value="手数", width=self.width3, height=self.height0, text_align=ft.TextAlign.CENTER, \
                                           text_size=15, border=ft.InputBorder.NONE, filled=True, disabled=True)
        sheet_head_res_chip = ft.TextField(value="剩余码量", width=self.width3, height=self.height0, text_align=ft.TextAlign.CENTER, \
                                           text_size=15, border=ft.InputBorder.NONE, filled=True, disabled=True)
        sheet_head_surplus_chip = ft.TextField(value="结余码量", width=self.width3, height=self.height0, text_align=ft.TextAlign.CENTER, \
                                               text_size=15, border=ft.InputBorder.NONE, filled=True, disabled=True)
        sheet_head_p_l = ft.TextField("盈亏", width=self.width3, height=self.height0, text_align=ft.TextAlign.CENTER, \
                                      text_size=15, border=ft.InputBorder.NONE, filled=True, disabled=True)
        sheet_head = ft.Row([sheet_head_name, sheet_head_hand_num, sheet_head_res_chip, \
                            sheet_head_surplus_chip, sheet_head_p_l], spacing=0)
        # 玩家列表信息显示
        self.people_list = ft.Column([], alignment=ft.MainAxisAlignment.START, spacing=0) # 玩家列表没有间隙
        # 开始等功能按键显示
        add_people_button = ft.TextButton(text="Add people", data=self.people_init_index, \
                                          on_click=self.add_people2sheet, width=self.width3, \
                                          height=self.height0, adaptive=True)
        log_display_head = ft.TextField(value=self.default_log_disp, disabled=True, width=int(self.width3 * 3), height=self.height0,\
                                        label="消息提示", text_align=ft.TextAlign.CENTER)
        log_display_block = ft.Column([log_display_head], spacing=0)
        start_game_button = ft.TextButton(text="Start!", width=self.width3, height=self.height0,\
                                          on_click=self.start_button_callback, adaptive=True)
        self.last_line = ft.Row([add_people_button, log_display_block, start_game_button], spacing=0, \
                                #alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                vertical_alignment=ft.CrossAxisAlignment.START,
                                )

        return ft.Column([self.head_info, sheet_head, self.people_list, self.last_line], alignment=ft.MainAxisAlignment.START, spacing=0)

    def main(self, page: ft.Page):
        self.page = page
        self.page.scroll = True
        self.page.scroll = "adaptive"
        self.page.vertical_alignment = ft.MainAxisAlignment.START

        count_page = self.create_count_page()

        self.page.add(count_page)

if __name__ == "__main__":
    cnt_p = Count_page()
    ft.app(target=cnt_p.main)
