def add(a,b):
    return a+b
def subtract(a,b):
    return a-b
def multiply(a,b):
    return a*b
def divide(a,b):
    if b ==0:
        return None
    return a/b
def show_all(a,b):
    print(add(a,b))
    print(subtract(a,b))
    print(multiply(a,b))
    print(divide(a,b))
a=float(input('Enter a number: '))
b=float(input('Enter another number: '))
show_all(a,b)

