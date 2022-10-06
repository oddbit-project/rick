from rick.resource.console import AnsiColor


color = AnsiColor()

# text color: red
msg = color.red('red message')
print(msg)

# text color: light blue
msg = color.light_blue('light blue message')
print(msg)

# text color: green
msg = color.green('green message')
print(msg)

# text color: green; background: white
msg = color.green('green message on white background', 'white')
print(msg)

# text color: green, bold; background: white
msg = color.green('bold green message on white background', 'white', 'bold')
print(msg)

# text color: green, underline; background: white
msg = color.green('underline bold green message on white background', 'white', ['bold', 'underline'])
print(msg)