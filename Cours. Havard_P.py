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



