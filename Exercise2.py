def bmi(weight_kg,height_m):
    return weight_kg/(height_m**2)
BMI=bmi(float(input('enter your weight in kg:')),float(input('enter your height in meter:')))
print(BMI)
if BMI<18.5:
    print('underweight')
elif 18.5<BMI<24.9:
    print('normal')
elif 25<BMI<29.9:
    print('overweight')
else:
    print('obese')