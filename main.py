import os
import ast
from collections import Counter

def read_python_files(directory):
    """Read all Python files and return their content."""
    code = ""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    code += f.read() + "\n"
    return code

def summarize_code(code):
    """Generate a simple summary of the code."""
    tree = ast.parse(code)
    func_names = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    class_names = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
    return {
        "functions": Counter(func_names),
        "classes": Counter(class_names)
    }

def generate_insights(code):
    """Generate simple insights from the code."""
    insights = []
    if "import os" in code:
        insights.append("Consider security implications of file operations.")
    if "import numpy" in code and "import pandas" not in code:
        insights.append("You might benefit from integrating Pandas for data handling.")
    return insights

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python main.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory.")
        sys.exit(1)

    code = read_python_files(directory)
    if not code.strip():
        print("No Python files found in the directory.")
        sys.exit(0)

    summary = summarize_code(code)

    print("Code Summary:")
    print(f"- Functions: {dict(summary['functions'])}")
    print(f"- Classes: {dict(summary['classes'])}")

    print("\nSuggestions:")
    for insight in generate_insights(code):
        print(f"- {insight}")