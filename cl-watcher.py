import json
import pydash
import requests
import yagmail
import os
from bs4 import BeautifulSoup
from time import strftime

cwd = os.getcwd()
HISTORY_FILE = cwd + '/cl_watcher_posts.hist'
LOG_FILE = cwd + '/cl-watcher.log'

# Personal variables
base_url = 'http://sfbay.craigslist.org'
search_urls = [] # Append as many search as you want
search_urls.append('/search/cta?query=gti&hasPic=1&min_price=9000&min_auto_year=2012&auto_title_status=1&auto_transmission=1')
GMAIL_USERNAME = 'your_username' # The username used to send the email via yagmail
SMTP_TO = 'recipient@gmail.com' # The recipient of the e-mail


def log_entry(message):
    now = strftime("%Y-%m-%d %H:%M:%S")
    f = open(LOG_FILE, 'a')
    f.write(str(now) + ': ' + str(message) + '\n')


def query_cl(search_url):    
    url = base_url + search_url
    r = requests.get(url)
    return r.text


def get_cl_posts():
    """ Fetch the raw HTML from a list of URL and extract the CL posts information
        Return: results (Array) - List of Dict reprensenting the CL posts
    """
    results = []
    for search_url in search_urls:
        raw_html = query_cl(search_url)
        soup = BeautifulSoup(raw_html, "html5lib")
        html_results = soup.findAll("p", { "class" : "row" })

        for html_result in html_results:
            link = html_result.find("a", { "class" : "hdrlnk" })
            price = html_result.find("span", { "class" : "price" })
            href = link['href']
            cl_post = {
                'title': link.string,
                'href': link['href'],
                'price': price.string
            }
            results.append(cl_post)

    return results


def filter_old_posts(posts):
    """ Filter the posts that have already been processed
        Args:   posts (Array) - The unfiltered list
        Return: posts (Array) - Filtered list
    """
    try:
        with open(HISTORY_FILE, 'r+') as f:
            for line in f.readlines():
                #TODO: Fix this logic
                # saved_post = json.loads(line)
                # pydash.pull(posts, lambda x: x == saved_post)
                #TODO: Delete this section if pydash is fixed 
                for post in posts:
                    if json.loads(line) == post:
                        pydash.pull(posts, post)
    except FileNotFoundError:
        f = open(HISTORY_FILE, 'w+')
        f.close()

    return posts


def archive_post(post):
    """ Archives a post to a list of processed post
        Args: post (Dict)
    """
    f = open(HISTORY_FILE, 'a')
    f.write(str(json.dumps(post)) + '\n')
    f.close()


def send_emails(posts):
    """ Sends one email grouping all posts
        Args: posts (Array)
    """
    yag = yagmail.SMTP(GMAIL_USERNAME)
    contents = []
    if len(posts) == 1:
        subject = 'cl-watcher: ' + posts[0]['title']
    else:
        subject = 'cl-watcher: ' + str(len(posts)) + ' new posts'
    for post in posts:
        contents.append('' + post['price'] + ': ' + base_url + post['href'])
    try:
        yag.send(SMTP_TO, subject, contents)
    except (Exception):
        raise e
    log_entry('Email sent with ' + str(len(posts)) + ' new post(s)')
    for post in posts:
        archive_post(post)
        

def main():
    log_entry('Fetching CL posts...')
    posts = get_cl_posts()
    posts = filter_old_posts(posts)
    if not posts:
        log_entry('Nothing new')
    else:
        send_emails(posts)

if __name__ == "__main__":
    main()
