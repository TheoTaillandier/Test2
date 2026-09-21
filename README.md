# Test2
import sys
import importlib.util

print("Python :", sys.version)
print()

libraries = [
    "pandas",
    "numpy",
    "requests",
    "matplotlib",
    "plotly",
    "yfinance",
    "bs4",
    "selenium",
]

for lib in libraries:
    available = importlib.util.find_spec(lib) is not None
    print(f"{lib:12} : {'OK' if available else 'NON'}")
