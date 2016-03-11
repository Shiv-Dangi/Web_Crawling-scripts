#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup
import json
import csv
import ast


# Collect all level1 url from scoopwhoop page.
# level1 are the api calls that called when scroll down the webstesite.
level1_url = ["http://www.scoopwhoop.com/api/v1/homepage/desktop/","http://www.scoopwhoop.com/api/v1/all/?offset=0",]

for i in range(200):
	last_url = level1_url[-1]
	r = requests.get(last_url)
	data = json.loads(r.content)          # output = Dictionary
	if data["next_offset"] != -1:
		next_url = last_url[:last_url.index("=")]
		next_url = next_url + "=" + str(data["next_offset"])
		level1_url.append(next_url)
	else:
		break



# Now collect url's with respect to each post published on the site. one url for post data and one url for facebook share data
# and put these in a dictionary {"key=slug":value=["url for post data", "url for facebook data"]}
# level2 are the api calls that called when open a particular post
level2_url = {}

for i in range(len(level1_url)):
	r = requests.get(level1_url[i])
	data_level1url = json.loads(r.content)   		# output = Dictionary
	dataof_level1url = data_level1url['data']  		# output = list
	for j in range(len(dataof_level1url)):
		unit_element = dataof_level1url[j] 			# output = Dictionary
		if 'slug' in unit_element.keys():  			# Check wheter unit element of a valid post
			slug_field = unit_element['slug']
			if (slug_field not in level2_url):		# Check if post url's is allready entered in dictionary
				data_url = "http://www.scoopwhoop.com/api/v1/" + slug_field
				fbdata_url = "https://graph.facebook.com/?id=http://scoopwhoop.com/" + slug_field + "/&callback=facebookCallback"
				level2_url[slug_field] = [data_url, fbdata_url]


# function for checking if any required valve related to post is not getting.
def valuecheck(count):
	if count:
		return count
	else:
		return 0



# Generate a csv file that contain following information for a particular Post
# Title,Published_date,url,Facebook_Share.Facebook_comment, Author, Category, word_count, Paragraph_count, image_count 

with open('scoopwhoop_data.csv', 'wb') as csvfile:
	fieldnames = ['Author', 'category', 'Title', 'Published_date', 'url', 'Facebook_Share', 'Facebook_comment', 'word_count', 'Paragraphs_count', 'img_count', ]
	writer = csv.writer(csvfile)
	writer.writerow(fieldnames)

	author_key = ['display_name']
	category_keys = ['category_display']
	requiredinfo_keys = ['title', 'pub_date', 'slug']
	requiredfb_keys = ['shares', 'comments']

	for slug in level2_url:
		r = requests.get(level2_url[slug][0]).json()
		author = r['userData'][0]
		author = [author[key].encode('utf-8') if key in author else '' for key in author_key ]				# Author
		categories = ''
		category = r['data']['category']
		for c in category:
			categories = categories + str([c[key].encode('utf-8') if key in c else '' for key in category_keys])			# Category
		post_data = r['data']
		post_data = [post_data[key].encode('utf-8') if key in post_data else '' for key in requiredinfo_keys]		# title, Published_date, url
		post_data[2] = "http://scoopwhoop.com/" + post_data[2]
		 
		content = r['data']['article_content']
		soup = BeautifulSoup(content)
		img_count = valuecheck(len(soup.find_all('img')))																# no. of images
		para_count = valuecheck(len(soup.find_all('p')))																# no. of Paragraphs
		word_count = valuecheck(len((soup.text).split()))																# no. of words
		
		try:
			r = requests.get(level2_url[slug][1]).content
			fb_data_string = r[21:-1]
			fb_data = ast.literal_eval(fb_data_string)
			fb_data = [str(fb_data[key]).encode('utf-8') if key in fb_data else '' for key in requiredfb_keys ]		# fb_share, fb_comment
		except requests.exceptions.ConnectionError as e:
			print "requests.exceptions.ConnectionError"
			fb_data = ['','']
		except ValueError:
			print "ValueError"
			fb_data = ['','']
		except:
			print "Unexpected error:"
			fb_data = ['','']

		
		
		final_data = author + [categories] + post_data + fb_data + [word_count, para_count, img_count,]
		writer.writerow(final_data)




		
	