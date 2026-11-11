# -*- coding: utf-8 -*-
"""
足球运动员数据管理程序
适合大一 Python 入门课程使用
只使用标准库（json），用"列表 + 字典"保存数据
"""

import json
import os

# 数据文件名（和程序放在同一个文件夹里）
DATA_FILE = "players.json"


# ---------------- 数据的加载与保存 ----------------

def load_players():
    """程序启动时从 players.json 读取数据。
    如果文件不存在或内容有问题，就返回空列表，从零开始。"""
    if not os.path.exists(DATA_FILE):
        return []  # 第一次运行，还没有数据文件
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        else:
            return []
    except (json.JSONDecodeError, OSError):
        print("提示：数据文件读取失败，将使用空数据开始。")
        return []


def save_players(players):
    """把数据保存到 players.json 文件中。"""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(players, f, ensure_ascii=False, indent=2)
    except OSError:
        print("提示：数据保存失败，请检查磁盘或文件权限。")


# ---------------- 输入校验 ----------------

def input_positive_number(prompt):
    """让用户输入一个正数（用于身高、体重）。
    输入不合法时提示并要求重新输入，直到正确为止。"""
    while True:
        text = input(prompt).strip()
        try:
            value = float(text)
        except ValueError:
            print("输入错误：请输入一个数字！")
            continue
        if value <= 0:
            print("输入错误：数值必须大于 0！")
            continue
        return value


def input_nonnegative_int(prompt):
    """让用户输入一个非负整数（用于进球、助攻、出场次数）。
    输入不合法时提示并要求重新输入。"""
    while True:
        text = input(prompt).strip()
        try:
            value = int(text)
        except ValueError:
            print("输入错误：请输入一个整数！")
            continue
        if value < 0:
            print("输入错误：数值不能是负数！")
            continue
        return value


def input_not_empty(prompt):
    """让用户输入一个非空字符串（用于姓名、球队等）。
    输入为空时提示并要求重新输入。"""
    while True:
        text = input(prompt).strip()
        if text == "":
            print("输入错误：内容不能为空！")
        else:
            return text


# ---------------- 功能 1：添加球员 ----------------

def add_player(players):
    """依次输入各项信息，添加一名球员。"""
    print("\n===== 添加球员 =====")
    name = input_not_empty("请输入姓名：")
    team = input_not_empty("请输入球队：")
    position = input_not_empty("请输入位置（如 前锋/中场/后卫/门将）：")
    height = input_positive_number("请输入身高(cm)：")
    weight = input_positive_number("请输入体重(kg)：")
    goals = input_nonnegative_int("请输入进球数：")
    assists = input_nonnegative_int("请输入助攻数：")
    games = input_nonnegative_int("请输入出场次数：")

    player = {
        "姓名": name,
        "球队": team,
        "位置": position,
        "身高": height,
        "体重": weight,
        "进球数": goals,
        "助攻数": assists,
        "出场次数": games,
    }
    players.append(player)
    save_players(players)  # 添加后立即保存
    print("已成功添加球员：" + name)


# ---------------- 功能 2：查看全部球员 ----------------

def show_all_players(players):
    """用对齐的表格显示所有球员信息。"""
    print("\n===== 全部球员 =====")
    if len(players) == 0:
        print("暂无球员数据。")
        return

    # 表头（每列固定宽度，用 format 对齐）
    header = "{:<4}{:<10}{:<12}{:<8}{:>8}{:>8}{:>8}{:>8}{:>8}".format(
        "序号", "姓名", "球队", "位置", "身高", "体重", "进球", "助攻", "出场")
    print(header)
    print("-" * len(header))

    for i in range(len(players)):
        p = players[i]
        line = "{:<6}{:<10}{:<14}{:<8}{:>6.1f}{:>8.1f}{:>8}{:>8}{:>8}".format(
            i + 1,
            p["姓名"],
            p["球队"],
            p["位置"],
            p["身高"],
            p["体重"],
            p["进球数"],
            p["助攻数"],
            p["出场次数"])
        print(line)


# ---------------- 功能 3：按球队查询 ----------------

def search_by_team(players):
    """输入球队名称，显示该球队的所有球员。"""
    print("\n===== 按球队查询 =====")
    if len(players) == 0:
        print("暂无球员数据。")
        return

    team = input_not_empty("请输入要查询的球队名称：")
    found = []  # 保存符合条件的球员
    for p in players:
        if p["球队"] == team:
            found.append(p)

    if len(found) == 0:
        print("没有找到球队【" + team + "】的球员。")
    else:
        print("球队【" + team + "】共有 " + str(len(found)) + " 名球员：")
        header = "{:<10}{:<8}{:>8}{:>8}{:>8}{:>8}{:>8}".format(
            "姓名", "位置", "身高", "体重", "进球", "助攻", "出场")
        print(header)
        print("-" * len(header))
        for p in found:
            line = "{:<10}{:<8}{:>8.1f}{:>8.1f}{:>8}{:>8}{:>8}".format(
                p["姓名"], p["位置"], p["身高"], p["体重"],
                p["进球数"], p["助攻数"], p["出场次数"])
            print(line)


# ---------------- 功能 4：修改球员信息 ----------------

