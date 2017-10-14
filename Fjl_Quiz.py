"""

Author:	  Bartlomiej Tuchowski
Created:     06.08.2017

"""
#imports
import random
import pymysql as db

#definitions
def MainMenu():
	print ("---Main Menu---\n\n(a)New Game\n(b)Scores\n(c)Reset Scores\n(d)Add Questions\n(e)Rules\n(q)Quit\nOPTIONS [a, b, c, d ,q]")
	choice = input("What is your choice? ")
	if choice == "a":
		NewGame()
	elif choice == "b":
		Scores()
	elif choice == "c":
		ResetScores()
	elif choice == "d":
		AddQuestions()
	elif choice == "e":
		Rules()
	elif choice == "q":
		Quit()
	else:
		print ("\nUse one of Main Menu command.\n")
		MainMenu()	

def NewGame():
	name = str(input("Enter your name: "))
	connection= db.connect(host= "localhost", user = "user", passwd="okon", db="quiz")
	cur = connection.cursor()
	query = "SHOW TABLES;"
	cur.execute(query)
	results = cur.fetchall()
	if results[0] == ('newgame',):
			query = "DROP TABLE IF EXISTS newgame;"
			cur.execute(query)
	query = "CREATE TABLE newgame (Question VARCHAR(500), Answer VARCHAR(500), IDX Serial);"
	cur.execute(query)
	query = ("SELECT Question, Answer FROM questions;")
	cur.execute(query)
	results = cur.fetchall()
	for data in results:
		query = "INSERT INTO newgame (Question, Answer) VALUE (%s, %s);"
		cur.execute(query, (data[0], data[1]))
		connection.commit()
	question_IDX=[]
	query = "SELECT IDX FROM newgame;"
	number_of_questions = cur.execute(query)
	counter=1
	for digit in range (0, number_of_questions):
		question_IDX.append(counter)
		counter += 1
	counter = 0
	score = 0
	for question in range(0,20):
		counter += 1
		print ("Number of question: ", counter)
		question=random.choice(question_IDX)
		query = "SELECT Question FROM newgame WHERE IDX=%s;"
		cur.execute(query, question)
		results = cur.fetchall()
		for character in results:
			print (" ".join([r for r in character]))
		answer = str(input())
		query = "SELECT Answer FROM newgame WHERE Question=%s;"
		cur.execute(query, results )
		results = cur.fetchall()
		for row in results:
			results=" ".join([r for r in row])
		if answer == results:
			print ("Good answer!")
			score += 3
			question_IDX.remove(question)
		else:
			print ("Wrong answer :(")
			question_IDX.remove(question)
			score -= 1
		if counter == 20:
			print (name, "you get", score, "points! You can check your ranking in scores.")
			query = "INSERT INTO scores (Name, Score) VALUE (%s, %s);"
			cur.execute(query, (name, score))
			connection.commit()
			connection.close
			Step()

def Scores():
	connection=db.connect(host="localhost", user="user", passwd="okon", db="quiz")
	cur=connection.cursor()
	print ("Scores:")
	query = "DESCRIBE scores;"
	cur.execute(query)
	columns = [c[0] for c in cur.fetchall()]
	print(' '.join([ "%-10s" % c for c in columns]))
	print('-' * (10*len(columns)))
	query="SELECT * FROM scores;"
	cur.execute(query)
	results = cur.fetchall()
	for row in results:
		print (" ".join([ "%-10s" % r for r in row]))
	Step()

def ResetScores():
	connection=db.connect(host="localhost", user="user", passwd="okon", db="quiz")
	cur=connection.cursor()
	choice = str(input("Are you sure you want to CLEAR scores ? OPTIONS[y, n] "))
	if choice == "n":
		MainMenu()
	elif choice == "y":
		query = "DROP TABLE IF EXISTS scores;"
		cur.execute(query)
		query = "CREATE TABLE scores (Name VARCHAR(20), Score INT, IDX Serial);"
		cur.execute(query)
		print ("Score table is empty now.")
		Step()
	else:
		print ("\nUse one of OPTIONS.\n")
		
def AddQuestions():
	connection=db.connect(host="localhost", user="user", passwd="okon", db="quiz")
	cur=connection.cursor()
	question=str(input("Write a question: "))
	answer=str(input("Add an answer: "))
	query="INSERT INTO questions (Question, Answer) VALUE (%s, %s);"
	cur.execute(query, (question, answer))
	connection.commit()
	print ("Question added!")
	connection.close()
	def AddQuestionsStep():
		choice=str(input("Do you want to add next question ? OPTIONS[y, n] "))
		if choice == "y":
			AddQuestions()
		elif choice =="n":
			MainMenu()
		else:
			print ("\nUse one of OPTIONS.\n")
			AddQuestionsStep()
	AddQuestionsStep()

def Rules():
	print ("---Game Rules---\n\n1. The game consists of a set of 20 questions\n2. For correct answer you get 3 points.\n3. For wrong answer you get -1 point.\n4. Use capital letters only if it's required.\n5. Have fun :)\n")
	Step()
	
def Quit():
	print ("\nSee you next time :)")
	exit()
	
def Step():
	choice = input("Do you want to continue ? OPTIONS[y, n] ")
	if choice == "y":
		MainMenu()
	elif choice == "n":
		Quit()
	else: 
		print ("\nUse one of OPTIONS.\n")
		Step()

#run
if __name__=="__main__":		
	MainMenu()
	