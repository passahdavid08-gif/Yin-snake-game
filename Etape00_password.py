import random 

lower = "abcdefghijklmnopqrstuvwxyz"
upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
numbers = "0123456789"
symbols = "[]{}()*;/,_-"

all_characters = lower + upper + numbers + symbols
length = int(input("Enter the length of the password: "))

password = "".join(random.choice(all_characters) for _ in range(length))
print(password)
