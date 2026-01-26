
name_no_hint = "Alice"
age_no_hint = 25

# With type hints (recommended for complex code)
name_with_hint: str = "Alice"
age_with_hint: int = 25














# Output using print
print(f"No hints - Name: {name_no_hint}, Age: {age_no_hint}")
print(f"With hints - Name: {name_with_hint}, Age: {age_with_hint}")

# Lists: With and without type hints
# Without type hints
grades_no_hint = [90, 85, 88]

# With type hints


print(f"Grades no hint: {grades_no_hint}")
print(f"Grades with hint: {grades_with_hint}")

# Dictionaries: With and without type hints
# Without type hints
info_no_hint = {"course": "Python", "level": "Beginner"}

# With type hints

print(f"Info no hint: {info_no_hint}")

# Functions: With and without type hints
# Without type hints
def greet_no_hints(name, age):
    return f"Hello {name}, you are {age} years old!"

# With type hints (parameters and return type)
def greet_with_hints(name: str, age: int) -> str:
    return f"Hello {name}, you are {age} years old!"

# Call functions
print(greet_no_hints("Bob", 30))
print(greet_with_hints("Alice", 25))




# Conditional statements
if age_no_hint > 20:
    print("You are an adult")
elif age_no_hint > 13:
    print("You are a teenager")
else:
    print("You are a child")

# Simple loop example
for grade in grades_no_hint:
    if grade >= 90:
        print(f"Grade {grade}: Excellent")
    elif grade >= 80:
        print(f"Grade {grade}: Good")
    else:
        print(f"Grade {grade}: Needs improvement")