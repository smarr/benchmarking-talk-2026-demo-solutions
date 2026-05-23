def write_macro(name, value, file):
    print(f"\\{name}{{{value:.2f}}}")
    file.write(f"\\newcommand{{\\{name}}}{{{value:.2f}$\\times$\\xspace}}\n")
