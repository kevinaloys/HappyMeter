__author__ = "Kevin Aloysius"

#This Module is reponsible for creating Real World Female and Male First Names and Last Name So that
#it looks Legit
#Names obtained from U.S Census Data 1990 \m/ 
#       


import random
import string

global female_first
global male_first
global last_name
## Removing \n while reading from the text for female first names , male first names and general last names.


text = open('k-female.txt','r')
female_first=text.readlines()
for i in range(len(female_first)):
	female_first[i]=female_first[i].rstrip('\n')
text.close()

text = open('k-male.txt','r')
male_first=text.readlines()
for i in range(len(male_first)):
	male_first[i]=male_first[i].rstrip('\n')
text.close()

text=open('k-last.txt','r')
last_name=text.readlines()
for i in range(len(last_name)):
	last_name[i]=last_name[i].rstrip('\n')
text.close()