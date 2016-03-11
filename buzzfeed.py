#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup
import csv

'''api that are called when scroll down the website'''
#'http://www.buzzfeed.com/index/paging?p=1&r=1&z=4UX9NL&country=in'
#'http://www.buzzfeed.com/index/paging?p=2&r=1&z=4UX9NL&country=in'

def get_count(count):
	'''This function checking the num_of_count of a tag in post if value is not finding then insert empty string'''
	if count:
		return count
	else:
		return ''

def value_check(value):
	'''This function checking the value mention in fieldnames for a post if value is not finding then insert empty string'''
	if value:
		return (value.text).strip('\n').replace('\n',' ')
	else:
		return ''

post_data = []              # post_data is a list which have list type element like [[post_url, post_rresponse],[]] for each post 

for i in range(1,3):
	'''this loop open the website scroll the website while collecting each post url and response'''
	next_url = 'http://www.buzzfeed.com/index/paging?p=' + str(i) +'&r=1&z=4UX9NL&country=in'
	try:
		r = requests.get(next_url)
	except requests.exceptions.ConnectionError:
		r.status_code = "Connection refused"
	soup = BeautifulSoup(r.content)
	title = soup.find('title')
	if title == None or str(title) == '<title>BuzzFeed</title>':
		soup1 = soup.find('ul',{'data-bfa':'@l:Feed;'})
		posts = soup1.find_all('div',{'class':'lede__body'})
		for post in posts:
			href = post.find('a',{'class':'lede__link'})['href']
			if href:
				post_url = 'http://www.buzzfeed.com' +    href 
				response = value_check(post.find('span', {'class':'num'}))
				post_data.append([post_url, response])
	else:
		break  




with open('buzzfeed_data.csv', 'wb') as csvfile:
	fieldnames = ['Title', 'url', 'Response', 'author', 'views', 'Date', 'Time', 'category', 'comment', 'word_count', 'paragraph_count', 'img_count', 'r1_lol', 'r2_heart', 'r3_wtf', 'r4_fail', 'r5_omg', 'r6_win', 'r7_ew', 'r8_cute', 'r9_yaaass', 'r10_heartbroken']
	len(fieldnames)
	writer = csv.writer(csvfile)
	writer.writerow(fieldnames)

	for i, item in enumerate(post_data) :
		post_info = []
		try:
			r = requests.get(item[0])
		except requests.exceptions.ConnectionError:
			r.status_code = "Connection refused"
		
		soup = BeautifulSoup(r.content)

		post_info.append(value_check(soup.find('h1',{'id':'post-title'})).encode('utf-8'))  						# Title
		post_info.append(item[0].encode('utf-8'))																	# url
		post_info.append(item[1].encode('utf-8'))																	# Response
		post_info.append(value_check(soup.find('div',{'class':['user-info-info','byline__body']})).encode('utf-8'))	# Author
		post_info.append(value_check(soup.find('p',{'class':'num views'})).encode('utf-8'))							# views
		post_info.append(value_check(None))																			# Date
		post_info.append(value_check(None))																			# time
		post_info.append(value_check(soup.find('a',{'class':'vertical-label'})).encode('utf-8'))					# category
		post_info.append(value_check(None))																			# comment
		post = soup.find('div',{'id':'buzz_sub_buzz'}) 
		post_info.append(get_count(len(post.text.split())))															# word_count
		post_info.append(get_count(len(post.find_all('p'))))														# para_count
		post_info.append(get_count(len(post.find_all('img'))))  													# img count
		
		
		reaction = soup.find('ul',{'id':'reactions'})
		if reaction:
			post_info.append(value_check(reaction.find('li',{'id':'reaction-lol'})).encode('utf-8'))				# lol
			post_info.append(value_check(reaction.find('li',{'id':'reaction-love'})).encode('utf-8'))				# heart
			post_info.append(value_check(reaction.find('li',{'id':'reaction-wtf'})).encode('utf-8'))				# wtf
			post_info.append(value_check(reaction.find('li',{'id':'reaction-fail'})).encode('utf-8'))				# fail
			post_info.append(value_check(reaction.find('li',{'id':'reaction-omg'})).encode('utf-8'))				# omg
			post_info.append(value_check(reaction.find('li',{'id':'reaction-win'})).encode('utf-8')) 				# win
			post_info.append(value_check(reaction.find('li',{'id':'reaction-ew'})).encode('utf-8'))					# ew
			post_info.append(value_check(reaction.find('li',{'id':'reaction-cute'})).encode('utf-8'))				# cute
			post_info.append(value_check(reaction.find('li',{'id':'reaction-yaaass'})).encode('utf-8'))				# yaaass
			post_info.append(value_check(reaction.find('li',{'id':'reaction-hate'})).encode('utf-8'))				# heartbroken
			
		print post_info
		writer.writerow(post_info)	




'''
requests.exceptions.ConnectionError: HTTPConnectionPool(host='www.buzzfeed.com', port=80): 
Max retries exceeded with url: /genamourbarrett/ban-feelings-ban-them-for-good 
(Caused by NewConnectionError('<requests.packages.urllib3.connection.HTTPConnection object at 0x7fa6ee1a4b50>: 
	Failed to establish a new connection: [Errno -2] Name or service not known',)) 
'''