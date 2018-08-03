from copy import *
import time
import signal
import os
import random
import sys

class Team13:

	def __init__(self):
		self.repeat = 0
		self.best_move = (0, 0)
		self.block_scores = [[6, 4, 4, 6], [4, 3, 3, 4], [4, 3, 3, 4], [6, 4, 4, 6]]
		self.zobrist = []
		self.hash_board = dict()
		self.aggressiveness = 3
		self.repeat = 0
		for i in xrange(16):
			self.zobrist.append([])
			for j in xrange(16):
				self.zobrist[i].append([])
				for k in xrange(2):
					self.zobrist[i][j].append(random.randint(0, 2**64))

	def heurestic1(self):
		heur = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
		for k in xrange(4):
			for z in xrange(4):
				score = 0
				for i in xrange(4):
					temp = 0
					for j in xrange(4):
						if self.board_copy.board_status[i+4*k][j+4*z] == self.player:
							temp += 1
						if self.board_copy.board_status[i+4*k][j+4*z] == self.opponent:
							temp = 0
							break
					if temp != 0:
						score = score + self.aggressiveness**temp
				heur[k][z] += score
				temp = 0
				score = 0
				for j in xrange(4):
					temp = 0
					for i in xrange(4):
						if self.board_copy.board_status[i+4*k][j+4*z] == self.player:
							temp += 1
						if self.board_copy.board_status[i+4*k][j+4*z] == self.opponent:
							temp = 0
							break
					if temp != 0:
						score = score + self.aggressiveness**temp
				heur[k][z] += score
				temp = 0
				score = 0
				if self.board_copy.board_status[4*k][1+4*z]!=self.opponent and self.board_copy.board_status[4*k+1][4*z]!=self.opponent and self.board_copy.board_status[4*k+1][2+4*z]!=self.opponent and self.board_copy.board_status[4*k+2][4*z+1]!=self.opponent:
					if self.board_copy.board_status[4*k][1+4*z] == self.player:
						temp += 1
					if self.board_copy.board_status[4*k+1][4*z] == self.player:
						temp += 1
					if self.board_copy.board_status[4*k+1][2+4*z] == self.player:
						temp += 1
					if self.board_copy.board_status[4*k+2][4*z+1] == self.player:
						temp += 1
					if temp != 0:
						score = score + self.aggressiveness**temp
				temp = 0
				if self.board_copy.board_status[4*k][2+4*z]!=self.opponent and self.board_copy.board_status[4*k+1][4*z+1]!=self.opponent and self.board_copy.board_status[4*k+2][2+4*z]!=self.opponent and self.board_copy.board_status[4*k+1][4*z+3]!=self.opponent:
					if self.board_copy.board_status[4*k][2+4*z] == self.player:
						temp += 1
					if self.board_copy.board_status[4*k+1][1+4*z] == self.player:
						temp += 1
					if self.board_copy.board_status[4*k+2][2+4*z] == self.player:
						temp += 1
					if self.board_copy.board_status[4*k+1][4*z+3] == self.player:
						temp += 1
					if temp != 0:
						score = score + self.aggressiveness**temp
				temp = 0
				if self.board_copy.board_status[2+4*k][4*z]!=self.opponent and self.board_copy.board_status[4*k+1][4*z+1]!=self.opponent and self.board_copy.board_status[4*k+2][2+4*z]!=self.opponent and self.board_copy.board_status[4*k+3][4*z+1]!=self.opponent:
					if self.board_copy.board_status[4*k+2][4*z] == self.player:
						temp += 1
					if self.board_copy.board_status[4*k+1][1+4*z] == self.player:
						temp += 1
					if self.board_copy.board_status[4*k+2][2+4*z] == self.player:
						temp += 1
					if self.board_copy.board_status[4*k+3][4*z+1] == self.player:
						temp += 1
					if temp != 0:
						score = score + self.aggressiveness**temp
				temp = 0
				if self.board_copy.board_status[1+4*k][4*z+2]!=self.opponent and self.board_copy.board_status[4*k+2][4*z+1]!=self.opponent and self.board_copy.board_status[4*k+2][3+4*z]!=self.opponent and self.board_copy.board_status[4*k+3][4*z+2]!=self.opponent:
					if self.board_copy.board_status[4*k+1][4*z+2] == self.player:
						temp += 1
					if self.board_copy.board_status[4*k+2][1+4*z] == self.player:
						temp += 1
					if self.board_copy.board_status[4*k+2][3+4*z] == self.player:
						temp += 1
					if self.board_copy.board_status[4*k+3][4*z+2] == self.player:
						temp += 1
					if temp != 0:
						score = score + self.aggressiveness**temp
				heur[k][z] += score
		final = 0
		score = 0
		for k in xrange(4):
			temp = 1
			for z in xrange(4):
				if self.board_copy.block_status[k][z]!=self.opponent and self.board_copy.block_status[k][z]!='d':
					temp *= max(heur[k][z], 1)
				if self.board_copy.block_status[k][z]==self.opponent or self.board_copy.block_status[k][z]=='d':
					temp = 0
					break
			final += temp
		for z in xrange(4):
			temp = 1
			for k in xrange(4):
				if self.board_copy.block_status[k][z]!=self.opponent and self.board_copy.block_status[k][z]!='d':
					temp *= max(heur[k][z], 1)
				if self.board_copy.block_status[k][z]==self.opponent or self.board_copy.block_status[k][z]=='d':
					temp = 0
					break
			final += temp
		temp = 1
		if self.board_copy.block_status[0][1]!=self.opponent and self.board_copy.block_status[1][0]!=self.opponent and self.board_copy.block_status[2][1]!=self.opponent and self.board_copy.block_status[1][2]!=self.opponent and self.board_copy.block_status[0][1]!='d' and self.board_copy.block_status[1][0]!='d' and self.board_copy.block_status[2][1]!='d' and self.board_copy.block_status[1][2]!='d':
			temp *= max(heur[0][1], 1)
			temp *= max(heur[1][0], 1)
			temp *= max(heur[1][2], 1)
			temp *= max(heur[2][1], 1)
			final += temp
		temp = 1
		if self.board_copy.block_status[1][1]!=self.opponent and self.board_copy.block_status[2][2]!=self.opponent and self.board_copy.block_status[0][2]!=self.opponent and self.board_copy.block_status[1][3]!=self.opponent and self.board_copy.block_status[1][1]!='d' and self.board_copy.block_status[2][2]!='d' and self.board_copy.block_status[0][2]!='d' and self.board_copy.block_status[1][3]!='d':
			temp *= max(heur[1][1], 1)
			temp *= max(heur[2][2], 1)
			temp *= max(heur[0][2], 1)
			temp *= max(heur[1][3], 1)
			final += temp
		temp = 1
		if self.board_copy.block_status[1][2]!=self.opponent and self.board_copy.block_status[2][1]!=self.opponent and self.board_copy.block_status[2][3]!=self.opponent and self.board_copy.block_status[3][2]!=self.opponent and self.board_copy.block_status[1][2]!='d' and self.board_copy.block_status[2][1]!='d' and self.board_copy.block_status[2][3]!='d' and self.board_copy.block_status[3][2]!='d':
			temp *= max(heur[1][2], 1)
			temp *= max(heur[2][1], 1)
			temp *= max(heur[3][2], 1)
			temp *= max(heur[2][3], 1)
			final += temp
		temp = 1
		if self.board_copy.block_status[1][1]!=self.opponent and self.board_copy.block_status[2][2]!=self.opponent and self.board_copy.block_status[2][0]!=self.opponent and self.board_copy.block_status[3][1]!=self.opponent and self.board_copy.block_status[1][1]!='d' and self.board_copy.block_status[2][2]!='d' and self.board_copy.block_status[2][0]!='d' and self.board_copy.block_status[3][1]!='d':
			temp *= max(heur[1][1], 1)
			temp *= max(heur[2][2], 1)
			temp *= max(heur[2][0], 1)
			temp *= max(heur[3][1], 1)
			final += temp
		return final

	def heurestic2(self):
		heur = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
		for k in xrange(4):
			for z in xrange(4):
				score = 0
				for i in xrange(4):
					temp = 0
					for j in xrange(4):
						if self.board_copy.board_status[i+4*k][j+4*z] == self.opponent:
							temp += 1
						if self.board_copy.board_status[i+4*k][j+4*z] == self.player:
							temp = 0
							break
					if temp != 0:
						score = score + self.aggressiveness**temp
				heur[k][z] += score
				temp = 0
				score = 0
				for j in xrange(4):
					temp = 0
					for i in xrange(4):
						if self.board_copy.board_status[i+4*k][j+4*z] == self.opponent:
							temp += 1
						if self.board_copy.board_status[i+4*k][j+4*z] == self.player:
							temp = 0
							break
					if temp != 0:
						score = score + self.aggressiveness**temp
				heur[k][z] += score
				score = 0
				temp = 0
				if self.board_copy.board_status[4*k][1+4*z]!=self.player and self.board_copy.board_status[4*k+1][4*z]!=self.player and self.board_copy.board_status[4*k+1][2+4*z]!=self.player and self.board_copy.board_status[4*k+2][4*z+1]!=self.player:
					if self.board_copy.board_status[4*k][1+4*z] == self.opponent:
						temp += 1
					if self.board_copy.board_status[4*k+1][4*z] == self.opponent:
						temp += 1
					if self.board_copy.board_status[4*k+1][2+4*z] == self.opponent:
						temp += 1
					if self.board_copy.board_status[4*k+2][4*z+1] == self.opponent:
						temp += 1
					if temp != 0:
						score = score + self.aggressiveness**temp
				temp = 0
				if self.board_copy.board_status[4*k][2+4*z]!=self.player and self.board_copy.board_status[4*k+1][4*z+1]!=self.player and self.board_copy.board_status[4*k+2][2+4*z]!=self.player and self.board_copy.board_status[4*k+1][4*z+3]!=self.player:
					if self.board_copy.board_status[4*k][2+4*z] == self.opponent:
						temp += 1
					if self.board_copy.board_status[4*k+1][1+4*z] == self.opponent:
						temp += 1
					if self.board_copy.board_status[4*k+2][2+4*z] == self.opponent:
						temp += 1
					if self.board_copy.board_status[4*k+1][4*z+3] == self.opponent:
						temp += 1
					if temp != 0:
						score = score + self.aggressiveness**temp
				temp = 0
				if self.board_copy.board_status[2+4*k][4*z]!=self.player and self.board_copy.board_status[4*k+1][4*z+1]!=self.player and self.board_copy.board_status[4*k+2][2+4*z]!=self.player and self.board_copy.board_status[4*k+3][4*z+1]!=self.player:
					if self.board_copy.board_status[4*k+2][4*z] == self.opponent:
						temp += 1
					if self.board_copy.board_status[4*k+1][1+4*z] == self.opponent:
						temp += 1
					if self.board_copy.board_status[4*k+2][2+4*z] == self.opponent:
						temp += 1
					if self.board_copy.board_status[4*k+3][4*z+1] == self.opponent:
						temp += 1
					if temp != 0:
						score = score + self.aggressiveness**temp
				temp = 0
				if self.board_copy.board_status[1+4*k][4*z+2]!=self.player and self.board_copy.board_status[4*k+2][4*z+1]!=self.player and self.board_copy.board_status[4*k+2][3+4*z]!=self.player and self.board_copy.board_status[4*k+3][4*z+2]!=self.player:
					if self.board_copy.board_status[4*k+1][4*z+2] == self.opponent:
						temp += 1
					if self.board_copy.board_status[4*k+2][1+4*z] == self.opponent:
						temp += 1
					if self.board_copy.board_status[4*k+2][3+4*z] == self.opponent:
						temp += 1
					if self.board_copy.board_status[4*k+3][4*z+2] == self.opponent:
						temp += 1
					if temp != 0:
						score = score + self.aggressiveness**temp
				heur[k][z] += score
		final = 0
		for k in xrange(4):
			temp = 1
			for z in xrange(4):
				if self.board_copy.block_status[k][z]!=self.player and self.board_copy.block_status[k][z]!='d':
					temp *= max(heur[k][z], 1)
				if self.board_copy.block_status[k][z]==self.player or self.board_copy.block_status[k][z]=='d':
					temp = 0
			final += temp
		for z in xrange(4):
			temp = 1
			for k in xrange(4):
				if self.board_copy.block_status[k][z]!=self.player and self.board_copy.block_status[k][z]!='d':
					temp *= max(heur[k][z], 1)
				if self.board_copy.block_status[k][z]==self.player or self.board_copy.block_status[k][z]=='d':
					temp = 0
			final += temp
		temp = 1
		if self.board_copy.block_status[0][1]!=self.player and self.board_copy.block_status[1][0]!=self.player and self.board_copy.block_status[2][1]!=self.player and self.board_copy.block_status[1][2]!=self.player and self.board_copy.block_status[0][1]!='d' and self.board_copy.block_status[1][0]!='d' and self.board_copy.block_status[2][1]!='d' and self.board_copy.block_status[1][2]!='d':
			temp *= max(heur[0][1], 1)
			temp *= max(heur[1][0], 1)
			temp *= max(heur[1][2], 1)
			temp *= max(heur[2][1], 1)
			final += temp
		temp = 1
		if self.board_copy.block_status[1][1]!=self.player and self.board_copy.block_status[2][2]!=self.player and self.board_copy.block_status[0][2]!=self.player and self.board_copy.block_status[1][3]!=self.player and self.board_copy.block_status[1][1]!='d' and self.board_copy.block_status[2][2]!='d' and self.board_copy.block_status[0][2]!='d' and self.board_copy.block_status[1][3]!='d':
			temp *= max(heur[1][1], 1)
			temp *= max(heur[2][2], 1)
			temp *= max(heur[0][2], 1)
			temp *= max(heur[1][3], 1)
			final += temp
		temp = 1
		if self.board_copy.block_status[1][2]!=self.player and self.board_copy.block_status[2][1]!=self.player and self.board_copy.block_status[2][3]!=self.player and self.board_copy.block_status[3][2]!=self.player and self.board_copy.block_status[1][2]!='d' and self.board_copy.block_status[2][1]!='d' and self.board_copy.block_status[2][3]!='d' and self.board_copy.block_status[3][2]!='d':
			temp *= max(heur[1][2], 1)
			temp *= max(heur[2][1], 1)
			temp *= max(heur[3][2], 1)
			temp *= max(heur[2][3], 1)
			final += temp
		temp = 1
		if self.board_copy.block_status[1][1]!=self.player and self.board_copy.block_status[2][2]!=self.player and self.board_copy.block_status[2][0]!=self.player and self.board_copy.block_status[3][1]!=self.player and self.board_copy.block_status[1][1]!='d' and self.board_copy.block_status[2][2]!='d' and self.board_copy.block_status[2][0]!='d' and self.board_copy.block_status[3][1]!='d':
			temp *= max(heur[1][1], 1)
			temp *= max(heur[2][2], 1)
			temp *= max(heur[2][0], 1)
			temp *= max(heur[3][1], 1)
			final += temp
		return final

	def search(self, depth, alpha, beta, to_maximise, old_move):
		status = self.board_copy.find_terminal_state()
		if status[0] == self.player:
			return 2**64
		if status[0] == self.opponent:
			return -2**64
		if status[0]=='NONE' and status[1]=='DRAW':
			temp = 0
			for i in xrange(4):
				for j in xrange(4):
					if self.board_copy.block_status[i][j] == self.player:
						temp += self.block_scores[i][j]
					if self.board_copy.block_status[i][j] == self.opponent:
						temp -= self.block_scores[i][j]
			return temp**3
		if depth == 0:
			hash_value = 0
			for i in xrange(16):
				for j in xrange(16):
					if self.board_copy.board_status[i][j] != '-':
						if self.board_copy.board_status[i][j] == self.player:
							hash_value = hash_value^self.zobrist[i][j][0]
						else:
							hash_value = hash_value^self.zobrist[i][j][1]
			if hash_value in self.hash_board:
				if to_maximise:
					return self.hash_board[hash_value]
				return -self.hash_board[hash_value]
			self.hash_board[hash_value] = self.heurestic1()-self.heurestic2()
			if to_maximise:
				return self.hash_board[hash_value]
			else:
				return -self.hash_board[hash_value]
		if to_maximise:
			v = -(2**65)
			valid_cells = self.board_copy.find_valid_move_cells(old_move)
			for valid_move in valid_cells:
				ret = self.board_copy.update(old_move, valid_move, self.player)
				self.last_move = valid_move
				if ret[1]==True and self.repeat==0:
					# print 'Bonus!!!!'
					self.repeat = 1
					val = self.search(depth-1, alpha, beta, 1, valid_move)
					self.repeat = 0
				else:
					self.repeat = 0
					val = self.search(depth-1, alpha, beta, 0, valid_move)
				self.board_copy.board_status[valid_move[0]][valid_move[1]] = '-'
				self.board_copy.block_status[valid_move[0]/4][valid_move[1]/4] = '-'
				if val>v and self.level==depth:
					self.best_move = valid_move
				v = max(v, val)
				alpha = max(v, alpha)
				if beta <= alpha:
					return v
			return v
		v = 2**65
		valid_cells = self.board_copy.find_valid_move_cells(old_move)
		for valid_move in valid_cells:
			ret = self.board_copy.update(old_move, valid_move, self.opponent)
			self.last_move = valid_move
			if ret[1]==True and self.repeat==0:
				# print 'Bonus!!!'
				self.repeat = 1
				val = self.search(depth-1, alpha, beta, 0, valid_move)
				self.repeat = 0
			else:
				self.repeat = 0
				val = self.search(depth-1, alpha, beta, 1, valid_move)
			v = min(v, val)
			beta = min(v, beta)
			self.board_copy.board_status[valid_move[0]][valid_move[1]] = '-'
			self.board_copy.block_status[valid_move[0]/4][valid_move[1]/4] = '-'
			if beta <= alpha:
				return v
		return v

	def signal_handler(self, signal, frame):
		raise Exception('Time up!!')

	def move(self, board, old_move, flag):
		original_board = deepcopy(board)
		valid_cells = board.find_valid_move_cells(old_move)
		self.board_copy = board
		self.player = flag
		self.last_move = (0, 0)
		if flag == 'x':
			self.opponent = 'o'
		else:
			self.opponent = 'x'
		signal.signal(signal.SIGALRM, self.signal_handler)
		signal.alarm(15)
		valid_cells = self.board_copy.find_valid_move_cells(old_move)
		optimal = valid_cells[random.randrange(len(valid_cells))]
		try:
			for it in xrange(3, 256):
				self.level = it
				self.search(it, -(2**65), 2**65, 1, old_move)
				optimal = self.best_move
				self.board_copy = original_board
		except Exception as e:
						pass
		return optimal
