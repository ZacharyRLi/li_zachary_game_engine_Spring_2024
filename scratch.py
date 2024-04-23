# This file was created by: Zachary Li

# Write a function that takes two arguments and multiplies them together
# Use a return statement
# Print
def function(a, b):
    return a * b
def change(x):
    y = str(x)
    print("My number is: " + y)
i = 0
while i < 10:
    change(function(5, 10))
    i += 1
    print(i)