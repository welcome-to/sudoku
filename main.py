from copy import deepcopy
from itertools import combinations
from random import randint

#создание класса ячеек с атребутами set (список возможных чисел) и abs (точое\предположительное заполнение)
class Cell(object):
	def __init__(self,row,column):
		#self.set = [1,2,3,4,5,6,7,8,9]
		self.set = set([1,2,3,4,5,6,7,8,9])
		self.abs = False
		self.row = row
		self.column = column
	def __eq__(self,cell):
		if self.set == cell.set:
			return True
		else:
			return False
	def __repr__(self):
		return str(self.set)

	#метод обновляющий set возможный чисел на новый
	def update(self,NewSet):
		self.set = NewSet
		if len(self.set) == 1:
			self.abs = True


#проверка полного заполнения блока чисел (строки,столбца,квадрата)
def isfull(block):
	if block == set([1,2,3,4,5,6,7,8,9]):
		return True
	else:
		return False


#создание класа доски (доска - масив из ячеек 9 на 9)
class Board(object):
	def __init__(self):
		data = []
		for i in range(9):
			row = []
			for a in range(9):
				row.append(Cell(i,a))
			data.append(row)
		self.data = data

	#создание копии доски
	def clone(self):
		board = Board()
		board.data = deepcopy(self.data)
		return board
	
	#обновление сета ячейки по адресу
	def cellupdate(self,row,cell,NewSet):
		self.data[row][cell].update(NewSet)

	#получение сета ячейки по адресу 
	def CellSet(self,row,element):
		cellset=self.data[row][element].set
		return cellset

	#получение номера квадрата по адресу ячейки
	def squareid(self,row,column):
		row1=row//3
		column1=column//3
		square = row1*3 + column1
		return square

	#получение списка точно выбраных элементов в ряду по его номеру 
	def rowcont(self,row):
		cell = 0
		row1 = set()
		while cell<9:
			if len(self.CellSet(row,cell)) == 1:
				row1 |= self.CellSet(row,cell)
				#row1.append(list(self.CellSet(row,cell))[0])
			cell+=1
		return row1

	#получение списка точно выбраных элементов в столбце по его номеру 
	def columncont(self,column):
		row = 0 
		column1 = set()
		while  row<9:
			if len(self.CellSet(row,column)) == 1:
				column1 |= self.CellSet(row,column)
			row+=1
		return column1

	#получение списка точно выбраных элементов в квадрате по его номеру
	def squarecont(self,square):
		scuarerow = square // 3
		scuarecolumn = square % 3
		row = [scuarerow * 3,scuarerow * 3 + 1,scuarerow * 3 +2]
		column = [scuarecolumn * 3,scuarecolumn * 3 + 1,scuarecolumn * 3 +2]
		row1 = 0
		column1 = 0
		square = set()
		while row1 < 3:
			column1=0
			while column1 < 3:
				if len(self.CellSet(row[row1],column[column1])) == 1:
					square |= self.CellSet(row[row1],column[column1])
				column1+=1
			row1+=1
		return square

	#получение полного контента квадрата
	def allsquarecont(self,square):
		scuarerow = square // 3
		scuarecolumn = square % 3
		row = [scuarerow * 3,scuarerow * 3 + 1,scuarerow * 3 +2]
		column = [scuarecolumn * 3,scuarecolumn * 3 + 1,scuarecolumn * 3 +2]
		row1 = 0
		column1 = 0
		square = []
		while row1 < 3:
			column1 = 0
			while column1 < 3:
				square.append(self.data[row[row1]][column[column1]])
				column1+=1
			row1+=1
		return square

	#получение полного контента колонны
	def allcolumncont(self,column):
		row = 0 
		column1 = []
		while  row<9:
			column1.append(self.data[row][column]) 
			row+=1
		return column1

	#получение полного контента ряда
	def allrowcont(self,row):
		cell = 0
		row1 = []
		while cell<9:
			row1.append(self.data[row][cell])
			cell+=1
		return row1

	#количество не однозначно заплненых функций (отладочная функция)
	def count_of_not_full(self):
		result = 0
		for row in range(9):
			for column in range(9):
				if len(self.CellSet(row, column)) > 1:
					result += 1
		return result

	#проверка таблицы на правильное заполнение
	def testcontent(self):
		a=0
		while a<9:
			if (not isfull(self.squarecont(a))) or (not isfull(self.rowcont(a))) or (not isfull(self.columncont(a))):
				return False
			a+=1
		return True

	def __str__(self):
		return '\n'.join([' '.join([str(self.CellSet(x,y)) for y in range(9)]) for x in range(9)])
	
	#проверка таблицы на возмоноть дозаполнения
	def iscorrect(self):
		for row in range(9):
			for column in range(9):
				if len(self.CellSet(row,column)) == 0:
					return False
		return True

	def is_full(self):
		for row in range(9):
			for column in range(9):
				if len(self.CellSet(row,column)) != 1:
					return False
		return True



