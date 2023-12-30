converted = [
    ("maciej owczarz", "07:00", "08:00"),
    ("oliwier napiórkowski", "07:20", "08:00")
]

def Convert(path):
    global converted
    converted.clear()
    with open(path, encoding="utf-8") as f:
        for line in f:
            AppendRecord(line)

def AppendRecord(line:str):
    global converted
    line = line.strip()
    splitted = line.split(' ')
    length = len(splitted)
    exitTime = splitted[length - 1]
    exitTime = exitTime.replace('.', ':')
    exitTime = AssureProperTimeFormat(exitTime)
    entryTime = splitted[length - 2]
    entryTime = entryTime.replace('.', ':')
    entryTime = AssureProperTimeFormat(entryTime)
    nameAndSurname = ""
    for i in range(length - 2):
        nameAndSurname += splitted[length - 3 - i] + ' '
    nameAndSurname = nameAndSurname.strip()
    converted.append((nameAndSurname, entryTime, exitTime))

def AssureProperTimeFormat(timeString):
    splitted = timeString.split(':')
    if len(splitted[0]) == 1:
        timeString = insert_char(timeString, '0', 0)
    return timeString

def insert_char(string, char, index):
    return string[:index] + char + string[index:]