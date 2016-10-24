# Fetch Craigslist listings and send an update email

Providing one or several craiglists URL relevant to the search you are interested in, the script will send you an email containing the list of all links that were returned by the search.
The script keeps a local history of the posts so it doesn't send the same link twice.

I created this script when looking for a specific car so I would get updated right away when a new car matching my specific research was posted. Can be particularly helpful for apartment hunting too.

## Install

There is nothing to install, just make sure you have the following library installed:
- keyring (https://github.com/jaraco/keyring)
- yagmail (https://github.com/kootenpv/yagmail)

Save the password of your GMAIL_USERNAME with keyring, so it stays on your local machine.

## Usage

Replace the following variables in `cl-watcher.py` by what makes sense to you:
```
base_url
search_urls # Append search URLs to the list
GMAIL_USERNAME
SMTP_TO
```

Schedule the script with cron or launchd (I would highly recommend LaunchControl).
Receive your update emails as often as desired!