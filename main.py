from src.CycleRecorder import RecordActions
from src.Repeater import RepeatAction
from src.InputConverter import Convert, converted

if __name__ == '__main__':
    Convert(r'C:\Users\Damian\source\repos\VisionScripter\test.txt')
    sequence = RecordActions()
    RepeatAction(sequence)