import sys
import os
import subprocess
from multiprocessing.dummy import Pool as ThreadPool 
import time
from string import ascii_lowercase
from itertools import product

ver = '1.0'

class msg:
	def good(message):
		print('\x1b[34m' + '[*]' + '\x1b[0m', message.strip())
	def warn(message):
		print('\x1b[1;33m' + '[!]' + '\x1b[0m', message.strip())
	def info(message):
		print('\x1b[1;32m' + '[+]' + '\x1b[0m', message.strip())
	def fail(message):
		print('\x1b[1;31m' + '[-]' + '\x1b[0m', message.strip())
	def title(message):
		print('\x1b[1;37m' + message.strip() + '\x1b[0m')

def startInt():
	msg.title("findURL v"+ver)

	start_len = input("Set start URL len : ")

	finish_len = input("Set finish URL len : ")

	_type = input("Witch do you wnat to find? [com/net/kr/io] : ")

	thread = input("Thread setting [1 over] : ")

	ok = input("Do you want to search this range? "+str(start_len)+"~"+str(finish_len)+" [y/n] : ")

	if ok=='y':
		return {'start_len':start_len, 'finish_len':int(finish_len)+1, 'type':str(_type), 'thread':int(thread)}
	else:
		return 'exit'

def ping(host):
	type = str(data['type'])
	msg.info('ping ' + host + '.' + type)
	with open(os.devnull, 'w') as DEVNULL:
		try:
			subprocess.check_call(
				['ping', '-c', '1', '-t', '10', host + '.' + type],
				stdout=DEVNULL,  # suppress output
				stderr=DEVNULL
			)
			return True
		except subprocess.CalledProcessError:
			dnsinfo(host,type)
def dnsinfo(host,type):
	msg.warn('Search Whois DataBase '+host + '.' + type)
	with open(os.devnull, 'w') as DEVNULL:
		try:
			ref = subprocess.check_output(
				['whois', host + '.' + type]
			)
			if len(ref)<2500:
				msg.good(host  + '.' + type + "Can use!")
				with open("./"+ str(type) +".txt", 'a') as f:
					f.write(host  + '.' +  type+'\n')
				f.close()
			else:
				return True
		except subprocess.CalledProcessError:
			return False

def findURL(data):
	array=[]
	for length in range(int(data['start_len']),int(data['finish_len'])): # it isn't reasonable to try a password more than this length
		word = product(ascii_lowercase, repeat=length)
		for attempt in word:
			attempt = ''.join(attempt) # <- Join letters together
			array.append(attempt)
			#print(array)

		pool = ThreadPool(int(data['thread'])) 
		results = pool.map(ping, array)

if __name__ == '__main__':
	data = startInt()
	if data=='exit':
		msg.info('findURL EXIT.')
		sys.exit()
	msg.info("Thread set = "+str(data['thread']))
	findURL(data)
	msg.info("Finish findURL.")
	sys.exit()
