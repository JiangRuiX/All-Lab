def print_menu():
    print("1. Say hello")
    print("2. Add two numbers")
    print("3. Print a message")
    print("4. Exit")
    print("5. Square")


def say_hello():
    print("Hello")


def add_two_numbers():
    num1 = int(input("Enter first number: "))
    num2 = int(input("Enter second number: "))
    print("Total:", num1 + num2)


def print_message():
    print("Python is fun")


def square():
    a=int(input("Enter a number: "))
    result=a*a
    print("Result:", result)


choice = ""

while choice != "4":
    print_menu()
    choice = input("Enter your choice: ")

    if choice == "1":
        say_hello()
    elif choice == "2":
        add_two_numbers()
    elif choice == "3":
        print_message()
    elif choice == "4":
        print("Goodbye")
    elif choice == "5":
        square()
    else:
        print("Invalid choice")
