'''
flet run --web --port 8888 .\pock_count_v2.py
https://v4.mui.com/zh/components/material-icons/
'''
import flet as ft
from datetime import datetime

class Main:
    def __init__(self):
        self.page               = None                                          # 主页面
        self.func1_page         = None                                          # 功能 1 页面
        self.func2_page         = None                                          # 功能 2 页面
        self.func3_page         = None                                          # 功能 3 页面
        self.all_page           = []
        self.cupertino_actions  = None                                          # 警告对话框
        self.people_datasheet   = None                                          # 存放玩家原始数据
        self.people_list        = None                                          # 玩家数据表格
        self.people_logbase     = None                                          # 玩家历史记录原始数据
        self.people_log_list    = None                                          # 玩家历史记录
        self.hand_num_chan_ale  = None                                          # 修改手数提示框
        self.d_text_size        = 11                                            # 数据表格文本大小
        self.d_height           = 30                                            # 数据表格高度
        self.select_people_ref  = ft.Ref[ft.Text]()                             # 人数修改参考
        self.player_num_now     = 0                                             # 当前玩家数目
        self.everyhand_now      = 0                                             # 当前每手数值
        self.multi_power_now    = 0                                             # 当前倍率数值
        self.player_num_upper   = 99                                            # 最多玩家数目
        self.player_index_list  = range(self.player_num_upper)                  # 玩家序号列表
        self.new_player_name    = "Player"                                      # 默认玩家名称
        self.default_log_disp   = "德州扑克计分"                                 # log框默认显示
        self.hand_num_list      = [0] * self.player_num_upper                   # 手数变化列表
        # self.sur_chip_list      = [0, 0, 0, 0, 0, 
        #                            0, 0, 0, 0, 0]                               # 结余码量
        # self.p_l_chip_list      = [0, 0, 0, 0, 0, 
        #                            0, 0, 0, 0, 0]                               # 盈亏
        # self.res_chip_list      = [0, 0, 0, 0, 0, 
        #                            0, 0, 0, 0, 0]                               # 剩余码量
        # self.player_name_list   = []
        self.start_flag         = False                                         # 开始标志位
    
    def reset_callback(self, e):
        '''重置按钮回调函数
        '''
        if (self.dlg):
            self.page.open(self.dlg)
    
    def handnum_chan_callback(self, e):
        '''修改手数回调函数
        '''
        if (self.hand_num_chan_ale and self.start_flag):
            player_name = e.control.parent.controls[1].value                        # 显示玩家的名称
            self.hand_num_chan_ale.title.value = "玩家"+player_name                 # 修改显示名称
            self.hand_num_chan_ale.title.data  = e.control.parent.controls[0].value # 更新玩家在表格索引
            # 当玩家名称不是数字时，在玩家前面添加一列数字
            self.page.open(self.hand_num_chan_ale)
    
    def hand_num_add(self, e):
        '''手数提示框 +1 按钮回调函数
        '''
        if (self.start_flag):
            # 需要注意， player_name需要是数字
            player_index = int(e.control.parent.title.data)
            self.hand_num_list[player_index] += 1               # 分值加1
            self.people_list.controls[player_index].controls[2].content.value = \
                str(self.hand_num_list[player_index])           # 更新到表格
            self.close_action_callback(e)
            self.page.update()
            now_time = str(datetime.now().strftime("%H:%M:%S"))
            log = ft.Text(now_time + " 手数 ++ 1 " + "当前:" + str(self.hand_num_list[player_index]))
            self.people_log_list.controls[player_index].content.subtitle.controls.insert(0, log)
    
    def hand_num_sub(self, e):
        '''手数提示框 -1 按钮回调函数
        '''
        if (self.start_flag):
            # 需要注意， player_name需要是数字
            player_index = int(e.control.parent.title.data)
            self.hand_num_list[player_index] -= 1               # 分值减1
            self.people_list.controls[player_index].controls[2].content.value = \
                str(self.hand_num_list[player_index])           # 更新到表格
            self.close_action_callback(e)                       # 关闭命令提示窗
            self.page.update()
            now_time = str(datetime.now().strftime("%H:%M:%S"))
            log = ft.Text(now_time + " 手数 -- 1 " + "当前:" + str(self.hand_num_list[player_index]))
            self.people_log_list.controls[player_index].content.subtitle.controls.insert(0, log)

    def add_people_callback(self, e):
        '''加人选择按钮回调函数
        '''
        self.page.open(self.people_num_sheet)

    def people_n_picker_callback(self, e):
        '''选择人数变化回调函数
        '''
        self.select_people_ref.current.value = self.player_index_list[int(e.data)]  # 人数实时变化
        self.player_num_now = self.select_people_ref.current.value                  # 更新人数用于运算
        # 实际上指向内存是 people_datasheet 和 people_logbase，所以数据不会变化
        self.people_list.controls = self.people_datasheet.controls[:self.player_num_now]    # 读取[0-9]个人
        self.people_log_list.controls = self.people_logbase.controls[:self.player_num_now]  # 读取[0-9]个人
        # 如果已经开始游戏，则激活修改
        if (True == self.start_flag):
            for i in range(self.add_buttom.content.content.value):
                self.people_list.controls[i].controls[2].disabled = False                   # 手数激活修改
                self.people_list.controls[i].controls[3].disabled = False                   # 剩余码量激活修改
        self.page.update()
    
    def nav_bar_callback(self, e):
        '''底部导航栏回调函数
        '''
        print("Selected tab:", e.control.selected_index)
        if (self.page != None):
            self.page.remove_at(0)
            if (0 == e.control.selected_index):
                self.page.add(self.func1_page)
            elif (1 == e.control.selected_index):
                self.page.add(self.func2_page)
            else:
                self.page.add(self.func3_page)
            self.page.update()

    def close_action_callback(self, e):
        '''按钮回调函数-执行关闭效果
        '''
        # self.page.add(ft.Text(f"Action clicked: {e.control.text}"))   # 显示 log
        # e.control is the clicked action button, e.control.parent is the corresponding parent dialog of the button
        self.page.close(e.control.parent)                               # 关闭按钮对应父控件
    
    def start_button_callback(self, e):
        '''开始按钮回调函数
        需要注意的控件
        当前每手、当前倍率、人数、剩余码量？开始按钮
        '''
        if (self.hand_num_now_tfiled.content.value != '' and 
            self.multi_power_now_tfiled.content.value != '' and
            self.add_buttom.content.content.value > 0):
            if False == self.start_flag:     # 开始游戏
                ## 取消编辑功能
                self.hand_num_now_tfiled.content.disabled       = True
                self.multi_power_now_tfiled.content.disabled    = True
                self.add_buttom.content.disabled                = False         # 人数可以修改
                self.reset_buttom.content.disabled              = True
                ## 按钮文字改成结束
                e.control.text = '结束'
                for i in range(self.add_buttom.content.content.value):
                    self.people_log_list.controls[i].header.title.value = \
                        '玩家'+self.people_list.controls[i].controls[1].value   # 更新第二页玩家名称
                    self.people_list.controls[i].controls[1].disabled = False   # 名字激活修改
                    self.people_list.controls[i].controls[2].disabled = False   # 手数激活修改
                    self.people_list.controls[i].controls[3].disabled = False   # 剩余码量激活修改
                self.start_flag = True
                # 删除所有结果
                del self.result_dlg.content.controls[:]
            else:                            # 停止游戏
                ## 重新激活
                self.hand_num_now_tfiled.content.disabled       = False
                self.multi_power_now_tfiled.content.disabled    = False
                self.add_buttom.content.disabled                = False
                self.reset_buttom.content.disabled              = False
                e.control.text = '开始'
                every_hand_num_now  = int(self.hand_num_now_tfiled.content.value)
                multi_pow_now       = int(self.multi_power_now_tfiled.content.value)
                for i in range(self.add_buttom.content.content.value):
                    res_chip = int(self.people_list.controls[i].controls[3].value)  # 获取剩余码量
                    hand_num = int(self.hand_num_list[i])  # 获取手数
                    self.people_list.controls[i].controls[1].disabled = False       # 名字激活修改
                    self.people_list.controls[i].controls[2].disabled = True        # 手数无法修改
                    self.people_list.controls[i].controls[3].disabled = True        # 剩余码量无法修改
                    sur_chip = int(res_chip - every_hand_num_now * hand_num)        # 结余码量
                    p_l = int(sur_chip / multi_pow_now)                             # 盈亏

                    log = ft.Text("游戏结束, 结余码量:"+str(sur_chip)+", 盈亏:"+str(p_l))   # 更新到第二页
                    self.people_log_list.controls[i].content.subtitle.controls.insert(0, log)
                    player_info = ft.Text(self.people_log_list.controls[i].header.title.value + 
                                          " 结余码量:"+str(sur_chip)+", 盈亏:"+str(p_l))
                    self.result_dlg.content.controls.append(player_info)
                self.start_flag = False
                # 显示结果
                self.page.open(self.result_dlg)
            self.page.update()
        else:
            pass
            # \todo: 后面添加提示框
        # ！todo

    def change_name_callback(self, e):
        '''玩家名称文本框改变回调函数
        '''
        i = int(e.control.parent.controls[0].value)  # 获取列表index
        self.people_log_list.controls[i].header.title.value = '玩家'+str(e.control.value)   # 更新玩家名称

    def create_tfiled_0(self, name, col=1, height=30, disable=False, t_size=11):
        '''创建文本框-预设0
        无边框，居中显示
        '''
        return ft.TextField(value=name, disabled=disable, height=height,   \
                            text_size=t_size, col=col,
                            border=ft.InputBorder.NONE, text_align=ft.TextAlign.CENTER)

    def main(self, page: ft.Page):
        # page绑定到self.page变量
        self.page = page
        self.page.title = "德州扑克计分"
        self.page.scroll = True

        self.page_init()

    def page_init(self):
        '''创建主页面
        '''
        if (self.page == None):
            return

        # 底部导航栏
        self.page.navigation_bar = ft.CupertinoNavigationBar(
            bgcolor         = ft.Colors.LIME_50,
            inactive_color  = ft.Colors.GREY,
            active_color    = ft.Colors.BLACK,
            on_change       = self.nav_bar_callback,
            destinations    = [
                                ft.NavigationBarDestination(icon=ft.Icons.LOOKS_ONE_ROUNDED, label="计分面板"),
                                ft.NavigationBarDestination(icon=ft.Icons.LOOKS_TWO_ROUNDED, label="历史记录"),
                                ft.NavigationBarDestination(
                                    icon=ft.Icons.LOOKS_3_ROUNDED,
                                    # selected_icon=ft.Icons.BOOKMARK,
                                    label="关于",
                                ),
                            ]
        )

        # 添加页面
        self.func1_page = ft.SafeArea(self.count_page_init())
        self.func2_page = ft.SafeArea(self.history_page_init())
        self.func3_page = ft.SafeArea(self.about_page_init())
        self.page.add(self.func1_page)

    def people_list_init(self):
        '''创建数据表格，未初始化数据
        在这里先把所有的数据给初始化，后面就不会再频繁创建了，只是把指定数据进行显示而已
        字体大小设置为11
        '''
        for i in range(self.player_num_upper):
            index       = self.create_tfiled_0(str(i), col=2, disable=True, t_size=11)
            # 名称，目前是序号
            name        = self.create_tfiled_0('', col=4, disable=False, t_size=11)
            name.on_change=self.change_name_callback    # 修改名称时候同步修改第二页
            # 手数
            hand_n      = ft.CupertinoButton(content=ft.Text('0', color=ft.Colors.YELLOW, size=11), \
                                             col=3, opacity_on_click=0.3,\
                                             disabled=True,                     # 默认无法修改
                                             on_click=self.handnum_chan_callback)
            # 剩余码量
            res_chip    = self.create_tfiled_0('0', col=3, disable=True, t_size=11)
            # 结余码量
            # sur_chip    = self.create_tfiled_0('0', col=3, disable=True, t_size=11)
            # 盈亏
            # p_l_chip    = self.create_tfiled_0('0', col=2, disable=True, t_size=11)
            people      = ft.ResponsiveRow([
                                            index, name, hand_n, res_chip, #sur_chip, p_l_chip
                                            ], spacing=0)
            self.people_datasheet.controls.append(people)

    def count_page_init(self):
        '''计数界面初始化
        '''
        # 顶部显示 # 手机竖屏的话显示两列，横屏显示4列，电脑全屏也显示4列
        ## 当前每手填空框
        self.hand_num_now_tfiled     = ft.Container(ft.TextField(label="当前每手", border="underline", \
                                                            disabled=False, text_align=ft.TextAlign.CENTER), \
                                               col={"xs": 6, "sm": 3})
        ## 当前倍率填空框
        self.multi_power_now_tfiled  = ft.Container(ft.TextField(label="当前倍率", border="underline", \
                                                            disabled=False, text_align=ft.TextAlign.CENTER), \
                                               col={"xs": 6, "sm": 3})
        ## logo
        # logo_text               = ft.Text("小楠出品 V2.0")
        # logo_text_cont          = ft.Container(
        #                                        content=logo_text,
        #                                        margin=5,
        #                                        padding=5,
        #                                        alignment=ft.alignment.center,
        #                                        bgcolor=ft.Colors.PINK_ACCENT_200,
        #                                        data=0,
        #                                        ink=True,
        #                                        col={"xs": 6, "sm": 3}
        #                                        )

        ## 添加人员按钮
        add_button_text         = ft.Container(ft.Text("人数"), \
                                               col={"xs": 2, "sm": 1})
        ### 默认人数是0
        self.add_buttom         = ft.Container(ft.TextButton(content=ft.Text(value=self.player_index_list[0],   \
                                                                             ref=self.select_people_ref),       \
                                                                 on_click=self.add_people_callback),            \
                                               col={"xs": 2, "sm": 1})
        ### 选择列表参数，默认人数是0
        people_n_picker         = ft.CupertinoPicker(
                                              selected_index=0,  # 修改默认人数
                                              magnification=1.22,
                                              squeeze=1.2,
                                              use_magnifier=True,
                                              on_change=self.people_n_picker_callback,
                                              controls=[ft.Text(value=f) for f in self.player_index_list],
                                              )
        ### 选择列表界面
        self.people_num_sheet   = ft.CupertinoBottomSheet(
                                                        people_n_picker,
                                                        height=216,
                                                        padding=ft.padding.only(top=6),
                                                        )

        ## 开始按钮
        start_buttom            = ft.Container(ft.FilledTonalButton(text="开始", data=0, 
                                                                    on_click=self.start_button_callback), \
                                               col={"xs": 4, "sm": 2})

        ## 重置按钮
        self.reset_buttom            = ft.Container(ft.FilledTonalButton(text="重置", data=0,  \
                                                                    icon=ft.icons.WARNING_ROUNDED,  \
                                                                    icon_color=ft.Colors.RED_600,   \
                                                                    style=ft.ButtonStyle(color=ft.Colors.RED_600), \
                                                                    on_click=self.reset_callback),  \
                                               col={"xs": 4, "sm": 2},                    \
                                               )
        ### ios风格按钮
        cupertino_actions       = [
                                    ft.CupertinoDialogAction(
                                        "是的",
                                        is_destructive_action=True,
                                        on_click=self.close_action_callback,
                                    ),
                                    ft.CupertinoDialogAction(
                                        text="否",
                                        is_default_action=False,
                                        on_click=self.close_action_callback,
                                    ),
                                    ]

        ### material风格按钮
        # self.material_actions = [
        #     ft.TextButton(text="Yes", on_click=self.handle_action_click,                \
        #                   style=ft.ButtonStyle(color=ft.Colors.RED_600)),
        #     ft.TextButton(text="No", on_click=self.handle_action_click),
        # ]

        ### 重置警告对话框
        self.dlg                = ft.CupertinoAlertDialog(
                                                        title=ft.Text("警告警告！"),
                                                        content=ft.Text("你确定要重置吗？"),
                                                        actions=cupertino_actions,
                                                        )
        
        # 使用网格布局实现横竖屏自适应支持
        head_info               = ft.ResponsiveRow([
                                        self.hand_num_now_tfiled, self.multi_power_now_tfiled, \
                                        add_button_text, self.add_buttom, start_buttom, self.reset_buttom
                                        ], vertical_alignment=ft.CrossAxisAlignment.END, spacing=0)
        
        # 玩家数据表格
        ## 表头显示
        sheet_head_index         = ft.TextField(value="序号",    disabled=True, height=self.d_height,   \
                                                text_size=self.d_text_size, col=2,\
                                                border=ft.InputBorder.NONE, text_align=ft.TextAlign.CENTER)
        sheet_head_name         = ft.TextField(value="玩家名称",    disabled=True, height=self.d_height,   \
                                                text_size=self.d_text_size, col=4,\
                                                border=ft.InputBorder.NONE, text_align=ft.TextAlign.CENTER)
        sheet_head_hand_num     = ft.TextField(value="手数",    disabled=True, height=self.d_height,   \
                                                text_size=self.d_text_size, col=3,
                                                border=ft.InputBorder.NONE, text_align=ft.TextAlign.CENTER)
        sheet_head_res_chip     = ft.TextField(value="剩余码量", disabled=True, height=self.d_height,   \
                                                text_size=self.d_text_size, col=3,
                                                border=ft.InputBorder.NONE, text_align=ft.TextAlign.CENTER)
        # sheet_head_surplus_chip = ft.TextField(value="结余码量", disabled=True, height=self.d_height,   \
        #                                         text_size=self.d_text_size, col=3,
        #                                         border=ft.InputBorder.NONE, text_align=ft.TextAlign.CENTER)
        # sheet_head_p_l          = ft.TextField(value="盈亏",    disabled=True, height=self.d_height,   \
        #                                         text_size=self.d_text_size, col=2,
        #                                         border=ft.InputBorder.NONE, text_align=ft.TextAlign.CENTER)
        sheet_head              = ft.ResponsiveRow([sheet_head_index, sheet_head_name, sheet_head_hand_num, sheet_head_res_chip, \
                                                    #sheet_head_surplus_chip, sheet_head_p_l
                                                    ], spacing=0)
        ## 玩家列表信息显示
        self.people_datasheet = ft.Column([], spacing=0)   # 原始数据
        self.people_list = ft.Column([], spacing=0)        # 用来显示的数据
        self.people_list_init()                 # 原始数据初始化
        
        ## 手数修改提示框
        hand_n_chan_actions       = [
                                    ft.CupertinoDialogAction(
                                        "-1",
                                        is_destructive_action=True,
                                        on_click=self.hand_num_sub,
                                    ),
                                    ft.CupertinoDialogAction(
                                        text="+1",
                                        is_default_action=False,
                                        on_click=self.hand_num_add,
                                    ),
                                    ]
        self.hand_num_chan_ale  = ft.CupertinoAlertDialog(
                                                        title=ft.Text("玩家"),
                                                        content=ft.Text("手数增加还是减少？"),
                                                        actions=hand_n_chan_actions,
                                                        )
        # 显示结果界面
        self.result_dlg         = ft.CupertinoAlertDialog(title=ft.Text("游戏结束"), content=ft.Column([], spacing=0))

        # 返回整个计数界面
        return ft.Column([head_info, sheet_head, self.people_list])

    def people_log_list_init(self):
        '''创建历史记录折叠面板，未初始化数据
        这里先把所有的数据给初始化，后面就不需要频繁创建，只需要把指定数据进行显示即可
        '''
        for i in range(self.player_num_upper):
            # 面板
            exp = ft.ExpansionPanel(
                bgcolor=ft.Colors.BLACK,
                header=ft.ListTile(title=ft.Text(f"玩家 {i}")),
            )
            # 面板展开控件
            exp.content = ft.ListTile(
                # title=ft.Text(f"20250409"),            # 标题
                subtitle=ft.Column([ 
                                #    ft.Text(f"在x时x分x秒 ++ 1"),
                                #    ft.Text(f"在x时x分x秒 -- 1"),
                                   ], spacing=0)
                # trailing=ft.IconButton(ft.Icons.DELETE, data=exp),
            )

            self.people_logbase.controls.append(exp)

    def history_page_init(self):
        # 当前所有选手信息记录
        self.people_logbase = ft.ExpansionPanelList(
            expand_icon_color=ft.Colors.YELLOW,
            elevation=2,
            divider_color=ft.Colors.YELLOW,
            # on_change=handle_change,
            controls=[
            ]
        )
        self.people_log_list = ft.ExpansionPanelList(
            expand_icon_color=ft.Colors.YELLOW,
            elevation=2,
            divider_color=ft.Colors.YELLOW,
            # on_change=handle_change,
            controls=[
            ]
        )
        self.people_log_list_init()
        
        return self.people_log_list
         
    def about_page_init(self):
        # logo
        logo_text               = ft.Text("小楠出品 V2.0.4")
        logo_text_cont          = ft.Container(
                                               content=logo_text,
                                               margin=5,
                                               padding=5,
                                               alignment=ft.alignment.center,
                                               bgcolor=ft.Colors.PURPLE_ACCENT_700,
                                               data=0,
                                               ink=True,
                                               col={"xs": 6, "sm": 3}
                                               )
        return logo_text_cont

if __name__ == "__main__":
    main_class = Main()
    ft.app(target=main_class.main)