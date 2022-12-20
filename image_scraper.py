import praw
import urllib
import os


def create_subreddit_directory(subreddit: str) -> str:
    """ Creates the subreddit folder for the images and returns its file path.

    Args:
        subreddit: A string representing the subreddit that was chosen.

    Returns:
        A file path string representing the subreddit.

    """
    file_path = os.path.join(os.getcwd(), "media", subreddit)
    
    # if directory does not exist then create the new directory
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    return file_path 


def ask_user() -> tuple[list]:
    """ Gets input from the user for the credentials of their account and API
        And requests the user's chosen number of images, subreddit and category.

    Args: 
        None.
    
    Returns:
        A tuple that first contains the list of credentials for the API and a list of inputs from the user.
    """
    list_of_creds = []
    list_of_inputs = []

    txt_or_not = input("Do you have a credentials file? Enter yes or no\n")

    # If the user has a text file for credentials
    if (txt_or_not.lower() == "yes"):
        credential_file = input("Enter the name of the crendentials file:\n") + ".txt"
        list_of_creds = read_creds(credential_file)
        

    # Asks for the user to input their credentials manually
    elif (txt_or_not.lower() == "no"):
        list_of_creds.append(input("Enter the personal use script:\n"))
        list_of_creds.append(input("Enter the secret key:\n"))
        list_of_creds.append(input("Enter the app name:\n"))
        list_of_creds.append(input("Enter your username:\n"))
        list_of_creds.append(input("Enter your password:\n"))

    # Asks the user for the number of images they want to scrape and what subreddit and category
    list_of_inputs.append(input("Enter the number of images you want:\n"))
    list_of_inputs.append(input("Enter your selected subreddit:\n"))
    list_of_inputs.append(input("Enter the category to sort by:\n"))

    return list_of_creds, list_of_inputs


def reddit_API(credentials: list) -> praw.Reddit:
    """ Creates the praw Reddit object by passing in the credentials.

    Args:
        credentials: A list of credentials that will be used to create the object.

    Returns:
        A praw.Reddit object with the passed in credentials.
    """
    personal_use_script = credentials[0]
    secret = credentials[1]
    user_agent = credentials[2]
    username = credentials[3]
    password = credentials[4]

    # Creates the Reddit object with praw passing in the credentials
    reddit = praw.Reddit(client_id=personal_use_script,
                        client_secret=secret,
                        user_agent=user_agent,
                        username=username,
                        password=password)

    return reddit


def read_creds(txt_file:str) -> list:
    """ Reads txt_file of credentials and saves it to the credntial list.
    
    Args:
        txt_file: A string representing the file name of the credentials text file.
    
    Returns:
        A list of credentials that were appended to it from the text file.
        This contains the personal use script, secret key, app name, username, password in order.
    """
    credential_list = []

    with open(txt_file, 'r') as f:
        for l in f:
            # Appends the line with \n stripped
            credential_list.append(l.strip())

    return credential_list


def category_select(category: str, images: int):
    """Sorts the posts by the category the user selects.

    Args:
        category: A string representing the category selected to sort by.
        images: An int representing the number of images to be scraped.
    
    Returns:
        A list generator object that can be parsed using the next function.
    """
    # Switches to hot
    if (category.lower() == "hot"):
        threads = subreddit.hot(limit=images)
    elif (category.lower() == "top"):
        threads = subreddit.top(limit=images)
    elif (category.lower() == "new"):
        threads = subreddit.new(limit=images)
    elif (category.lower() == "controversial"):
        threads = subreddit.controversial(limit=images)
    return threads


def scrape_media(num_image: int, subreddit: str, category: str) -> None:
    """ Scrapes media from the subreddit and saves it to its corresponding directory.

    Args:
        num_image: The number of images to scrape.
        subreddit: The chosen subreddit to scrape.
        category: The chosen category to sort by.

    Returns:
        None, since the function only saves directly saves the url's media to the directory.

    """
    image_number = 0
    posts = category_select(category, num_image)

    # Iterate through the posts by the number of images
    for _ in range(num_image):
        current_post = next(posts)
        # current_post = next(subreddit.top(limit=num_image))
        # Extract the file format from the url
        ending = current_post.url.rsplit(".")[-1]

        # If no images or gifs were to be found then skip the post
        if "png" not in ending or "jpg" not in ending or "gif" not in ending or "gifv" not in ending:
            continue
        print(current_post.url)
        try:
            full_file_name = os.path.join(subreddit_directory, subreddit + str(image_number) + "." + ending)
            # Save the object into the file path
            urllib.request.urlretrieve(current_post.url, full_file_name)
            image_number += 1
        except: 
            # Raise exception if media could not be saved to directory
            print("Image could not be downloaded: " + current_post.url)
            raise Exception

# Calls ask_user and saves the list of credentials and list of 
# inputs to reddit_credentials and user_input variables respectively
 
reddit_credentials, user_input = ask_user()

number_of_images = int(user_input[0])
chosen_subreddit = user_input[1]
chosen_category = user_input[2]

# Save the subreddit folder filepath
subreddit_directory = create_subreddit_directory(chosen_subreddit)

# Saves reddit object
reddit = reddit_API(reddit_credentials)

# Saves the subreddit object passing in the chosen_subreddit
subreddit = reddit.subreddit(chosen_subreddit)

# Calls scrape media to download the images and gifs from the subreddit
scrape_media(number_of_images, chosen_subreddit, chosen_category)