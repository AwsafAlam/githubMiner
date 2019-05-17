import sys  #for command line argument
# from git import Repo
import os
import shutil
import tempfile
import urllib.parse
from random import randint
import time
import mysql.connector
import requests
import wget
import json
import simplejson
import csv
import math


lang = sys.argv[1]
OUTPUT_FOLDER = "G:/MinedZips/" + lang + "/" #Folder where ZIP files will be stored

query_limit = 5

f = open("Token.txt", "r")
token = f.read()
f.close()
print(token)

headers = {
    'Authorization': 'token ' + token,
}

response = requests.get('https://api.github.com/', headers=headers)

print(response)



if not os.path.exists(OUTPUT_FOLDER):
    os.mkdir(OUTPUT_FOLDER)

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="3985",
  database="miner"
)

mycursor = mydb.cursor()

while 1 > 0:
    sql = "select * from repos WHERE language = %s AND downloaded = 0 ORDER BY RAND() LIMIT %s"
    val = (lang, query_limit, )

    mycursor.execute(sql, val)
    myResult = mycursor.fetchall()

    if len(myResult) < 5:
        print("Not enough links to download")
        break

    #============================================== download

    for entry in myResult:
        print(entry)

        print("url: " + entry[1])

        item = requests.get(entry[1], headers=headers).json()

        if len(item) < 6:   #for invalid requests
            print("not found")
            continue

        # Obtain user and repository names
        user = item['owner']['login']
        repository = item['name']

        # Download the zip file of the current project
        print("Downloading repository '%s' from user '%s' ..." % (repository, user))
        url = item['clone_url']
        fileToDownload = url[0:len(url) - 4] + "/archive/master.zip"
        fileName = item['full_name'] + ".zip"
        jsonName = item['full_name'] + ".json"

        if not os.path.exists(OUTPUT_FOLDER+user):
            os.mkdir(OUTPUT_FOLDER+user)

        wget.download(fileToDownload, OUTPUT_FOLDER + fileName)

        with open(OUTPUT_FOLDER + jsonName, "w") as jsonFile:
            json.dump(item, jsonFile)

        # print(user)
        # print(repository)

        sql = "UPDATE repos SET downloaded = 1 WHERE id = %s LIMIT 5"
        val = (str(entry[0]), )

        mycursor.execute(sql, val)
        mydb.commit()





    time.sleep(1)