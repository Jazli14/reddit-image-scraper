# Reddit Image Scraper

This is a basic Reddit image scraper on Python that can download images and gifs to your computer.
It uses the Reddit API
The user will need to create their own Reddit API and copy the personal use script and secret key values.
Using this [link](https://www.reddit.com/prefs/apps)

## How to Use
The user can create a text file containing your Reddit credentials that is line separates their personal use script, secret key, app name, user name and password
Or the user may manually pass these into the console when running the image_scraper.py file with a terminal.

Then pass the program will prompt the user with three queries:
1. The number of images to download.
2. The subreddit to scrape from.
3. The category to sort the posts by.

After that the program will deliver these images to the folder labelled "images" with a subdirectory of the name of the subreddit.
