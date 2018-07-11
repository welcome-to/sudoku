from main import *

shit_board_1 = Board()
print(shit_board_1)
print(shit_board_1.iscorrect())

shit_board_1.cellupdate(2, 2, set([]))
print(shit_board_1)
print(shit_board_1.iscorrect())

correct = read("correct.csv")
print(correct)
print(correct.testcontent())
print(shit_board_1.testcontent())
