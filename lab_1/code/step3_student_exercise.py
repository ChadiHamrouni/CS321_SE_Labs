# Step 3: Student Exercise - Multiple Function Implementations
# This file contains function stubs that students need to implement themselves.
# Each function builds on concepts from steps 1 and 2 (variables, lists, dicts, strings, conditionals).
# Students should fill in the function bodies to make the tests at the bottom pass.
# Do not modify the function signatures or the test code.

# Exercise 1: List Operations
# Implement a function that adds an item to a list and returns the updated list
def add_to_list(items, new_item):
    # TODO: Add new_item to the items list and return the list
    pass

# Exercise 2: Dictionary Lookup
# Implement a function that checks if a key exists in a dictionary and returns its value or None
def find_in_dict(data, key):
    # TODO: If key exists in data, return its value; otherwise return None
    pass

# Exercise 3: String Processing
# Implement a function that takes a string, converts it to lowercase, and splits it into words
def process_string(text):
    # TODO: Convert text to lowercase and split into a list of words
    pass

# Exercise 4: Conditional Logic with Lists
# Implement a function that filters a list to include only items longer than a given length
def filter_long_items(items, min_length):
    # TODO: Return a new list containing only strings from items that are longer than min_length
    pass

# Exercise 5: Dictionary Update
# Implement a function that updates a dictionary with a new key-value pair
def update_dict(data, key, value):
    # TODO: Add or update the key with the value in data and return the updated dict
    pass

# Test functions (students should run this to verify their implementations)
if __name__ == "__main__":
    # Test Exercise 1
    test_list = ["apple", "banana"]
    result1 = add_to_list(test_list, "cherry")
    print(f"Exercise 1: {result1}")  # Expected: ['apple', 'banana', 'cherry']

    # Test Exercise 2
    test_dict = {"name": "Alice", "age": "25"}
    result2 = find_in_dict(test_dict, "name")
    print(f"Exercise 2 (existing key): {result2}")  # Expected: Alice
    result2b = find_in_dict(test_dict, "city")
    print(f"Exercise 2 (missing key): {result2b}")  # Expected: None

    # Test Exercise 3
    test_text = "Hello World Python"
    result3 = process_string(test_text)
    print(f"Exercise 3: {result3}")  # Expected: ['hello', 'world', 'python']

    # Test Exercise 4
    test_items = ["a", "ab", "abc", "abcd"]
    result4 = filter_long_items(test_items, 2)
    print(f"Exercise 4: {result4}")  # Expected: ['abc', 'abcd']

    # Test Exercise 5
    test_data = {"x": 1, "y": 2}
    result5 = update_dict(test_data, "z", 3)
    print(f"Exercise 5: {result5}")  # Expected: {'x': 1, 'y': 2, 'z': 3}