# This is a python script to extract media attributes from VAST xml files
# Media attributes collected are : bitrate, width, height, delivery, type, link of video
# Constraint: Collect media attributes with highest bitrate from an xml file
#
# The script traverses through all sub-folders of 'arizona', finds .xml files and 
# appends to a DataFrame, then exports DataFrame to a .csv file
# Necessary conditions for the script to compile: 
# 1. The 'arizona' folder needs to be in the current working directory
# 2. Tools need to be installed: BeautifulSoup, pandas, os 
#
# Output: output.csv in the current working directory
# Author: Saveri Pal
# Last edit: April 23, 2019
# ------------------------------------------------------------------------------------------

from bs4 import BeautifulSoup
import pandas as pd
import os

# Creates empty DataFrame with column names
df = pd.DataFrame(columns=['Bitrate','Width','Height','Type','Delivery','Link'])
count = 0

# Start exploring all folders from a given start folder to look for XML files
for (dirname, dirs, files) in os.walk('./arizona'):
	for filename in files:
		if filename.endswith('.xml'):
			count = count + 1

			delivery = ""
			ttype = ""
			bitrate = 0
			width = 0
			height = 0
			link = ""

			# Read the XML file
			f = open(os.path.join(dirname,filename), "r")
			contents = f.read()
			soup = BeautifulSoup(contents,'xml')

			# Gets all tags named MediaFiles inside this XML file
			media = soup.find_all('MediaFile')

			# Checks all MediaFiles one-by-one and stores attributes of the one w/ highest bitrate 
			for i in range (0, len(media)):
				if media[i].get('bitrate') != None:
					b = int(media[i].get('bitrate'))
					if b  > bitrate:
						bitrate = b
						delivery = media[i].get('delivery')
						ttype = media[i].get('type')
						width = int(media[i].get('width'))
						height = int(media[i].get('height'))
						link = media[i].get_text()
		

		# Append new row of data to data frame
		df = df.append({'Bitrate':bitrate,'Width':width,'Height':height,'Type':ttype,'Delivery':delivery,'Link':link}, ignore_index= True)

#print(df)
#print("no of files is :"+ str(count))

# Export DataFrame to csv
df.to_csv("output.csv")




