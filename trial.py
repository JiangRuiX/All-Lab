def player_name():
    name=input('Please enter player name:')
    return name
def player_age():
    age=input('Please enter player age:')
    return age
def player_height():
    height=input('Please enter player height:')
    return height
def player_weight():
    weight=input('Please enter player weight:')
    return weight
def line_drawer():
    print('-'*30)
def print_result(name,age,height,weight):
    line_drawer()
    print(f'Name:{Name}')
    line_drawer()
    print(f'Age:{Age}')
    line_drawer()
    print(f'Height:{Height}')
    line_drawer()
    print(f'Weight:{Weight}')
Name=player_name()
Age=player_age()
Height=player_height()
Weight=player_weight()
print_result(Name,Age,Height,Weight)