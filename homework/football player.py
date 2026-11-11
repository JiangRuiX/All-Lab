"""
足球运动员数据管理系统 —— Team Project 参考实现（目标：约 80 分 / Excellent 档）

对照作业评分表（Grading Rubric）：
  Features (40%)      删除 / 查找（并含新增、修改、查看、统计）
  Persistence (30%)   多个对象 + 列表管理（不做文件读写，那属于 Outstanding 档）
  UX (10%)            循环菜单 + 菜单输入校验
  DX (10%)            用户输入校验 + 数据类自检
  Git (10%)           需自行 git commit 并打 tag（代码之外，见交付说明）

只使用本学期讲过的内容：类与对象、列表、字典、循环、分支、函数、输入校验。
不使用第三方库，不使用文件读写。函数按课件《Parameters & Return Values》的要求设计：
「查数据 / 算统计」的函数用参数接收数据、用 return 交出结果；
「读输入 / 打印结果」的函数专门负责交互，两者不混在一起。

【本文件为无注释提交版】代码与逐行注释讲解版完全一致。
"""


class Player:
    """一名足球运动员。球衣号码是唯一编号，不允许重复。"""

    def __init__(self, name, number, position, age, goals, assists):
        self.name = name
        self.number = number
        self.position = position
        self.age = age
        self.goals = goals
        self.assists = assists

    def is_valid(self):
        """数据类校验：字段不合法就提前返回 False（链式提前返回写法）。"""
        if self.name == "" or self.position == "":
            return False
        if self.number < 1 or self.number > 99:
            return False
        if self.age < 15 or self.age > 50:
            return False
        if self.goals < 0 or self.assists < 0:
            return False
        return True

    def __str__(self):
        """查看单个球员详情时，print(球员对象) 会自动调用这个方法。"""
        return (f"  姓名：{self.name}\n"
                f"  球衣号码：{self.number}\n"
                f"  位置：{self.position}\n"
                f"  年龄：{self.age} 岁\n"
                f"  进球数：{self.goals}\n"
                f"  助攻数：{self.assists}")

    def to_row(self):
        """把一名球员转成表格中的一行文字。"""
        return (pad(self.number, 8) + pad(self.name, 12) + pad(self.position, 10) +
                pad(self.age, 8) + pad(self.goals, 8) + pad(self.assists, 8))


def pad(text, width):
    """把内容补到指定显示宽度：中文算 2 格、英文数字算 1 格，表格才不会歪。"""
    size = 0
    for ch in str(text):
        if ord(ch) > 127:
            size += 2
        else:
            size += 1
    return str(text) + " " * max(0, width - size)


def find_index_by_number(players, number):
    """按球衣号码查找，返回它在列表中的下标；找不到返回 -1。"""
    for i in range(len(players)):
        if players[i].number == number:
            return i
    return -1


def find_by_name(players, name):
    """按姓名精确查找，返回符合条件的球员列表。"""
    result = []
    for p in players:
        if p.name == name:
            result.append(p)
    return result


def find_by_position(players, position):
    """按位置查找，返回符合条件的球员列表。"""
    result = []
    for p in players:
        if p.position == position:
            result.append(p)
    return result


def total_goals(players):
    """计算全队总进球数。"""
    total = 0
    for p in players:
        total += p.goals
    return total


def top_scorer(players):
    """找出进球最多的球员；列表为空时返回 None。"""
    if len(players) == 0:
        return None
    best = players[0]
    for p in players:
        if p.goals > best.goals:
            best = p
    return best


def count_by_position(players):
    """用字典统计每个位置有多少人。"""
    counts = {}
    for p in players:
        if p.position in counts:
            counts[p.position] += 1
        else:
            counts[p.position] = 1
    return counts


def read_int(prompt, low, high, default=None):
    """读取 [low, high] 范围内的整数。传了 default 时，直接回车表示保留原值。"""
    while True:
        text = input(prompt + " ").strip()
        if text == "" and default is not None:
            return default
        try:
            value = int(text)
        except ValueError:
            print("输入错误：请输入一个整数！")
            continue
        if low <= value <= high:
            return value
        print(f"输入错误：请输入 {low} 到 {high} 之间的整数！")


def read_text(prompt, default=None):
    """读取非空字符串。传了 default 时，直接回车表示保留原值。"""
    while True:
        text = input(prompt + " ").strip()
        if text == "" and default is not None:
            return default
        if text != "":
            return text
        print("输入错误：内容不能为空！")


def read_yes_no(prompt):
    """读取 y / n，返回 True 或 False。"""
    while True:
        answer = input(prompt + " ").strip().lower()
        if answer == "y":
            return True
        if answer == "n":
            return False
        print("输入错误：请输入 y 或 n！")


def print_table(players):
    """把球员列表打印成表格，供「显示全部」和「查找结果」复用。"""
    print(pad("号码", 8) + pad("姓名", 12) + pad("位置", 10) +
          pad("年龄", 8) + pad("进球", 8) + pad("助攻", 8))
    print("-" * 54)
    for p in players:
        print(p.to_row())


def show_menu():
    """打印功能菜单。"""
    print("\n========== 足球运动员数据管理系统 ==========")
    print("  1. 添加球员")
    print("  2. 显示全部球员")
    print("  3. 查看球员详情（按球衣号码）")
    print("  4. 修改球员信息（按球衣号码）")
    print("  5. 删除球员（按球衣号码）")
    print("  6. 查找球员（号码 / 姓名 / 位置）")
    print("  7. 数据统计")
    print("  0. 退出程序")
    print("=============================================")


