# -*- coding: utf-8 -*-
"""
足球运动员数据管理程序（Python 入门课）

功能菜单：
    1 添加球员      2 查看全部球员    3 按球队查询
    4 修改球员信息  5 删除球员        6 简单统计      0 退出程序

数据保存在运行程序时所在目录（一般就是脚本所在目录）的 players.json 里，
启动时自动读取，添加 / 修改 / 删除之后自动保存。

只用标准库 json，没有第三方库，也没有用类和装饰器，
数据用"列表 + 字典"保存：players 是列表，里面每个元素是一个球员字典。
"""

import json

# 数据文件名（存放在运行程序时所在的目录）
DATA_FILE = "players.json"

# 表格每一列的宽度（注意：一个汉字在屏幕上占 2 个字符宽度）
# 姓名一列宽 12，最多显示 6 个汉字；球队一列宽 14，最多 7 个汉字。
# 万一起过宽度，pad() 会截断显示，但程序里存的是完整内容。
W_NAME = 12
W_TEAM = 14
W_POS = 8
W_HEIGHT = 6
W_WEIGHT = 6
W_GOAL = 4
W_ASSIST = 4
W_APPEAR = 4

# 全局变量：所有球员都放在这个列表里，每个球员是一个字典
players = []


# ====================== 一、让表格对齐的小工具 ======================

def char_width(ch):
    """返回一个字符在屏幕上占的宽度：汉字算 2，英文数字算 1"""
    if ord(ch) > 127:
        return 2
    return 1


def text_width(text):
    """返回一整段文字的显示宽度"""
    width = 0
    for ch in text:
        width = width + char_width(ch)
    return width


def pad(text, width):
    """把文字补空格到指定宽度；文字太长就截断，保证表格不会歪"""
    text = str(text)
    if text_width(text) > width:
        # 太长：从头开始取字符，取到放不下为止
        result = ""
        used = 0
        for ch in text:
            if used + char_width(ch) > width:
                break
            result = result + ch
            used = used + char_width(ch)
        return result
    # 不够长：在后面补空格
    return text + " " * (width - text_width(text))


def make_border():
    """生成表格的横线"""
    line = "+"
    for width in [W_NAME, W_TEAM, W_POS, W_HEIGHT, W_WEIGHT, W_GOAL, W_ASSIST, W_APPEAR]:
        line = line + "-" * (width + 2) + "+"
    return line


def make_row(name, team, position, height, weight, goal, assist, appear):
    """生成表格的一行，每个格子左右各留一个空格"""
    row = "| " + pad(name, W_NAME)
    row = row + " | " + pad(team, W_TEAM)
    row = row + " | " + pad(position, W_POS)
    row = row + " | " + pad(height, W_HEIGHT)
    row = row + " | " + pad(weight, W_WEIGHT)
    row = row + " | " + pad(goal, W_GOAL)
    row = row + " | " + pad(assist, W_ASSIST)
    row = row + " | " + pad(appear, W_APPEAR) + " |"
    return row


def print_player_table(player_list):
    """把一组球员打印成整齐的表格"""
    if len(player_list) == 0:
        print("（没有可显示的球员）")
        return

    border = make_border()
    print(border)
    print(make_row("姓名", "球队", "位置", "身高cm", "体重kg", "进球", "助攻", "出场"))
    print(border)
    for player in player_list:
        print(make_row(
            player["姓名"],
            player["球队"],
            player["位置"],
            "{:.1f}".format(player["身高"]),
            "{:.1f}".format(player["体重"]),
            str(player["进球数"]),
            str(player["助攻数"]),
            str(player["出场次数"])
        ))
    print(border)


# ====================== 二、输入与校验（保证程序不会崩） ======================

def input_text(tip, default=None):
    """读取一段文字。给了 default 时，直接回车就用默认值"""
    while True:
        text = input(tip).strip()
        if text == "":
            if default is None:
                print("  这一项不能为空，请重新输入。")
                continue
            return default
        return text


def input_positive_float(tip, default=None):
    """读取正数（身高、体重），输错就提示并重新输入"""
    while True:
        text = input(tip).strip()
        if text == "" and default is not None:
            return default
        try:
            value = float(text)
        except ValueError:
            print("  这里要输入数字，例如 178 或 72.5，请重新输入。")
            continue
        # 必须大于 0，等于 0 或者是负数都不行
        if not (value > 0):
            print("  必须大于 0，请重新输入。")
            continue
        return round(value, 1)


