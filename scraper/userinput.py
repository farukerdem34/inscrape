import argparse

def getUserInput():
        parser = argparse.ArgumentParser()

        # Username or E-Mail (Sign In)
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument("-u","--username",dest="username",help="Username of the Instagram account to login.",type=str)
        group.add_argument("--email",dest="email",help="Email address name of Instagram account to login.",type=str)
        parser.add_argument("-p","--password",dest="password",help="The password of the Instagram account to be logged in.",type=str,required=True)

        # Verbosisty
        parser.add_argument("-v","--verbose",dest="verbose",action="store_true",help="Verbosity")

        # Output Arguments
        

        # Scraping Targets
        subparsers = parser.add_subparsers(dest="subCommand",required=True)
        
        follow_parser = subparsers.add_parser("follow")
        follow_parser.add_argument("--followers",action="store_true")
        follow_parser.add_argument("--followings",action="store_true")
        follow_parser.add_argument("-t","--target",dest="target",help="Username of the account to get the follower and unfollowed list.",type=str,required=True)
        output_group = follow_parser.add_mutually_exclusive_group(required=False)
        output_group.add_argument("-o",dest="output",action="store_true")
        output_group.add_argument("--output",dest="output",type=str)

        post_parser = subparsers.add_parser("post")
        post_parser.add_argument("-p",dest="post",help="Single post download.",type=str,required=False)

        args = parser.parse_args()
        return args
