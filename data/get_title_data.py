'''This script crawls a specified reddit and posts comments as the world
   renowned magician Tony Wonder'''

import os
import json
import time
import praw
import re


class RedditScraper:
    '''This is the reddit bot class for handling all interaction with the web'''
    def __init__(self, login_file, subreddit_name):
        self.login_file = login_file
        self.bot_name = 'reddit_scraper'
        self.new_item_default = 1000
        self.reddit = self.get_reddit_session()
        self.subreddit = self.get_subreddit_session(subreddit_name)

    @staticmethod
    def read_json_from_file(file):
        '''Reads json from file and returns a dict.
        Args:
            file (string): Path to json file.
        Returns:
            dict: Read and parsed json.
        '''
        with open(file) as data_file:
            login_info = json.load(data_file)
        return login_info

    @staticmethod
    def write_list_to_file(input_list, file_name):
        '''Writes given id to specified log file
        Args:
            input_list: list of strings desired to be written to file
            file_name: file name of log to append
        Returns:
            None
        '''
        with open(file_name, 'a') as file:
            file.writelines(["%s\n" % item  for item in input_list])


    def get_reddit_session(self):
        '''Authenticates and starts a praw.reddit.Reddit object
        Returns:
            praw.reddit.Reddit: Authenticated object
        '''
        login_info = self.get_login_info()
        reddit_object = praw.Reddit(client_id=login_info['client_id'],
                                    client_secret=login_info['secret'],
                                    redirect_uri='http://localhost:8080',
                                    user_agent=self.bot_name,
                                    username=login_info['username'],
                                    password=login_info['password'])
        return reddit_object

    def get_login_info(self):
        '''Gets login info from login_file
        Returns:
            dict: secret info needed for praw login and reddit posting
        '''
        if os.path.isfile(self.login_file):
            return self.read_json_from_file(self.login_file)
        else:
            return {"client_id":os.environ["LOGIN_INFO_CLIENT_ID"],
                    "secret":os.environ["LOGIN_INFO_SECRET"],
                    "username":os.environ["LOGIN_INFO_USERNAME"],
                    "password":os.environ["LOGIN_INFO_PASSWORD"]}

    def get_subreddit_session(self, subreddit_name):
        '''Gets subreddit session.
        Args:
            subreddit_name (string): Name of subreddit.
        Returns:
            praw Subreddit object.
        '''
        subreddit = self.reddit.subreddit(subreddit_name)
        return subreddit

    def get_new_posts(self):
        '''Returns new posts for specified subreddit.
        Args:
            None
        Returns:
            Generator of new posts for subreddit.
        '''
        newest_posts = self.subreddit.new(limit=self.new_item_default)
        return newest_posts

    def get_new_post_titles(self):
        '''Returns new post titles for specified subreddit.
        Args:
            None
        Returns:
            List of title strings.
        '''
        posts = self.get_new_posts()
        titles = []
        for submission in posts:
            titles.append(submission.title)
        return titles


def main():
    '''Main function that drives the comment and submission handling'''
    login_file = '../login_info.json'
    subreddit_name = 'minnesotavikings'
    reddit_bot = RedditScraper(login_file=login_file, subreddit_name=subreddit_name)

    titles = reddit_bot.get_new_post_titles()

    reddit_bot.write_list_to_file(titles, "post_titles.txt")

if __name__ == '__main__':
    main()
