# -*- coding: utf8 -*-
from github import Github
import json
import os
import random
import sys

class Crawler():
  def __init__(self, user, repo, per_page=30, max_retry_times=5):
    self.per_page = per_page
    self.city_country = self.getCityData()
    self.repo_name = repo
    self.user_name = user
    self.max_retry_times = max_retry_times
    self.account = []
    with open('./accounts.txt', 'r') as fr:
      for line in fr:
        self.account.append(line.strip())
    self.chooseOneAccount()

  def chooseOneAccount(self):
    idx = random.randint(0, len(self.account)-1)
    login_id, login_passwd = self.account[idx].split(',')
    print 'choose one github account:', login_id, login_passwd
    self.gh = Github(login_id, login_passwd, per_page=self.per_page)
    self.repo = self.gh.get_user(self.user_name).get_repo(self.repo_name)
 
  def getCityData(self):
    f = open('./cities.json','r')
    data = json.load(f)
    city_country = {}
    for item in data:
      if item['country'] != 'CN': continue
      city_country[item["name"].lower()] = item["country"]
    print 'load city data completed..'
    return city_country


  def parseCollection(self, collection, collection_size, storeUserInfo, log_file, flag, restart_file):
    china_count = 0
    total_valid_count = 0
    total_count = collection_size
    count = 0
    # restart from log file
    restart = 0
    if os.path.exists(restart_file):
      fr_restart = open(restart_file,'r')
      line = fr_restart.readline()
      if line:
        restart, china_count, total_valid_count = [int(i) for i in line.strip().split(',')]
    count = restart * self.per_page
    cur_page = restart

    while True:
      for user in collection.get_page(cur_page):
        if flag == 'fork':
          user = user.owner
        elif flag == 'stargazer' or flag == 'issue':
          # print 'starred_time: ', user.starred_at, user.user.name
          user = user.user
        count += 1
        print 'processed: %d/%d, china user in valid users: %d/%d' % (count, total_count, china_count, total_valid_count)
        # store the progress
        if count % 10 == 0:
          fw_restart = open(restart_file, 'w')
          fw_restart.write('%d,%d,%d' %(int(count/self.per_page), china_count, total_valid_count))
          fw_restart.close()
        location = user.location
        if location is None:continue
        location = location.lower()
        total_valid_count += 1
        check = False
        if location.find('china') >= 0:
          china_count += 1
          check = True
        else:
          token = location.split(',')
          if self.city_country.has_key(token[0]) and self.city_country[token[0]]=='CN':
            china_count += 1
            check = True
        if check and storeUserInfo:
          user_info = '%s##%s##%s##%s##%s\n' % (user.login, user.name, user.email, user.followers, location)
          print user_info
          fw = open(log_file, 'a')
          fw.write(user_info.encode('utf8'))
          fw.close()
      # iterate next page
      cur_page += 1

  def crawlStargazer(self, storeUserInfo):
    print 'start crawl stargazers...'
    retry_times = 0
    while retry_times < self.max_retry_times:
      stargazers = self.repo.get_stargazers_with_dates()
      size = self.repo.stargazers_count
      try:
        self.parseCollection(stargazers, size, storeUserInfo, './stargazer.user', 'stargazer', './stargazer.restart')
      except Exception, e:
        self.chooseOneAccount()
        print 'retry %d and changed the account...' % (retry_times)

  def crawlContributor(self, storeUserInfo):
    print 'start crawl contributor...'
    retry_times = 0
    while retry_times < self.max_retry_times:
      try:
        contributors = self.repo.get_contributors()
        self.parseCollection(contributors, -1, storeUserInfo, './contributor.user', 'contributor', './contributor.restart')
      except Exception, e:
        self.chooseOneAccount()
        print 'retry %d and changed the account...' % (retry_times)

  def crawlForks(self, storeUserInfo):
    print 'start crawl forks...'
    retry_times = 0
    while retry_times < self.max_retry_times:
      try:
        forks = self.repo.get_forks()
        size = self.repo.forks_count
        self.parseCollection(forks, size, storeUserInfo, './forks.user', 'fork', './forks.restart')
      except Exception, e:
        self.chooseOneAccount()
        print 'retry %d and changed the account...' % (retry_times)

  def crawlWatcher(self, storeUserInfo):
    print 'start crawl watcher...'
    retry_times = 0
    while retry_times < self.max_retry_times:
      watchers = self.repo.get_subscribers()
      size = self.repo.subscribers_count
      try:
        self.parseCollection(watchers, size, storeUserInfo, './watcher.user', 'watcher', './watcher.restart')
      except Exception, e:
        self.chooseOneAccount()
        print 'retry %d and changed the account...' % (retry_times)

  def crawlIssue(self, storeUserInfo):
    print 'start crawl issue...'
    retry_times = 0
    while retry_times < self.max_retry_times:
      issues = self.repo.get_issues()
      size = self.repo.open_issues_count
      try:
        self.parseCollection(issues, size, storeUserInfo, './issue.user', 'issue', './issue.restart')
      except Exception, e:
        self.chooseOneAccount()
        print 'retry %d and changed the account...' % (retry_times)



if __name__ == '__main__':
  if len(sys.argv) < 3:
    print 'argv[1]: repo_name (tensorflow or models)'
    print 'argv[2]: option(1:stargazer, 2:contributor, 3:fork, 4:watcher, 5:issue)'
    exit()
  crawler = Crawler('tensorflow', sys.argv[1])
  option = int(sys.argv[2])
  if option == 1:
    crawler.crawlStargazer(True)
  elif option == 2:
    crawler.crawlContributor(True)
  elif option == 3:
    crawler.crawlForks(True)
  elif option == 4:
    crawler.crawlWatcher(True)
  elif option == 5:
    crawler.crawlIssue(True)
  else:
    print 'invalid option'