def add_player(players):
    """新增一名球员；球衣号码重复时拒绝添加。"""
    print("\n===== 添加球员 =====")
    number = read_int("球衣号码(1-99)：", 1, 99)
    if find_index_by_number(players, number) != -1:
        print("添加失败：该球衣号码已存在，请换一个！")
        return

    name = read_text("姓名：")
    position = read_text("位置（前锋/中场/后卫/门将）：")
    age = read_int("年龄(15-50)：", 15, 50)
    goals = read_int("进球数(0-999)：", 0, 999)
    assists = read_int("助攻数(0-999)：", 0, 999)

    player = Player(name, number, position, age, goals, assists)
    if not player.is_valid():
        print("添加失败：球员数据不合法，请重新输入！")
        return
    players.append(player)
    print(f"已添加球员：{name}（{number} 号）")


def show_all(players):
    """显示全部球员。"""
    print("\n===== 全部球员 =====")
    if len(players) == 0:
        print("暂无球员数据，请先添加。")
        return
    print_table(players)
    print(f"共 {len(players)} 名球员。")


def show_detail(players):
    """按球衣号码查看某一球员的完整信息。"""
    print("\n===== 查看球员详情 =====")
    if len(players) == 0:
        print("暂无球员数据。")
        return
    number = read_int("请输入球衣号码(1-99)：", 1, 99)
    index = find_index_by_number(players, number)
    if index == -1:
        print("没有找到该球衣号码的球员。")
        return
    print(players[index])


def edit_player(players):
    """按球衣号码修改球员信息；直接回车可保留原值。"""
    print("\n===== 修改球员信息 =====")
    if len(players) == 0:
        print("暂无球员数据。")
        return
    number = read_int("请输入要修改的球衣号码(1-99)：", 1, 99)
    index = find_index_by_number(players, number)
    if index == -1:
        print("没有找到该球衣号码的球员。")
        return

    p = players[index]
    print(players[index])
    print("（直接回车 = 保留原值；球衣号码是唯一编号，不能修改）")
    p.name = read_text(f"姓名（当前 {p.name}）：", p.name)
    p.position = read_text(f"位置（当前 {p.position}）：", p.position)
    p.age = read_int(f"年龄(15-50，当前 {p.age})：", 15, 50, p.age)
    p.goals = read_int(f"进球数(0-999，当前 {p.goals})：", 0, 999, p.goals)
    p.assists = read_int(f"助攻数(0-999，当前 {p.assists})：", 0, 999, p.assists)

    if not p.is_valid():
        print("修改失败：数据不合法！")
        return
    print("球员信息已更新。")


def delete_player(players):
    """按球衣号码删除球员，删除前必须二次确认。"""
    print("\n===== 删除球员 =====")
    if len(players) == 0:
        print("暂无球员数据。")
        return
    number = read_int("请输入要删除的球衣号码(1-99)：", 1, 99)
    index = find_index_by_number(players, number)
    if index == -1:
        print("没有找到该球衣号码的球员。")
        return

    p = players[index]
    if read_yes_no(f"确定删除 {p.name}（{number} 号）吗？(y/n)："):
        players.pop(index)
        print(f"已删除球员：{p.name}")
    else:
        print("已取消删除。")


def search_player(players):
    """查找球员：按号码精确查找、按姓名精确查找、按位置查找。"""
    print("\n===== 查找球员 =====")
    if len(players) == 0:
        print("暂无球员数据。")
        return
    print("  1. 按球衣号码")
    print("  2. 按姓名（精确匹配）")
    print("  3. 按位置")
    choice = read_int("请选择查找方式(1-3)：", 1, 3)

    found = []
    if choice == 1:
        number = read_int("请输入球衣号码(1-99)：", 1, 99)
        index = find_index_by_number(players, number)
        if index != -1:
            found.append(players[index])
    elif choice == 2:
        found = find_by_name(players, read_text("请输入姓名："))
    else:
        found = find_by_position(players, read_text("请输入位置："))

    if len(found) == 0:
        print("没有找到符合条件的球员。")
        return
    print(f"共找到 {len(found)} 名球员：")
    print_table(found)


def show_statistics(players):
    """显示汇总信息：人数、总进球、总助攻、平均年龄、最佳射手、各位置人数。"""
    print("\n===== 数据统计 =====")
    if len(players) == 0:
        print("暂无球员数据，无法统计。")
        return

    total_age = 0
    total_assists = 0
    for p in players:
        total_age += p.age
        total_assists += p.assists

    best = top_scorer(players)
    print(f"球员人数：{len(players)} 人")
    print(f"总进球数：{total_goals(players)}")
    print(f"总助攻数：{total_assists}")
    print(f"平均年龄：{total_age / len(players):.1f} 岁")
    print(f"最佳射手：{best.name}（{best.goals} 球）")

    print("各位置人数：")
    counts = count_by_position(players)
    for position in counts:
        print(f"  {position}：{counts[position]} 人")


def main():
    """程序入口：准备示例数据 → 反复显示菜单 → 按编号调用对应功能。"""
    players = [
        Player("张伟", 10, "前锋", 22, 18, 6),
        Player("李强", 7, "中场", 24, 5, 12),
        Player("王磊", 1, "门将", 26, 0, 1),
    ]
    print("欢迎使用足球运动员数据管理系统！（已预置 3 名示例球员）")

    while True:
        show_menu()
        choice = read_int("请输入功能编号：", 0, 7)

        if choice == 0:
            print("感谢使用，再见！")
            break
        elif choice == 1:
            add_player(players)
        elif choice == 2:
            show_all(players)
        elif choice == 3:
            show_detail(players)
        elif choice == 4:
            edit_player(players)
        elif choice == 5:
            delete_player(players)
        elif choice == 6:
            search_player(players)
        elif choice == 7:
            show_statistics(players)


if __name__ == "__main__":
    main()
