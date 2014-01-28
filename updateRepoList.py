#!/usr/bin/env python

import getpass
import sys
from collections import OrderedDict

from github_acadwf import addPyGithubToPath
from github_acadwf import getenvOrDie

addPyGithubToPath()

from github import Github
from github import GithubException


class RepoListing(object):
    def __init__(self, name, url):
        self.name = name
        self.url = url
    
    def getName(self):
        return self.name
    
    def getUrl(self):
        return self.url



GHA_GITHUB_ORG = getenvOrDie("GHA_GITHUB_ORG",
                        "Error: please set GHA_GITHUB_ORG to name of github organization for the course, e.g. UCSB-CS56-W14")

# Authenticate to github.com and create PyGithub "Github" object
username = raw_input("Github Username:")
pw = getpass.getpass()
g = Github(username, pw)
org = g.get_organization(GHA_GITHUB_ORG)

# Use the PyGithub Github object g to do whatever you want,
# for example, listing all your own repos (user is whichever user authenticated)


projectCategories = dict()
for repo in org.get_repos():
    repoName = repo.name
    repoUrl = repo.html_url
    fields = repoName.split('-', 2)
    #(prefix, category, name) = repoName.split('-', 2)
    if fields[0] == "cs56" and len(fields) >= 3:
        repoCategory = fields[1].capitalize()
        repoName = fields[2]
        if projectCategories.get(repoCategory, "") != "":
            projectCategories[repoCategory].append(RepoListing(repoName, repoUrl))
        else:
            projectCategories[repoCategory] = [RepoListing(repoName, repoUrl),]
    
alphabeticalCategories = OrderedDict(sorted(projectCategories.items(), key=lambda repoCategory: repoCategory[0]))
outputFile = open('AllRepos.md', 'w')
outputFile.write('# ' + 'CategoryList\n')
for repoCategory, repoListings in alphabeticalCategories.iteritems():
    outputFile.write('## ' + repoCategory + '\n')
    repoListings.sort(key=lambda repoListing: repoListing.name)
    for repoListing in repoListings:
        outputFile.write('* ' + '[' + repoListing.name + '](' + repoListing.url + ')\n')
    
