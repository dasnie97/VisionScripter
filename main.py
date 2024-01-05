from src.CycleRecorder import RecordActions
from src.Repeater import RepeatAction
from Helpers import *
from src.CreateSequence import *

if __name__ == '__main__':
    Convert(r'C:\Users\Damian\source\repos\VisionScripter\test.txt')
    sequence = RecordActions()
    sequence = CreateSequence(sequence, converted)
    RepeatAction(sequence)