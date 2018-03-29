# githubCrawler
This repo is used to collect the china user stats from the given repository in github.
Now it can collect the stargazers, contributors, forks information. For more information, you can follow the [API reference](http://pygithub.readthedocs.io/en/latest/apis.html) to add more.
Notice that there is the rate limit from Github API, in order to increase the speed, users can utilize multiple github accounts and [slices](http://pygithub.readthedocs.io/en/latest/utilities.html#github.PaginatedList.PaginatedList) to accelerate the crawling process in parallel.

**The github API only support up to 40000 [pagination](https://stackoverflow.com/questions/25265465/why-github-api-gives-me-a-lower-number-stars-of-a-repo) results.**

**Update: Based on the feedback from Github Support team, the [GraphQL API](https://developer.github.com/v4/) may solve this issue. While it's not supported by PyGithub yet.**
## requirements
	$ pip install PyGithub
## How to use it
	$ python crawler.py
