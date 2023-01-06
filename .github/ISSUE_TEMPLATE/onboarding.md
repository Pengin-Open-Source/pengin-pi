---
name: Onboarding
about: Assignee to complete all onboarding tasks and resolve ticket when done.
title: "[ONBOARDING]"
labels: good first issue
assignees: ''

---

Proposed altered onboarding:

# Onboarding

**If you are stuck on any part of this ask for help in the discord server and move on to the next part while you are waiting for help.**

## Pre-Setup
- [ ] Sign offer letter and contracts and follow filing instructions
- [ ] Request access to team share drives
- [ ] Request access to team calendar
- [ ] Request access to git repos and accept invites
- [ ] Request access to team Discord servers and accept invites

## IDE Setup
- [ ] [Install VSCode](https://code.visualstudio.com/download) or preferred IDE
- [ ] [Install Docker](https://docs.docker.com/get-docker/)
- [ ] [Install AWScli](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- [ ] [Setup GitHub SSH certificate](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)
- [ ] [Setup AWS credentials](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html)

## Python Training
**Complete at least one of these if you do not know Python:**
- [ ] [Python - Official tutorial (text)](https://docs.python.org/3/tutorial/index.html)
- [ ] [Python - Humorous (video series)](https://www.youtube.com/watch?v=HBxCHonP6Ro&list=PL6gx4Cwl9DGAcbMi1sH6oAMk4JHw91mC_)
- [ ] [Python - In depth (video series)](https://www.youtube.com/playlist?list=PL-osiE80TeTt2d9bfVyTiXJA-UTHn6WwU)

## Flask 
**If you have previous back-end framework experience skip this section and just read through the Flask documentation.**
- [ ] [If you have no web-tech (HTML, CSS, HTTP) experience at all then work through this tutorial ](https://developer.mozilla.org/en-US/docs/Learn/Getting_started_with_the_web)
- [ ] Find a suitable youtube tutorial for web-tech (HTML, CSS, HTTP) if you do not want to do the text tutorial above.
- [ ] [Flask (video series)](https://www.youtube.com/watch?v=7M1MaAPWnYg&list=PLB5jA40tNf3vX6Ue_ud64DDRVSryHHr1h)
- [ ] [Official Flask tutorial (text)](https://flask.palletsprojects.com/en/2.2.x/tutorial/)
- [ ] [SQLalchemy tutorial](https://docs.sqlalchemy.org/en/14/tutorial/index.html)
- [ ]  Find a suitable youtube tutorial if you do not want to do the text tutorial above.
- [ ] [Flask-SQLalchemy tutorial](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/quickstart/)
- [ ]  Find a suitable youtube tutorial if you do not want to do the text tutorial above.
- [ ] Create your own basic CRUD flask app using Jinja templates and SQLite with SQLalchemy from scratch:
   - The database should just use one table and model (Users) which will have the users name and email. 
   - A main page that shows the user's names and emails in a list and has buttons that delete users from the database.
   - A create page in which you can create new users in the database.
   - An update page in which you can edit users in the database.
   - Do not directly copy and change a tutorial for this (although you can do a tutorial that is similar first then try to build this yourself). The idea is to get you used to googling and reading documentation to figure out how to solve problems.
   - Feel free to ask for help in the server while doing this if you are not able to find the answer from googling.

## Git Training
- [ ] [If you do not know how to use git or do not feel confident then complete this](https://www.w3schools.com/git/default.asp?remote=github)

## Post IDE Setup
- [ ] [Clone Pengin-Pie repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)
- [ ] [Create new branch and push minor changes to it](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-branches-in-your-repository/viewing-branches-in-your-repository)
    - Branch off from any other branch and call it "yourname-test".
- [ ] [Run Flask App](https://docs.google.com/document/d/1O0UOZmFUHU6VutuDkUhn0ULgZ-tqm87aoNwDc6C8M1I/)
- [ ] Play around with the Pengin-pie repository(dev branch not main branch) and figure out how the application works.

**Once you reach this point you should be able to take on issues and work on the project.**

## Git workflow
- For this project we are working from the dev branch in the repository. 
-  **Never push to the main, dev  or issue branches!** 
- From the dev branch we branch off into issue branches in the following format: "issue number"-"issue title".
-  From these branches _you_ will then branch off into your own branch in this format: "issue number"-"issue title"-"developer's name".
-  An example of this would be "165-calendar" for the calendar issue branch which you enter with: `git checkout 165-calendar`.
- Once you are in the issue branch you then branch off into your own branch with:   `git branch 165-calendar-first-last ` (replace first and last with your first and last names).
- You then enter your own branch `git checkout 165-calendar-first-last `  and start working on your issue! 
- Once you have finished working on your issue then on the github website submit a pull request(PR) for merging into the issue branch. In this case you would submit a PR to merge "165-calendar-first-last" into "165-calendar".
- This PR will then be checked and feedback given to fix any issues before it can be merged.
- Once there are no issues left the PR will be merged!

## DevOps Training
- [ ] [Run Flask App in NginX](https://unit.nginx.org/howto/flask/)
- [ ] [Run Flask App in Docker](https://blog.logrocket.com/build-deploy-flask-app-using-docker/)
- [ ] [Run Flask App in NginX+Docker](https://github.com/tiangolo/uwsgi-nginx-flask-docker)
- [ ] [Lightsail](https://github.com/Pengin-Open-Source/pengin-pie/issues/13)

## Optional Content
- [ ] [Get DB Browser](https://sqlitebrowser.org/)
- [ ] [CDK Workshop](https://cdkworkshop.com/30-python.html)
- [ ] [Preorder Traversal](https://www.hackerrank.com/challenges/tree-preorder-traversal/problem)
- [ ] [Meta](https://www.w3schools.com/tags/tag_meta.asp)
- [ ] [DynamoDB](https://github.com/Pengin-Open-Source/pengin-pie/issues/24)