#чтение доски из файла
def read(filename):
	board = Board()
	with open(filename, 'r') as fp:
		lines = fp.readlines()
		row = 0
		for line in lines:
			numbers = map(int, line.split(';'))
			for pair in zip(range(9), numbers):
				if pair[1] != 0:
					board.cellupdate(row, pair[0], set([pair[1]]))
			row += 1
	return board

#заполнение доски в файл ответа
def output(filename,board):
	x=0
	file = open(filename,'w')

	while x<9:
		y = 0
		while y<9:
			file.write(str(board.CellSet(x,y))+';')
			y+=1
		file.write('\n')
		x+=1
	file.close()

#читай название (я не придумал описание)
def makesomethingood(row,column,board):
	square=board.squareid(row,column)
	toupdate = board.CellSet(row,column)
	square=board.squarecont(square)
	todell = square | board.rowcont(row) | board.columncont(column)
	toupdate = toupdate - todell
	board.cellupdate(row,column,toupdate)

#уменьшение списка возможных элементов 
def deleteextern(board):
	row=0
	while row < 9:
		column=0
		while column < 9:
			if len(board.CellSet(row,column)) != 1:
				makesomethingood(row,column,board)
			column+=1
		row+=1

#вписывание чисел однозначно встречающихся в блоках
def insertonlypos(block):
	for number in range(1, 10):
		k=0
		for cell in range(9):
			if number in block[cell].set:
				k+=1
				cellID = cell
		if k == 1:
			block[cellID].update(set([number]))

#вписывание чисел однозначно встречающихся в доске
def biginsertonlypos(board):
	for i in range(9):
		insertonlypos(board.allsquarecont(i))
		insertonlypos(board.allcolumncont(i))
		insertonlypos(board.allrowcont(i))

#решить судоку
def solve(board):
	while not board.testcontent():
		laststep = board.clone()
		deleteextern(board)
		biginsertonlypos(board)
		if board.data == laststep.data:
			break
	if board.testcontent():
		return board

	if not board.iscorrect() or (board.is_full() and not board.testcontent()):
		return

	row, column = choose_random_cell(board)

	candidates = list(board.CellSet(row, column))
	for c in candidates:
		new_board = board.clone()
		new_board.cellupdate(row, column, set([c]))
		result = solve(new_board)
		if result is not None:
			return result

	return

#выбрать рандомную ячейку с минимальной длинной 
def choose_random_cell(board):
	length=10
	for row in range(9):
		for column in range(9):
			if (len(board.CellSet(row,column)) < length) and (len(board.CellSet(row,column)) >= 2):
				length = len(board.CellSet(row,column))
				row1 = row
				column1 = column
			
	return row1, column1

#основная програма
def main():
	board = read(input('Введите название файла судоку:'))
	if board.testcontent():
		print('Yeaaaa')
	ans = solve(board)
	if ans == None:
		print('Xyu')

	else:
		print('Yeaaaa')
		output(input('Введите название файла вывода:'),ans)








if __name__ == '__main__':
	main()