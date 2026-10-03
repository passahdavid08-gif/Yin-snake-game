name = input("What is your name ??")
# Remove leading and trailing whitespace and capitalize 
name = name.strip().title()
# Get the first name only
first, last = name.split(" ")
print(f"Hello, {first}!")



x = float(input("Enter a first number x :"))
y = float(input("Enter a second number y :"))
z = round(x + y)
print(f"The sum of {x} and {y} is {z}")


# Conditionnal statements in Python are used to perform different actions based on different conditions. The most common conditional statements are `if`, `elif`, and `else`.
x = int(input("Enter a number: "))
y = int(input("Enter another number: "))
if x < y:
    print(f"{x} is less than {y}")
elif x > y :
    print(f"{x} is greater than {y}")
else:
    print(f"{x} is equal to {y}")   

# Conditionnal statements in Python are used to perform different actions based on different conditions. The most common conditional statements are `if`, `elif`, and `else`.
x = int(input("Enter a number: "))
y = int(input("Enter another number: "))
if x != y:
    print(f"{x} is not equal to {y}")       
else:
    print(f"{x} is equal to {y}")   


    # Grade 
score = int(input("Enter your score: "))
if score >= 90:
    print("Your grade is A")    
elif score >= 80:
    print("Your grade is B")
elif score >= 70:
    print("Your grade is C")
elif score >= 60:
    print("Your grade is D")
else:
    print("Your grade is F")    


# parity
def main():
    x = int(input("Enter a number: "))
    if is_even(x):
        print(f"{x} is an even number")
    else:
        print(f"{x} is an odd number")


# Bool expression :
def is_even(num):
    if num % 2 == 0:
        return True
    else:
        return False    


# main()
# is_even(5)


name = input("Enter your name: ")

match name:
    case "Alice":
        print("Hello, mink")
    case "Bob":
        print("Hello, gryffindor")
    case "Charlie":
        print("Hello, slytherin")
    case "David":
        print("Hello, hufflepuff")
    case _:
        print("Hello, who ?")