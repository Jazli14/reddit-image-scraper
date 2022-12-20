import praw
import urllib
import os

list_of_inputs = []

def read_creds(txt_file):
    with open(txt_file, 'r') as f:
        for l in f:
            list_of_inputs.append(l.strip())

def create_subreddit_directory(subreddit):
    file_path = os.path.join(os.getcwd(), "images", subreddit)
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    return file_path 

# txt_or_not = "yes"
txt_or_not = input("Do you have a credentials file? Enter yes or no\n")
if (txt_or_not.lower() == "yes"):
    creds = input("Enter the name of the crendentials file:\n") + ".txt"
    # creds = "credentials.txt"
    read_creds(creds)
elif (txt_or_not.lower() == "no"):
    list_of_inputs.append(input("Enter the personal use script:\n"))
    list_of_inputs.append(input("Enter the secret key:\n"))
    list_of_inputs.append(input("Enter the app name:\n"))
    list_of_inputs.append(input("Enter your username:\n"))
    list_of_inputs.append(input("Enter your password:\n"))
    list_of_inputs.append(input("Enter the number of images you want:\n"))
    list_of_inputs.append(input("Enter your selected subreddit:\n"))

personal_use_script = list_of_inputs[0]
secret = list_of_inputs[1]
user_agent = list_of_inputs[2]
username = list_of_inputs[3]
password = list_of_inputs[4]
number_of_images = int(list_of_inputs[5])
chosen_subreddit = list_of_inputs[6]

subreddit_directory = create_subreddit_directory(chosen_subreddit)

reddit = praw.Reddit(client_id=personal_use_script,
                    client_secret=secret,
                    user_agent=user_agent,
                    username=username,
                    password=password)


subreddit = reddit.subreddit(chosen_subreddit)
top = subreddit.top(limit=number_of_images)

image_number = 0
for i in range(number_of_images):
    current_post = next(top)
    print(current_post.url)
    ending = current_post.url.rsplit(".")[-1]
    try:
        full_file_name = os.path.join(subreddit_directory, chosen_subreddit + str(image_number) + "." + ending)
        urllib.request.urlretrieve(current_post.url, full_file_name)
        image_number += 1
    except: 
        print("Image could not be downloaded: " + current_post.url)
        raise Exception