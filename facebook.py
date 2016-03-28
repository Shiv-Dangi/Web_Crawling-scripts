#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup
import json

def request_handler(url):
	'''this function take url from parameter call them and return a response.'''
	try:
		response = (requests.get(url)).content
		return response
	except requests.exceptions.ConnectionError as e:
		print "requests.exceptions.ConnectionError"
		return ''
	except:
		print "Unexpected error:"
		return ''		
		
#Taking input url of user_facebook page
# start_url = raw_input('Enter the url: ')
start_url = 'https://www.facebook.com/tinyowlapp'


#collecting url of all possible subpages(like : Timeline, about, photos, review, likes, videos, events, notes)
# https://www.facebook.com/flipkart/timeline?ref=page_internal
timeline_page = start_url + "/timeline?ref=page_internal"
about_page = start_url + "/info/?tab=page_info"
review_page = start_url + "/reviews?ref=page_internal"
likes_page = start_url + "/likes?ref=page_internal"
videos_page = start_url + "/videos?ref=page_internal"
events_page = start_url + "/events?ref=page_internal"
notes_page = start_url + "/notes?ref=page_internal"
photos_page = start_url + "/photos_stream?ref=page_internal"


def value_checking(count):
	'''this function check if any fatched_info is not avaliable on html page then put empty_string on that place'''
	if count:
		return count
	else:
		return ''


def review_info(review_url):
	''' this function return the reviews information of the page'''
	response = request_handler(review_url)
	if response:
		soup = BeautifulSoup(response)
		overall_rating = value_checking(soup.find("div",{"class":"_4uyj"}).contents[0].text)
		total_review = value_checking(soup.find("div",{"class":"_4uyj"}).contents[1].text)
		five_star = value_checking(soup.find("div",{"id":"u_0_c"}).contents[1].text)
		four_star = value_checking(soup.find("div",{"id":"u_0_d"}).contents[1].text)
		three_star = value_checking(soup.find("div",{"id":"u_0_e"}).contents[1].text)
		two_star = value_checking(soup.find("div",{"id":"u_0_f"}).contents[1].text)
		one_star = value_checking(soup.find("div",{"id":"u_0_g"}).contents[1].text)

		reviews = soup.find_all('div',{'class':'_4-u2 mbm _5jmm _5pat _5v3q _4-u8'})

		for review in reviews:
			user_name = review.find('span',{'class':'fwb'}).contents[0].text
			user_fb_page = review.find('span',{'class':'fwb'}).contents[0].get("href")
			rate_by_user = review.find('u').text
			date = review.find('abbr',{'class':'_5ptz'}).get("title")
			describtion = review.find('div',{'class':'_5pbx userContent'}).text
			
			print user_name, user_fb_page, rate_by_user, date, describtion

		print overall_rating, total_review, five_star, four_star, three_star, two_star, one_star



review_info(review_page)
