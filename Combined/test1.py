from github import Github
import urllib.request
import os

g = Github("abhik1505040", "1011215995165502") #username, password

#for a specific repo
base_url = "https://raw.githubusercontent.com/"
repo_url = "AwsafAlam/githubMiner/master/"
repo = g.get_repo("AwsafAlam/githubMiner")
parent_dir = "D:\\" + repo_url.replace("/", "\\")
#os.makedirs(parent_dir)
contents = repo.get_contents("")
while len(contents) >= 1:
    file_content = contents.pop(0)
    print(file_content)
    if file_content.type == "dir":
        #os.makedirs(parent_dir + file_content.path.replace("/", "\\") )
        contents.extend(repo.get_contents(file_content.path))
    else:
        path = file_content.path
        # if path.find(".txt", -4) != -1: # .cpp for cpp file
        #     urllib.request.urlretrieve(base_url+repo_url+path, parent_dir + path.replace("/", "\\") )


#urllib.request.urlretrieve('https://raw.githubusercontent.com/PyGithub/PyGithub/master/tests/ReplayData/AuthenticatedUser.testAttributes.txt',"D:\\ok.txt")