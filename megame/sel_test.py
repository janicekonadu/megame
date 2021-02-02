from selenium import webdriver
from watson_developer_cloud import PersonalityInsightsV3
from os.path import join, dirname
import cv2
import numpy as np
import pytesseract
import re
import webbrowser

import json


from bs4 import BeautifulSoup
import requests
from models import Resume, Job, Education, Social, Project 


def getMemberLst(lst):

	empty = []

	for i in lst:

		b = i.text
		c = b.split()

		if b.count(" ") == 0:			
			empty.append(''.join(letter for letter in b.lower() if ('a' <= letter <= 'z' or letter == ' ') ).capitalize())
		else: 
			empty.append(' '.join(c))

	return empty


def getWorkData(): 
 
	options = webdriver.ChromeOptions()
	options.add_argument('--ignore-certificate-errors')
	options.add_argument("--test-type")

	options.add_argument("user-data-dir=[PATH]")

	#options.binary_location = "/usr/bin/chromium"
	driver = webdriver.Chrome([CHROMEDRIVER PATH] , chrome_options=options)

	'''-------------------------------------------------------------
	    LOGINS & SNAPSHOTS
	--------------------------------------------------------------'''


	#Facebook

	driver.get(fb_url)
	while not(fb_url in driver.current_url):
	    print("FB Login!")

	driver.execute_script("window.scrollTo(0, 500);")

	elem1 = driver.execute_script("return document.getElementsByTagName('span')")
	elem2 = driver.execute_script("return document.getElementsByTagName('h4')")
	imgs = driver.execute_script("return document.getElementsByTagName('img')")

	driver.execute_script("document.body.innerHTML.replace('·', '_')");

	for item in elem1:
		driver.execute_script("arguments[0].setAttribute('style', 'font-size:20pt')", item)
	for item in elem2:
		driver.execute_script("arguments[0].setAttribute('style', 'font-size:20pt')", item)
	for item in imgs: 
		driver.execute_script("arguments[0].setAttribute('style', 'display:none')", item)

	driver.save_screenshot("img/fb_screenshot.png")

	'''-------------------------------------------------------------
	    IMG MANIPULATION & TEXT EXTRACTION
	--------------------------------------------------------------'''
	while True:

		fb_img = "C:/megame/img/fb_screenshot.png"

		img = cv2.imread(fb_img)

		w, h, c = img.shape

		img = img[0:(w), 0:(h//2)] 

		cv2.imshow('half', img)

		# Convert to gray
		img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		cv2.imshow('gray', img)


		# Apply threshold to get image with only b&w (binarization)
		img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

		cv2.imshow('threshold', img)


		if cv2.waitKey(1) == 27:
		    cv2.destroyAllWindows()
		    break

	res = pytesseract.image_to_string(img).replace("NJIT\n\n", "NJIT\n").replace("16 Computer","16\nComputer")

	resu = res.replace("\"", "")

	# .replace("Computer", "\nComputer")

	result = resu.replace("* ","\n").replace("\"","")

	print(res)

	'''-------------------------------------------------------------
	    TEXT MANIPULATION & PARSING
	--------------------------------------------------------------'''

	months = [" January", " Februrary", " March", " April", " May", " June", " July", " August", " September", " October", " November" " December"]

	sections = re.split("WORK|EDUCATION|CURRENT", result)

	# print(sections)

	work = sections[1].split("\n\n")[1:]
	education = sections[2].split("\n\n")[1:]


	# print("WORK\n___________\n")
	# for i in work:
	# 	print(i)
	# 	print("\n\n")


	# print("EXPERIENCE\n___________\n")
	# for i in education:
	# 	print(i)
	# 	print("\n\n")

	# print(work)
	# print("\n\n")
	# print(education)


	#print("----------------------")

	driver.close()


def createMessage():
		message = """
		<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
		<html>
		<head>

			<title>Jonathan Doe | Web Designer, Director | name@yourdomain.com</title>
			<meta http-equiv="content-type" content="text/html; charset=utf-8" />

			<meta name="keywords" content="" />
			<meta name="description" content="" />

			<link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.7.0/build/reset-fonts-grids/reset-fonts-grids.css" media="all" /> 
			<link rel="stylesheet" type="text/css" href="resume.css" media="all" />

		</head>
		<body>

		<div id="doc2" class="yui-t7">
			<div id="inner">
			
				<div id="hd">
					<div class="yui-gc">
						<div class="yui-u first">
							<h1>
		"""
		message += resume.getName()


		message += "</h1><h2>"

		message += resume.getTitle()

		message += """</h2>
						</div>

					</div><!--// .yui-gc -->
				</div><!--// hd -->
				

				<div id="bd">
					<div id="yui-main">
						<div class="yui-b">

							<div class="yui-gf">
								<div class="yui-u first">
									<h2>Education</h2>
								</div>
								<div class="yui-u">"""

		eduLst = resume.get("edu") 

		for i in eduLst:
			message += "<p class=\"\">" + i + "</p>"

		message += """"</div>
							</div><!--// .yui-gf -->

							<div class="yui-gf">
								<div class="yui-u first">
									<h2>Technical Skills</h2>
								</div>
								<div class="yui-u">"""


		skillLst = resume.get("skills")

		count = 0
		for j in skillLst:
			if count%3 == 0:
				message += """<ul class="talent">"""

			message += 	"<li class=\"last\">" + i + "</li>"

			if count%3 == 0 and count != 0:
				message += """</ul>"""


		message +=""" 							
								</div>
							</div><!--// .yui-gf-->



							<div class="yui-gf">
			
								<div class="yui-u first">
									<h2>Work Experience</h2>
								</div><!--// .yui-u -->

								<div class="yui-u"> """


		jobLst = resume.get("jobs")						

		for k in jobLst:
				message += "<div class=\"job\">" + k + "</div>"

		message += """
								</div><!--// .yui-u -->
							</div><!--// .yui-gf -->


							<div class="yui-gf last">
								<div class="yui-u first">
									<h2>Projects</h2>
								</div>
								<div class="yui-u"> """


		projLst = resume.get("projects")						

		for l in projLst:
				message += "<div >" + l + "</div> <br/><br/>"


		message += """ 							
								</div>
							</div><!--// .yui-gf -->


						</div><!--// .yui-b -->
					</div><!--// yui-main -->
				</div><!--// bd -->

			</div><!-- // inner -->


		</div><!--// doc -->


		</body>
		</html> """

		return message



resume = Resume("Janice Konadu", "Full-Stack Developer", "[NUMBER]", "[EMAIL]")


fb_url = "[FACEBOOK URL]"
dvp_url = "[DEVPOST URL]"
gh_url = "[GITHUB URL]"



dvp_page = requests.get(dvp_url)
dp_soup = BeautifulSoup(dvp_page.content, 'html.parser')

# prj = dp_soup.find_all('h5')
# dvpLst = getMemberLst(prj)


gh_page = requests.get(gh_url)
gh_soup = BeautifulSoup(gh_page.content, 'html.parser')

g_prj = gh_soup.find_all('span', class_="js-repo")[1:]
prj_Lst = getMemberLst(g_prj) 

print(prj_Lst)

g_med = gh_soup.find_all('p', class_="mb-0 f6 text-gray")[1:]
med_Lst = getMemberLst(g_med)


g_desc = gh_soup.find_all('p', class_="pinned-item-desc text-gray text-small d-block mt-2 mb-3")[1:]
desc_Lst = getMemberLst(g_desc)


for i in range(len(prj_Lst)):

	name = prj_Lst[i]
	medium = med_Lst[i]
	desc = desc_Lst[i]

	project = Project(name, medium, desc)

	resume.addProject(project)

for in 


soc = gh_soup.find_all('span', class_="cp-tag recognized-tag")
socials = getMemberLst(soc)

# REMEMBER TO SPLIT SECOND COLUMN BY * AND " AND “ orrrrrr BY EVERYTHING THAT IS NOT AN ALPHANUMERICAL VALUE

for i in socials:
	resume.addSocial(i)




'''-------------------------------------------------------------------------------------
HTML MANAGEMENT
-------------------------------------------------------------------------------------'''


# Creates file, uses array data

f = open('megame.html','w')

message = createMessage()

# print (message)

f.write(message)
f.close()

# Opens browser

filename = '[MEGAME HTML PATH]' + 'megame.html'

webbrowser.open_new_tab(filename)



'''------------------------------------------------------------------------------------
IBM PERSONALITY INSOGHTS INCORPORATION
--------------------------------------------------------------------------------------'''

api_key = "[SECRET KEY]"
ibm_url = "https://gateway.watsonplatform.net/personality-insights/api"

personality_insights = PersonalityInsightsV3(
    version='2017-10-13',
    iam_apikey=api_key,
    url=ibm_url
)

with open(join(dirname(__file__), 'industryprofiles.txt')) as profile_txt:
    ind_profile = personality_insights.profile(
        profile_txt.read(),
        accept='application/json',
        content_type='text/plain',
        consumption_preferences=True,
        raw_scores=True
    ).get_result()
ind_data = json.dumps(ind_profile, indent=2).split()

print("********************************************************************")

with open(join(dirname(__file__), 'megame.html')) as profile_html:
    usr_profile = personality_insights.profile(
        profile_html.read(),
        accept='application/json',
        content_type='text/html',
        consumption_preferences=True,
        raw_scores=True
    ).get_result()
usr_data = json.dumps(usr_profile, indent=2).split()


trunc_Lst = np.setdiff1d(ind_data,usr_data)

score = ((len(ind_data) - len(trunc_Lst)) / len(ind_data)) * 10

print(str(score) + "/10")

