#!/usr/bin/env python

import requests #install from: http://docs.python-requests.org/en/master/

#Replace the following string value with your valid X-RapidAPI-Key.
Your_X_RapidAPI_Key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx";

#The query parameters: (update according to your search query)
q = "apple" #the search query
pageNumber = 1 #the number of requested page
pageSize = 10 #the size of a page
autoCorrect = True #autoCorrectspelling
safeSearch = False #filter results for adult content

response=requests.get("https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/Search/ImageSearchAPI?q={}&pageNumber={}&pageSize={}&autocorrect={}&safeSearch={}".format(q, pageNumber, pageSize, autoCorrect,safeSearch),
headers={
"X-RapidAPI-Key": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
}
).json()

#Get the numer of items returned
totalCount = response["totalCount"];

#Go over each resulting item
for webPage in response["value"]:
    # Get the image
    imageUrl = webPage["url"]
    imageHeight = webPage["height"]
    imageWidth = webPage["width"]

    # Get the image thumbail
    thumbnail = webPage["thumbnail"]
    print thumbnail
    thumbnailHeight = webPage["thumbnailHeight"]
    thumbnailWidth = webPage["thumbnailWidth"]

    #An example: Output the webpage url, height and width:
    print("imageUrl: %s imageHeight: %s imageWidth: %s" % (imageUrl, imageHeight, imageWidth))
