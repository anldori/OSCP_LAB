import os
import argparse


parser = argparse.ArgumentParser(description='Git pushing script')
parser.add_argument("-m", "--message", help="commit message", required=False)
args = parser.parse_args()


message = args.message if args.message else "update write-up"
os.system('git add .')
os.system("git commit -m \"{}\"".format(message))
os.system('git push')

