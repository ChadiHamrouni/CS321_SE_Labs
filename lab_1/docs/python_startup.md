# Python Startup Guide

If you're on Windows, use PowerShell or Windows Terminal (install from Microsoft Store) for these commands.

## Install Python
- Linux/Mac: Download from https://python.org or use package manager (e.g., `sudo apt install python3` on Ubuntu)
- Windows: Download installer from https://python.org and run it

## Install VS Code
- Linux/Mac: Download .deb/.rpm from https://code.visualstudio.com or use package manager
- Windows: Download installer from https://code.visualstudio.com and run it

## Install Python Extension in VS Code
- Open VS Code, go to Extensions (Ctrl+Shift+X), search for "Python", install the official one by Microsoft

## Check Python Installation
- Linux/Mac: `python --version` or `python3 --version`
- Windows: `python --version`

## Install virtualenv
- Linux/Mac: `python -m pip install virtualenv` or `python3 -m pip install virtualenv`
- Windows: `python -m pip install virtualenv`

## Create Virtual Environment
- Linux/Mac: `virtualenv myenv`
- Windows: `virtualenv myenv` (if not found, use `python -m virtualenv myenv`)

## Activate Virtual Environment
- Linux/Mac: `source myenv/bin/activate`
- Windows: `myenv\Scripts\activate`

## Deactivate Virtual Environment
- Linux/Mac: `deactivate`
- Windows: `deactivate`

## Alternative: Using built-in venv (simpler, no installation needed)
- Linux/Mac: `python -m venv myenv` or `python3 -m venv myenv`
- Windows: `python -m venv myenv`

## Activate Virtual Environment (venv)
- Linux/Mac: `source myenv/bin/activate`
- Windows: `myenv\Scripts\activate`

## Deactivate Virtual Environment (venv)
- Linux/Mac: `deactivate`
- Windows: `deactivate`

## Install Requirements (if requirements.txt exists)
- Linux/Mac: `pip install -r requirements.txt`
- Windows: `pip install -r requirements.txt`

## Run Python Script
- Linux/Mac: `python main.py`
- Windows: `python main.py`

## Everything is an Object in Python

In Python, all data types are objects, meaning they are instances of classes with their own attributes and methods. This is key to understanding how Python works.

- **Strings (str)**: Objects with methods like `upper()`, `split()`, `replace()`. Example: `"hello".upper()` returns `"HELLO"`.
- **Lists (list)**: Objects with methods like `append()`, `pop()`, `sort()`. Example: `[1,2,3].append(4)` adds 4 to the list.
- **Dictionaries (dict)**: Objects with methods like `get()`, `keys()`, `values()`. Example: `{"a":1}.get("a")` returns 1.
- **Integers (int)**: Objects with methods like `bit_length()`, `__add__()`. Example: `(5).bit_length()` returns 3.
- **Floats (float)**: Objects with methods like `is_integer()`, `hex()`. Example: `(3.14).is_integer()` returns False.
- **Booleans (bool)**: Subclass of int, inherits int methods. Example: `True + 1` equals 2.
- **Other types**: Tuples, sets, etc., all have their own methods.

Built-in functions like `len()`, `min()` work on these objects, but methods are called using dot notation on the object itself.

## Predefined Functions Reference

| Function | Parameters | Returns | Description |
|----------|------------|---------|-------------|
| len | obj | int | Returns the length of an object (string, list, dict, etc.) |
| str.split |  | list | Splits string into list using whitespace |
| str.join | iterable | str | Joins iterable elements into string with self as separator |
| str.upper |  | str | Returns uppercase version of string |
| str.lower |  | str | Returns lowercase version of string |
| str.startswith | prefix | bool | Checks if string starts with prefix |
| str.replace | old, new | str | Replaces occurrences of old with new |
| str.strip |  | str | Removes leading/trailing whitespace |
| str.count | sub | int | Counts occurrences of substring |
| list.append | obj | None | Adds obj to end of list |
| dict.get | key | value | Returns value for key, or None if not found |
| range | stop | range object | Creates sequence of numbers from 0 to stop-1 |
| sum | iterable | number | Sums elements of iterable |
| max | iterable | value | Returns maximum value from iterable |
| min | iterable | value | Returns minimum value from iterable |

## Additional Python Concepts

Before advanced exercises, understand these key concepts:

- **Loops**: `for` loops iterate over sequences; `while` loops repeat while condition is true. Example: `for i in range(5): print(i)`
- **Input/Output**: `input()` reads user input as string; `print()` outputs to console.
- **Basic Math Operators**: `+`, `-`, `*`, `/`, `//` (floor division), `%` (modulo), `**` (power).
- **Comparison Operators**: `==`, `!=`, `<`, `>`, `<=`, `>=` for conditions.
- **Logical Operators**: `and`, `or`, `not` for combining conditions.
- **Exception Handling**: Use `try/except` to handle errors. Example: `try: x = int(input()) except ValueError: print("Invalid")`
- **Modules**: Import code with `import module`. Example: `import math; math.sqrt(4)`
- **List Comprehensions**: Create lists concisely. Example: `[x*2 for x in [1,2,3]]` → `[2,4,6]`
- **File I/O**: `open()`, `read()`, `write()`, `close()` for files. Always use `with` for safety: `with open('file.txt', 'r') as f: data = f.read()`
- **Variable Scope**: Local variables inside functions; global outside. Use `global` to modify globals inside functions.

