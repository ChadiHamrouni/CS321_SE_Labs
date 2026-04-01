from typing import Literal
from pydantic import BaseModel
from agents import function_tool


CONVERSIONS: dict[str, float] = {
    "km→miles":       0.621371,
    "miles→km":       1.60934,
    "kg→lbs":         2.20462,
    "lbs→kg":         0.453592,
    "meters→feet":    3.28084,
    "feet→meters":    0.3048,
    "liters→gallons": 0.264172,
    "gallons→liters": 3.78541,
}


@function_tool
def convert_units(value: float, from_unit: str, to_unit: str) -> str:
    """Convert a value between two units (e.g. km to miles, kg to lbs).

    Supported pairs: km/miles, kg/lbs, meters/feet, liters/gallons.
    """
    key = f"{from_unit}→{to_unit}"
    if key not in CONVERSIONS:
        return f"Unsupported conversion: {key}. Supported: {', '.join(CONVERSIONS)}."
    result = value * CONVERSIONS[key]
    return f"{value} {from_unit} = {result:.4f} {to_unit}"


class CalcInput(BaseModel):
    a: float
    b: float
    operation: Literal["add", "subtract", "multiply", "divide"]


@function_tool
def calculate(params: CalcInput) -> str:
    """Perform a basic arithmetic operation (add, subtract, multiply, divide) on two numbers."""
    a, b, op = params.a, params.b, params.operation
    if op == "add":
        return str(a + b)
    if op == "subtract":
        return str(a - b)
    if op == "multiply":
        return str(a * b)
    if op == "divide":
        if b == 0:
            return "Error: division by zero."
        return str(a / b)
    return "Unknown operation."
