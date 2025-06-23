from src.classes.file import File

file = File('planete.csv', ';')
print(file.delimiter)

print(file.getStats())