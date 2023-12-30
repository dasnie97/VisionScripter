sequence = []

def append_mouse_position(x, y):
    sequence.append((x,y))

def append_text_input(text):
    if text != "":
        sequence.append(text)