def input_non_negative_int(tip, default=None):
    """读取非负整数（进球数、助攻数、出场次数），输错就提示并重新输入"""
    while True:
        text = input(tip).strip()
        if text == "" and default is not None:
            return default
        try:
            value = int(text)
        except ValueError:
            print("  这里要输入整数，例如 0 或 12，请重新输入。")
            continue
        if value < 0:
            print("  不能是负数，请重新输入。")
            continue
        return value


# ====================== 三、查找球员的小函数 ======================

def find_index(name):
    """查找球员在列表中的下标，找不到返回 -1"""
    i = 0
    while i < len(players):
        if players[i]["姓名"] == name:
            return i
        i = i + 1
    return -1


def find_player(name):
    """按姓名找到球员字典，找不到返回 None"""
    index = find_index(name)
    if index == -1:
        return None
    return players[index]


# ====================== 四、文件的保存与加载 ======================

def save_players():
    """把整个 players 列表写进 players.json"""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            # ensure_ascii=False：让中文原样写进文件，不变成 \uXXXX
            json.dump(players, f, ensure_ascii=False, indent=4)
        return True
    except OSError as error:
        print("保存数据失败：" + str(error))
        return False


def load_players():
    """从 players.json 读取球员列表；文件不存在就从空列表开始"""
    try:
        # 用 utf-8-sig 读：如果文件是记事本保存的（带 BOM 头），也能正常读出来
        with open(DATA_FILE, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("没有找到 " + DATA_FILE + "，本次从空数据开始。")
        return []
    except (OSError, ValueError) as error:
        print("读取 " + DATA_FILE + " 失败（" + str(error) + "），本次从空数据开始。")
        return []

    # 文件里的内容不一定是正常的列表，这里检查一下，格式不对的条目就跳过
    if not isinstance(data, list):
        print(DATA_FILE + " 的内容格式不对，本次从空数据开始。")
        return []

    result = []
    skip = 0
    for item in data:
        if not isinstance(item, dict):
            skip = skip + 1
            continue
        try:
            name = str(item["姓名"]).strip()
            team = str(item["球队"]).strip()
            position = str(item["位置"]).strip()
            height = float(item["身高"])
            weight = float(item["体重"])
            goals = int(item["进球数"])
            assists = int(item["助攻数"])
            appears = int(item["出场次数"])
        except (KeyError, TypeError, ValueError):
            # 缺字段或者字段不是数字，这条数据就不要了
            skip = skip + 1
            continue
        if name == "":
            skip = skip + 1
            continue
        one_player = {
            "姓名": name,
            "球队": team,
            "位置": position,
            "身高": height,
            "体重": weight,
            "进球数": goals,
            "助攻数": assists,
            "出场次数": appears,
        }
        result.append(one_player)

    if skip > 0:
        print("提示：" + DATA_FILE + " 里有 " + str(skip) + " 条数据格式不对，已跳过。")
    return result


# ====================== 五、1 添加球员 ======================

def add_player():
    print("\n--- 添加球员 ---")
    name = input_text("姓名: ")
    # 姓名用来区分球员，所以不允许重名
    while find_player(name) is not None:
        print("  已经有同名的球员了，请换一个姓名。")
        name = input_text("姓名: ")

    team = input_text("球队: ")
    position = input_text("位置（如 前锋/中场/后卫/门将）: ")
    height = input_positive_float("身高(cm): ")
    weight = input_positive_float("体重(kg): ")
    goals = input_non_negative_int("进球数: ")
    assists = input_non_negative_int("助攻数: ")
    appears = input_non_negative_int("出场次数: ")

    # 一名球员的信息用一个字典保存
    one_player = {
        "姓名": name,
        "球队": team,
        "位置": position,
        "身高": height,
        "体重": weight,
        "进球数": goals,
        "助攻数": assists,
        "出场次数": appears,
    }
    players.append(one_player)   # 再把字典放进列表
    save_players()
    print("添加成功！现在共有 " + str(len(players)) + " 名球员。")


# ====================== 六、2 查看全部球员 ======================

def show_all_players():
    print("\n--- 全部球员 ---")
    if len(players) == 0:
        print("现在还没有球员，请先用“1 添加球员”录入数据。")
        return
    print_player_table(players)
    print("共 " + str(len(players)) + " 名球员。")


# ====================== 七、3 按球队查询 ======================

def query_by_team():
    print("\n--- 按球队查询 ---")
    if len(players) == 0:
        print("现在还没有球员，没有可以查询的数据。")
        return

    team = input_text("请输入球队名称: ")
    result = []
    for player in players:
        if player["球队"] == team:
            result.append(player)   # 把同一支球队的球员收集起来

    if len(result) == 0:
        print("没有找到球队“" + team + "”的球员。")
        return
    print("球队“" + team + "”共有 " + str(len(result)) + " 名球员：")
    print_player_table(result)


# ====================== 八、4 修改球员信息 ======================

def modify_player():
    print("\n--- 修改球员信息 ---")
    if len(players) == 0:
        print("现在还没有球员，请先添加。")
        return

    name = input_text("请输入要修改的球员姓名: ")
    player = find_player(name)
    if player is None:
        print("没有找到名叫“" + name + "”的球员。")
        return

    print("这名球员现在的信息：")
    print_player_table([player])
    print("提示：每一项都直接按回车，就表示这一项不修改。")

    # 改姓名时要检查是否和其他球员重名
    new_name = input_text("姓名（回车不修改）: ", player["姓名"])
    while new_name != player["姓名"] and find_player(new_name) is not None:
        print("  已经有同名的球员了，请换一个姓名。")
        new_name = input_text("姓名（回车不修改）: ", player["姓名"])
    player["姓名"] = new_name

    player["球队"] = input_text("球队（回车不修改）: ", player["球队"])
    player["位置"] = input_text("位置（回车不修改）: ", player["位置"])
    player["身高"] = input_positive_float("身高(cm)（回车不修改）: ", player["身高"])
    player["体重"] = input_positive_float("体重(kg)（回车不修改）: ", player["体重"])
    player["进球数"] = input_non_negative_int("进球数（回车不修改）: ", player["进球数"])
    player["助攻数"] = input_non_negative_int("助攻数（回车不修改）: ", player["助攻数"])
    player["出场次数"] = input_non_negative_int("出场次数（回车不修改）: ", player["出场次数"])

    save_players()
    print("修改成功！修改后的信息：")
    print_player_table([player])


# ====================== 九、5 删除球员 ======================

def delete_player():
    print("\n--- 删除球员 ---")
    if len(players) == 0:
        print("现在还没有球员，没有可以删除的数据。")
        return

    name = input_text("请输入要删除的球员姓名: ")
    index = find_index(name)
    if index == -1:
        print("没有找到名叫“" + name + "”的球员。")
        return

    print("准备删除这名球员：")
    print_player_table([players[index]])

    answer = input("确定要删除吗？输入 y 确认，输入其他内容取消: ").strip().lower()
    if answer != "y":
        print("已取消删除。")
        return

    players.pop(index)   # 从列表里删掉这个字典
    save_players()
    print("删除成功！现在共有 " + str(len(players)) + " 名球员。")


# ====================== 十、6 简单统计 ======================

def show_statistics():
    print("\n--- 简单统计 ---")
    if len(players) == 0:
        print("现在还没有球员，无法统计。")
        return

    total_goals = 0
    total_height = 0.0
    total_weight = 0.0
    for player in players:
        total_goals = total_goals + player["进球数"]
        total_height = total_height + player["身高"]
        total_weight = total_weight + player["体重"]

    count = len(players)
    print("球员总数：" + str(count) + " 人")
    print("总进球数：" + str(total_goals) + " 个")
    print("平均身高：{:.1f} cm".format(total_height / count))
    print("平均体重：{:.1f} kg".format(total_weight / count))


# ====================== 十一、菜单与主程序 ======================

def show_menu():
    """打印菜单"""
    print()
    print("=" * 44)
    print("      足球运动员数据管理程序")
    print("=" * 44)
    print("  1. 添加球员")
    print("  2. 查看全部球员")
    print("  3. 按球队查询")
    print("  4. 修改球员信息")
    print("  5. 删除球员")
    print("  6. 简单统计")
    print("  0. 退出程序")
    print("=" * 44)


def main():
    """程序入口：先加载数据，再循环显示菜单、处理用户的选择"""
    global players
    players = load_players()
    print("欢迎使用足球运动员数据管理程序！")
    print("当前已加载 " + str(len(players)) + " 名球员。")

    running = True
    while running:
        show_menu()
        choice = input("请输入功能编号(0-6): ").strip()

        if choice == "1":
            add_player()
        elif choice == "2":
            show_all_players()
        elif choice == "3":
            query_by_team()
        elif choice == "4":
            modify_player()
        elif choice == "5":
            delete_player()
        elif choice == "6":
            show_statistics()
        elif choice == "0":
            save_players()
            print("数据已保存到 " + DATA_FILE + "，程序结束，再见！")
            running = False
        else:
            print("没有这个编号，请输入 0 到 6 之间的数字。")


# 直接运行本文件时才执行 main()
if __name__ == "__main__":
    main()