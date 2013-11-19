__author__="Kevin Aloysius"

import random
import string
from name import *

global x # Global variable x is resonsible for storing the list of random users generatod vie the randomUserGen Function
x=list() # 

#userIdGenerator is Responsible for creating User ID

def userIdGenerator(size=6, chars=string.digits + string.ascii_uppercase):
	return ''.join(random.choice(chars) for x in range(size))

def userGenerator():
	return createUser(random.choice(female_first + male_first),random.choice(last_name),random.randint(13,70))


class createUser(object):
	"""docstring for createUser"""
	def __init__(self, firstname='John', lastname='Doe', age=25):
		super(createUser, self).__init__()
		self.firstname = firstname
		self.lastname = lastname
		self.age = age
		self.happiness = 100 #Beginning of Time Happiness
		self.mood = []
		self.belongsToGroup=[]

	def appendMood(self,value):
		self.mood.append(value)


class createGroup:
	"""docstring for createGroup"""
	def __init__(self, groupname, members):
		super(createGroup, self).__init__()
		self.groupname = groupname
		self.members = []


#Calling the Function--> e.g randomUserGen(number)..This Only Generate the Random Users but wont Print It.Trust Me it is created in the Memory.
def randomUserGen(value):
	for i in range(value):
		x.append(userGenerator())


# This Fucntion is enables you to print the random users you created using randomUserGen(value) function.
#I just wanted to provide to the developers of this project the liberty to just create a random set of users coz not all of the times
#you want to create the random users and print it.Sometimes you just want to create it and sometimes you just want to print.
#Software Engineering also promotes the idea of moudlarity so I just wanted to see how far my Modularity can go.Cheers!!
def printRandomUserGen():
	for i in range(len(x)):
		print x[i].firstname, x[i].lastname

