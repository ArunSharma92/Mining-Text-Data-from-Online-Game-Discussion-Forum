# Mining-Text-Data-from-Online-Game-Discussion-Forum
import urllib2
from bs4 import BeautifulSoup
from bs4 import Comment

#Taking the user Input in form of url
print "Enter the link : "    
url = raw_input();
f = urllib2.urlopen(url)

soup = BeautifulSoup(f, "lxml")

title = soup.find('div' , attrs={"class":"tcat clearfix"})

filename = ""+title.find('div' , attrs={"class":"left"}).text.strip()+".txt"

try:
	file1 = open(filename,"w")
except IOError:
	print "The name of the forum topic is invalid to be kept as a file name"
	print "Please enter a valid file name"
	filename = raw_input()+".txt"
	file1 = open(filename,"w")
#file2 = open("posts.txt","w")

posts = soup.body.find('div' ,attrs={"id":"posts"})
#file2.write(str(posts))

p = soup.find('li' , attrs={"class":"pageof"}).text.split(" ")
pages = int(p[3])

print "Number of pages found : " + str(pages)
#Collecting Data by mining text through all the pages in the forum
#Collecting all the attributes that are required
for page in range(0,pages):

	print "Collecting posts from page #" + str(page+1) 

	if(page!=1):
		new_url = url+"&page="+str(page+1)
		f = urllib2.urlopen(new_url)
		soup = BeautifulSoup(f, "lxml")

	comments = soup.find_all(string=lambda text:isinstance(text,Comment))

	post_ids = []
	for c in comments:
		c = c.strip()
		try:
			if(c.index("post") == 0):
				post_ids.append(c.lstrip("post #"))
		except ValueError:
			continue

	for ids in post_ids:
		username = soup.body.find('div' ,attrs={"class" : "postbit-details-username", "id":"postmenu_"+ids})
		message = soup.body.find('div' ,attrs={"class" : "post", "id":"post_message_"+ids})
		original_post = message.find('blockquote',attrs={"class" : "quote quoted"})
		try:
			file1.write("User : "+username.a.text.strip().encode('ascii','ignore')+"\n")
		except AttributeError:
			file1.write("User : "+username.text.strip().encode('ascii','ignore')+"\n")
		if(original_post != None):
			file1.write("-----------------------------------------------------------------------------------------------\n")
			for line in (original_post.text.strip().encode('ascii','ignore')).split('\n'):
				line = line.strip()
				if(line == ""):
					continue
				file1.write(line)
				file1.write("\n")
			file1.write("-----------------------------------------------------------------------------------------------\n")
			message.blockquote.decompose()
		for line in (message.text.strip().encode('ascii','ignore')).split('\n'):
			line = line.strip()
			if(line == ""):
				continue
			file1.write(line)
			file1.write("\n")
				
		file1.write("===============================================================================================\n")
# Getting the mined text in a file and assigning the file a name		
print "All the posts of the given link are stored in '"+filename+"' file"
