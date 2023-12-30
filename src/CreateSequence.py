def CreateSequence(sequence:list, input:list):
    newList = []
    for item in input:
        counter = 0
        for step in sequence:
            if isinstance(step, str):
                newList.append(item[counter])
                counter += 1
            else:
                newList.append(step)
    return newList

