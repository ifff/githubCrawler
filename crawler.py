from github import Github
import json

class Crawler():
  def __init__(self, login_id, login_passwd, user, repo):
    self.gh = Github(login_id, login_passwd)
    self.city_country = self.getCityData()
    self.repo = self.gh.get_user(user).get_repo(repo)
 
  def getCityData(self):
    f = open('./cities.json','r')
    data = json.load(f)
    city_country = {}
    for item in data:
      city_country[item["name"].lower()] = item["country"]
    print 'load city data completed..'
    return city_country


  def parseCollection(self, collection, collection_size, storeUserInfo, log_file, isForks):
    china_count = 0
    total_valid_count = 0
    total_count = collection_size
    count = 0
    fw = open(log_file, 'a')
    for user in collection:
      if isForks:
        user = user.owner
      count += 1
      print 'processed: %d/%d, china user in valid users: %d/%d' % (count, total_count, china_count, total_valid_count)
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
        fw.write(user_info)

    print '%d,%d,%d' % (china_count, total_valid_count, total_count)


  def crawlStargazer(self, storeUserInfo):
    stargazers = self.repo.get_stargazers()
    size = self.repo.stargazers_count
    self.parseCollection(stargazers, size, True, './stargazer.user', False)

  def crawlContributor(self, storeUserInfo):
    contributors = self.repo.get_contributors()
    self.parseCollection(contributors, -1, True, './contributor.user', False)

  def crawlForks(self, storeUserInfo):
    forks = self.repo.get_forks()
    size = self.repo.forks_count
    self.parseCollection(forks, size, True, './forks.user', True)


if __name__ == '__main__':
  crawler = Crawler('testaccount135', 'testaccount123', 'tensorflow', 'tensorflow')
  crawler.crawlStargazer(False)
  #crawler.crawlContributor(False)
  #crawler.crawlForks(True)
