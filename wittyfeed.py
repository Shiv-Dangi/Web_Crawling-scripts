#!/usr/bin/env python
import requests
import csv
from bs4 import BeautifulSoup

url = "http://www.wittyfeed.com/story"
single_post_urls = []
headers = {'X-Requested-With':'XMLHttpRequest'}

r = requests.get(url)
soup = BeautifulSoup(r.content)
single_post_div = soup.find_all("div", {"class":"home_story_title"})
for item in single_post_div:
		next_post_url = item.contents[1].find("a").get("href")
		if next_post_url not in single_post_urls:
			single_post_urls.append(next_post_url)

for i in range(18,20000,12):
	next_url = 'http://www.wittyfeed.com/story/load_more_stories/' + str(i) + '/' + str(0)
	r =  requests.get(next_url, headers=headers)
	if len(r.content) == 1:
		break
	else:
		soup = BeautifulSoup(r.content)
		single_post_div = soup.find_all("div", {"class":"home_story_title"})
		for item in single_post_div:
				next_post_url = item.contents[1].find("a").get("href")
				if next_post_url not in single_post_urls:
					single_post_urls.append(next_post_url)



# Generate a csv file that contain following information for a particular Post
# url, Title, author, views, num_of_images, Published_date, category, num_of_Share

with open('wittyfeed_data.csv', 'wb') as csvfile:
	fieldnames = ['url', 'Title', 'author', 'views', 'num_of_images', 'Published_date', 'category', 'num_of_Share', 'word_count', 'num_of_paragraph']
	writer = csv.writer(csvfile)
	writer.writerow(fieldnames)

	for link in single_post_urls:
		story_id = link.split('/')[4]                       														# for getting view of the post 
		r = requests.get(link)
		soup = BeautifulSoup(r.content)
		post_data = []
		post_data.append(link.encode('utf-8'))    																	# url of the post
		post_data.append((soup.find("div", {"class":"story_title_full"}).contents[1].text).encode('utf-8'))   		# Title of the post
		post_data.append((soup.find("div",{"class":"storyteller_ImgOnMobile"}).contents[3].text).encode('utf-8')) 	# Author of the post
		view = requests.get('http://stats.wittyfeed.com/get_view_count/'+ str(story_id))
		post_data.append((view.content).strip())																	# view on the post
		post_data.append((soup.find("ul",{"class":"StoryMeta_ViewImg"}).contents[3].text).encode('utf-8'))			# num of images
		post_data.append((soup.find("ul",{"class":"story_meta_date_cate"}).contents[1].text).encode('utf-8'))		# Published_date
		post_data.append((soup.find("ul",{"class":"story_meta_date_cate"}).contents[3].text).encode('utf-8'))		# category
		share = requests.get("http://stats.wittyfeed.com/share_count/"+ link)
		post_data.append((share.content).strip())																	# num of share
		post_data.append(len(soup.find('div',{'class':'story_description'}).text))									# no. of words
		ptags = soup.find('div',{'class':'story_description'})
		post_data.append( len(ptags.find_all('p')))																	# no. of paragraph
		writer.writerow(post_data)
