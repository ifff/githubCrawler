# githubCrawler
This repo is used to collect the china user stats from the given repository in github.
Now it can collect the stargazers, contributors, forks information. For more information, you can follow the [API reference](http://pygithub.readthedocs.io/en/latest/apis.html) to add more.
Notice that there is the rate limit from Github API, in order to increase the speed, users can utilize multiple github accounts and [slices](http://pygithub.readthedocs.io/en/latest/utilities.html#github.PaginatedList.PaginatedList) to accelerate the crawling process in parallel.
## requirements
pip install PyGithub
## How to use it
python crawler.py
