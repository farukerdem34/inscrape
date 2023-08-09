from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from instagramUserInfo import User
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from userinput import getUserInput
from colors import bcolors as colors
import os
import datetime
import wget


class Instagram:
    def __init__(self, signin_method: str, password: str, wait: int = 4):
        self.browser = webdriver.Firefox()
        self.base_url = "https://www.instagram.com/"
        self.login_page = "accounts/login/"
        self.user = User(signin_method, password)
        self.wait = wait

    def waitForContent(self):
        sleep(self.wait)

    def signIn(self):
        self.browser.get(self.base_url+self.login_page)
        self.browser.implicitly_wait(20)
        emailInput = self.browser.find_element(
            By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[1]/div/label/input")
        passwordInput = self.browser.find_element(
            By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[2]/div/label/input")

        emailInput.send_keys(self.user.signin_method)
        passwordInput.send_keys(self.user.password)
        passwordInput.send_keys(Keys.ENTER)
        self.waitForContent()

    def verbose_list(self, data):
        self.clean_terminal()
        for i in data:
            print(i)

    def clean_terminal(self):
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

    def scrollDown(self, element):
        self.browser.execute_script(
            "arguments[0].scroll(0, arguments[0].scrollHeight);", element)
        self.waitForContent()

    def getFollowers(self, username: str, verbose: bool = False):
        self.browser.get(self.base_url+username+"/")
        self.waitForContent()
        followersButton = self.browser.find_element(
            By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[2]/a")
        followersButton.click()
        self.waitForContent()
        followersList = self.browser.find_elements(
            By.CSS_SELECTOR, "._aano > div:nth-child(1) > div:nth-child(1) > *")
        follower_count = len(followersList)
        if follower_count == 0:
            return None
        fbody = self.browser.find_element(
            By.XPATH, "//html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]")
        while True:
            print(f"{colors.WARNING}Receiving followers list.{colors.ENDC}")
            self.scrollDown(fbody)
            followersList = self.browser.find_elements(
                By.CSS_SELECTOR, "._aano > div:nth-child(1) > div:nth-child(1) > *")
            self.waitForContent()
            if not (follower_count == len(followersList)):
                follower_count = len(followersList)
                if verbose:
                    self.verbose_list(q.find_element(By.CSS_SELECTOR, "a").get_attribute(
                        "href")[26:-1] for q in followersList)
            else:
                break

        followers = []
        for follower in followersList:
            link = follower.find_element(
                By.CSS_SELECTOR, "a").get_attribute("href")
            data = {
                "username": link[26:-1],
                "profile_link": link
            }
            followers.append(data)
        return followers

    def getFollowing(self, username: str, verbose: bool = False):
        self.browser.get(self.base_url+username+"/")
        self.waitForContent()
        following = self.browser.find_element(
            By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[3]/a")
        following.click()
        self.waitForContent()
        followingsList = self.browser.find_elements(
            By.CSS_SELECTOR, "._aano > div:nth-child(1) > div:nth-child(1) > *")
        followingsCount = len(followingsList)
        if followingsCount == 0:
            return None
        fbody = self.browser.find_element(
            By.XPATH, "/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]")

        while True:
            print(f"{colors.WARNING}Receiving followings list.{colors.ENDC}")
            self.scrollDown(fbody)
            followingsList = self.browser.find_elements(
                By.CSS_SELECTOR, "._aano > div:nth-child(1) > div:nth-child(1) > *")
            self.waitForContent()
            if not (followingsCount == len(followingsList)):
                followingsCount = len(followingsList)
                if verbose:
                    self.verbose_list(q.find_element(By.CSS_SELECTOR, "a").get_attribute(
                        "href")[26:-1] for q in followingsList)
            else:
                break

        followings = []
        for account in followingsList:
            link = account.find_element(
                By.CSS_SELECTOR, "a").get_attribute("href")
            data = {
                "username": link[26:-1],
                "profile_link": link
            }
            followings.append(data)
        return followings

    def getPost(self, post_id):
        self.browser.get(f"{self.base_url}p/{post_id}/")
        self.waitForContent()
        try:
            post_image = self.browser.find_element(
                By.CSS_SELECTOR, "div.x972fbf > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > img:nth-child(1)")
            src = post_image.get_attribute("src")
        except NoSuchElementException:
            # try:
            #     post_video = self.browser.find_element(By.CSS_SELECTOR,"video.x1lliihq")
            #     src = post_video.get_attribute("src")
            # except NoSuchElementException:
            #     print(f"{colors.FAIL}Post content not found!{colors.ENDC}")
            print(f"{colors.FAIL}Post content not found!{colors.ENDC}")
            self.browser.close()
            quit()
        post_desc = self.browser.find_element(
            By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[2]/div/div/div[1]/div/div[2]/div/span/div/span").text
        post_desc = str(post_desc)
        path = os.getcwd()+"/"+post_desc
        os.mkdir(path)
        wget.download(src, out=path)


args = getUserInput()


def scaping_info(username: str, target: str, datetime: datetime):
    print(username+"   ---scraping--->   " + target, datetime)


def print_title(title: str, dash_count: int = 50):
    print(colors.OKGREEN+("="*dash_count) +
          f"{title}"+("="*dash_count)+colors.ENDC)


def save_output(args, followers, followings):
    if type(args.output) == bool:
        if args.followers:
            with open("followers.txt", "w") as file:
                file.write(followers)
        if args.followings:
            with open("followings.txt", "w") as file:
                file.write(followings)
    else:
        if args.followers:
            with open(f"{args.output}.followers.txt", "w") as file:
                file.write(followers)
        if args.followings:
            with open(f"{args.output}.followings.txt", "w") as file:
                file.write(followings)


def sign_in_method(args):
    if args.username:
        signin_method = args.username
    elif args.email:
        signin_method = args.email
    return signin_method


signin_method = sign_in_method(args)

instagram = Instagram(signin_method=signin_method, password=args.password)

instagram.signIn()


def follow_actions(args):
    scaping_info(args.username, args.target, datetime.datetime.now())
    if args.followers:
        followers = instagram.getFollowers(args.target, args.verbose)
        instagram.clean_terminal()
        print_title("Followers")
        if followers == None:
            print(f"{colors.FAIL}{args.target} has no followers..{colors.ENDC}")
        else:
            for i in followers:
                follower = i["username"]
                follower_url = i["profile_link"]
                print(
                    f"Username: {colors.OKCYAN}{follower}{colors.ENDC}, URL: {colors.OKCYAN}{follower_url}{colors.ENDC}")
                print_title("Followings")
    if args.followings:
        followings = instagram.getFollowing(args.target, args.verbose)
        print_title("Followers")
        if followings == None:
            print(
                f"{colors.FAIL}{args.target} does not follow any acoount.{colors.ENDC}")
        else:
            for i in followings:
                following = i["username"]
                following_url = i["profile_link"]
                print(
                    f"Username: {colors.OKCYAN}{following}{colors.ENDC}, URL: {colors.OKCYAN}{following_url}{colors.ENDC}")
    if args.output and not (followers == None) and not (following == None):
        save_output(args, followers, followings)
    else:
        print(f"{colors.FAIL}The output could not be saved{colors.ENDC}")


def post_actions(args):
    instagram.getPost(args.post)


if args.subCommand == "follow":
    follow_actions(args)
elif args.subCommand == "post":
    post_actions(args)
