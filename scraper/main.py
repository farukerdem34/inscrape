from selenium import webdriver
from instagramUserInfo import User
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from userinput import getUserInput
from colors import bcolors as colors
import os
import datetime


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
    



args = getUserInput()


def scaping_info(username: str, target: str, datetime: datetime):
    print(username+"   ---scraping--->   " + target, datetime)


def print_title(title: str, dash_count: int = 50):
    print(colors.OKGREEN+("="*dash_count) +
          f"{title}"+("="*dash_count)+colors.ENDC)


def save_output(output, followers, followings,followers_bool:bool,followings_bool:bool):
    if type(output) == bool:
        if args.followers:
            with open("followers.txt", "w") as file:
                file.write(followers)
        if args.followings:
            with open("followings.txt", "w") as file:
                file.write(followings)
    else:
        if followers_bool:
            with open(f"{args.output}.followers.txt", "w") as file:
                file.write(followers)
        if followings_bool:
            with open(f"{args.output}.followings.txt", "w") as file:
                file.write(followings)

def make_targets_list(target_file):
    targets = []
    for i in target_file:
        i = str(i)
        if i == "\n":
            pass
        else:
            targets.append(i.strip().replace("\n",""))
    return targets

def show_targets(args,targets):
    for i in args.targets.readlines():
        i = str(i)
        if i == "\n":
            pass
        else:
            targets.append(i.strip().replace("\n",""))

    print(f"{colors.HEADER}Targets:{colors.ENDC}")

    for target in targets:
        print(f"{colors.WARNING}[+] {target}{colors.ENDC}")

def sign_in_method(args):
    if args.username:
        signin_method = args.username
    elif args.email:
        signin_method = args.email
    return signin_method


signin_method = sign_in_method(args)

instagram = Instagram(signin_method=signin_method, password=args.password)



def follow_actions(args):
    instagram.signIn()  
    if args.target:
        attack_target(args.username,args.target,args.followers,args.following,args.verbose)
    elif args.targets:
        targets = make_targets_list(args.targets.readlines())
        show_targets(args,targets)
        attack_targets(targets)

def attack_targets(targets):
    for target in targets:
        attack_target(args.username,target,args.followers,args.following,args.output,args.verbose)

def attack_target(username:str,target:str,followers:bool,followings:bool,output,verbose:bool=False):
    scaping_info(username, target, datetime.datetime.now())
    if followers:
        followers_list = instagram.getFollowers(target, args.verbose)
        instagram.clean_terminal()
        print_title("Followers")
        if followers == None:
            print(f"{colors.FAIL}{target} has no followers..{colors.ENDC}")
        else:
            for i in followers:
                follower = i["username"]
                follower_url = i["profile_link"]
                print(
                        f"Username: {colors.OKCYAN}{follower}{colors.ENDC}, URL: {colors.OKCYAN}{follower_url}{colors.ENDC}")
                print_title("Followings")
    if followings:
        followings_list = instagram.getFollowing(target, verbose)
        print_title("Followers")
        if followings == None:
            print(f"{colors.FAIL}{target} does not follow any acoount.{colors.ENDC}")
        else:
            for i in followings:
                following = i["username"]
                following_url = i["profile_link"]
                print(
                        f"Username: {colors.OKCYAN}{following}{colors.ENDC}, URL: {colors.OKCYAN}{following_url}{colors.ENDC}")
    if output and not (followers == None) and not (following == None):
        save_output(output,followers_list,followings_list,followers, followings)
    else:
        print(f"{colors.FAIL}The output could not be saved{colors.ENDC}")


if args.subCommand == "profile":
    follow_actions(args)
else:
    pass    