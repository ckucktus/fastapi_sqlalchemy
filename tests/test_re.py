import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))

from project.popblyat import process

def test_process():
    input_data = ['1 thousand devils', 'My name is 9Pasha', 'Room #125 costs $100', '888']
    expected = ['thousand devils', 'My name is Pasha', 'Room costs', '']

    assert process(input_data) == expected