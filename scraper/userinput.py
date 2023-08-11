import argparse

def getUserInput():
        parser = argparse.ArgumentParser()

        # Username or E-Mail (Sign In)
        

        # Verbosisty
        parser.add_argument("-v","--verbose",dest="verbose",action="store_true",help="Verbosity")
        
        # Headless
        parser.add_argument("--headless",dest="headless",action="store_true",help="Headless mode.")

        

        # Scraping Targets
        subparsers = parser.add_subparsers(dest="subCommand",required=True)

        

        profile_parser = subparsers.add_parser("profile")
        profile_parser.add_argument("--followers",action="store_true")
        profile_parser.add_argument("--followings",action="store_true")
        target_group = profile_parser.add_mutually_exclusive_group(required=True)
        target_group.add_argument("-t","--target",dest="target",help="Username of the account.",type=str)
        target_group.add_argument("-T","--targets",dest="targets",help="Usernames of the accounts.",type=argparse.FileType("r"))

        signIn_group = profile_parser.add_mutually_exclusive_group(required=True)
        signIn_group.add_argument("-u","--username",dest="username",help="Username of the Instagram account to login.",type=str)
        signIn_group.add_argument("--email",dest="email",help="Email address name of Instagram account to login.",type=str)
        profile_parser.add_argument("-p","--password",dest="password",help="The password of the Instagram account to be logged in.",type=str,required=True)

        # Output Arguments
        output_group = profile_parser.add_mutually_exclusive_group(required=False)
        output_group.add_argument("-o",dest="output",action="store_true")
        output_group.add_argument("--output",dest="output",type=str)

        

        args = parser.parse_args()
        return args