def modify_player(players):
    """按姓名查找球员，然后逐项确认是否修改。"""
    print("\n===== 修改球员信息 =====")
    if len(players) == 0:
        print("暂无球员数据。")
        return

    name = input_not_empty("请输入要修改的球员姓名：")
    target = None  # 记录找到的球员
    for p in players:
        if p["姓名"] == name:
            target = p
            break

    if target is None:
        print("没有找到名为【" + name + "】的球员。")
        return

    print("已找到球员，当前信息：")
    print("  球队：" + target["球队"])
    print("  位置：" + target["位置"])
    print("  身高：" + str(target["身高"]) + " cm")
    print("  体重：" + str(target["体重"]) + " kg")
    print("  进球数：" + str(target["进球数"]))
    print("  助攻数：" + str(target["助攻数"]))
    print("  出场次数：" + str(target["出场次数"]))
    print("（直接按回车表示不修改该项）")

    # 每一项都可以选择跳过（回车 = 不修改）
    text = input("请输入新的球队：").strip()
    if text != "":
        target["球队"] = text

    text = input("请输入新的位置：").strip()
    if text != "":
        target["位置"] = text

    text = input("请输入新的身高(cm)：").strip()
    if text != "":
        while True:  # 反复提示直到输入正确
            try:
                value = float(text)
                if value > 0:
                    target["身高"] = value
                    break
                else:
                    print("输入错误：身高必须大于 0！")
            except ValueError:
                print("输入错误：请输入一个数字！")
            text = input("请重新输入身高(cm)：").strip()

    text = input("请输入新的体重(kg)：").strip()
    if text != "":
        while True:
            try:
                value = float(text)
                if value > 0:
                    target["体重"] = value
                    break
                else:
                    print("输入错误：体重必须大于 0！")
            except ValueError:
                print("输入错误：请输入一个数字！")
            text = input("请重新输入体重(kg)：").strip()

    text = input("请输入新的进球数：").strip()
    if text != "":
        while True:
            try:
                value = int(text)
                if value >= 0:
                    target["进球数"] = value
                    break
                else:
                    print("输入错误：进球数不能是负数！")
            except ValueError:
                print("输入错误：请输入一个整数！")
            text = input("请重新输入进球数：").strip()

    text = input("请输入新的助攻数：").strip()
    if text != "":
        while True:
            try:
                value = int(text)
                if value >= 0:
                    target["助攻数"] = value
                    break
                else:
                    print("输入错误：助攻数不能是负数！")
            except ValueError:
                print("输入错误：请输入一个整数！")
            text = input("请重新输入助攻数：").strip()

    text = input("请输入新的出场次数：").strip()
    if text != "":
        while True:
            try:
                value = int(text)
                if value >= 0:
                    target["出场次数"] = value
                    break
                else:
                    print("输入错误：出场次数不能是负数！")
            except ValueError:
                print("输入错误：请输入一个整数！")
            text = input("请重新输入出场次数：").strip()

    save_players(players)  # 修改后立即保存
    print("球员信息已更新并保存。")


# ---------------- 功能 5：删除球员 ----------------

def delete_player(players):
    """按姓名删除球员，删除前先让用户确认。"""
    print("\n===== 删除球员 =====")
    if len(players) == 0:
        print("暂无球员数据。")
        return

    name = input_not_empty("请输入要删除的球员姓名：")
    index = -1  # 记录找到的位置
    for i in range(len(players)):
        if players[i]["姓名"] == name:
            index = i
            break

    if index == -1:
        print("没有找到名为【" + name + "】的球员。")
        return

    # 删除前确认，防止误删
    answer = input("确定要删除球员【" + name + "】吗？(y/n)：").strip().lower()
    if answer == "y":
        players.pop(index)
        save_players(players)
        print("已删除球员：" + name)
    else:
        print("已取消删除。")


# ---------------- 功能 6：简单统计 ----------------

def show_statistics(players):
    """计算并显示总进球数、平均身高、平均体重。"""
    print("\n===== 简单统计 =====")
    if len(players) == 0:
        print("暂无球员数据，无法统计。")
        return

    total_goals = 0    # 总进球数
    total_height = 0.0  # 身高总和
    total_weight = 0.0  # 体重总和

    for p in players:
        total_goals = total_goals + p["进球数"]
        total_height = total_height + p["身高"]
        total_weight = total_weight + p["体重"]

    count = len(players)
    print("球员总人数：" + str(count) + " 人")
    print("总进球数：" + str(total_goals))
    print("平均身高：" + format(total_height / count, ".1f") + " cm")
    print("平均体重：" + format(total_weight / count, ".1f") + " kg")


# ---------------- 菜单与主程序 ----------------

def show_menu():
    """显示功能菜单。"""
    print("\n========== 足球运动员数据管理系统 ==========")
    print("  1. 添加球员")
    print("  2. 查看全部球员")
    print("  3. 按球队查询")
    print("  4. 修改球员信息")
    print("  5. 删除球员")
    print("  6. 简单统计（总进球数、平均身高、平均体重）")
    print("  0. 退出程序")
    print("=============================================")


def main():
    """主函数：加载数据，循环显示菜单，根据选择调用对应功能。"""
    players = load_players()  # 启动时自动加载数据
    if len(players) > 0:
        print("已从 players.json 加载 " + str(len(players)) + " 名球员数据。")
    else:
        print("未找到已有数据，从空数据开始。")

    while True:
        show_menu()
        choice = input("请输入功能编号：").strip()

        if choice == "1":
            add_player(players)
        elif choice == "2":
            show_all_players(players)
        elif choice == "3":
            search_by_team(players)
        elif choice == "4":
            modify_player(players)
        elif choice == "5":
            delete_player(players)
        elif choice == "6":
            show_statistics(players)
        elif choice == "0":
            save_players(players)  # 退出前再保存一次，保证数据不丢
            print("数据已保存，感谢使用，再见！")
            break
        else:
            print("输入错误：请输入 0-6 之间的功能编号！")


# 只有直接运行本文件时才执行 main()
if __name__ == "__main__":
    main()
1