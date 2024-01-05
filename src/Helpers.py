class InputConverter:
    def __init__(self) -> None:
        self.converted = []

    def Convert(self, path):
        self.converted.clear()
        with open(path, encoding="utf-8") as f:
            for line in f:
                self.AppendRecord(line)

    def AppendRecord(self, line:str):
        line = line.strip()
        splitted = line.split(' ')
        length = len(splitted)
        exitTime = splitted[length - 1]
        exitTime = exitTime.replace('.', ':')
        exitTime = self.AssureProperTimeFormat(exitTime)
        entryTime = splitted[length - 2]
        entryTime = entryTime.replace('.', ':')
        entryTime = self.AssureProperTimeFormat(entryTime)
        nameAndSurname = ""
        for i in range(length - 2):
            nameAndSurname += splitted[length - 3 - i].capitalize() + ' '
        nameAndSurname = nameAndSurname.strip()
        self.converted.append((nameAndSurname, entryTime, exitTime))

    def AssureProperTimeFormat(self, timeString):
        splitted = timeString.split(':')
        if len(splitted[0]) == 1:
            timeString = self.insert_char(timeString, '0', 0)
        return timeString

    def insert_char(self, string, char, index):
        return string[:index] + char + string[index:]