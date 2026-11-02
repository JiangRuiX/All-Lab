def print_stars():
    print('*'*20)
def print_dashes():
    print('-'*20)
def print_banner(title):
    print_stars()
    print(f'{title:^20}')
    print_stars()
title=input('enter the title:')
print_banner(title)