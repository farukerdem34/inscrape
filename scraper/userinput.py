import argparse

def getUserInput():
        parser = argparse.ArgumentParser()

        # Username or E-Mail
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument("-u","--username",dest="username",help="Instagram account username.",type=str)
        group.add_argument("--email",dest="email",help="Account email.",type=str,required=False)

        parser.add_argument("-p","--password",dest="password",help="Instagram account password.",type=str,required=True)
        parser.add_argument("-t","--target",dest="target",help="Target account name.",type=str,required=True)

        parser.add_argument("-v","--verbose",dest="verbose",action="store_true",help="Verbosity")
        output_group = parser.add_mutually_exclusive_group(required=False)
        output_group.add_argument("-o",dest="output",action="store_true")
        output_group.add_argument("--output",dest="output",type=str)
        args = parser.parse_args()
        return args