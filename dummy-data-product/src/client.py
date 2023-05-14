# defines libraries
import pandas as pd
import argparse
import datacommons as dc
from pathlib import Path
import dependencies.utils as utils
from dependencies.scraping import Scraper as scp 
obj = utils.Scraper()

# Set API key
dc.set_api_key(api_key='AIzaSyCTI4Xz-UW_G2Q2RfknhcfdAnTHq5X5XuI')

# specifies argument by the user  
parser = argparse.ArgumentParser(description='To fetch covid 19 data from datacommons.org')
parser.add_argument('-c', '--country', type=str, default=None ,help='country code')
parser.add_argument('-ac', '--all_country', type=str, default=None ,help='country code')
parser.add_argument('-f', '--feature', type=int, default=None, help='feature for which you requires the data')
parser.add_argument('-af', '--all', type=str, default=None, help='if all features are required')
args = parser.parse_args()

DATA_DIR = Path('data')
DATA_DIR.mkdir(exist_ok=True)

DATA_DIR = Path('meta_data')
DATA_DIR.mkdir(exist_ok=True)

if args.country is not None and args.all_country is not None:
    
    print("You can't set both c & ac , Please check the README.md file")

elif args.feature is not None and args.all is not None:
    
    print("You can't set both f & af , Please check the README.md file")

elif args.feature is not None and args.country is not None:
    
    # specific covid 19 data to specific country
    scp.scraper(args.country, args.feature)

elif args.all is not None and args.country is not None:
    
    # all covid 19 data to specific country
    obj.scraper_a_s(args.country) 

elif args.feature is not None and args.all_country is not None:
    
    # specific covid 19 data to all country
    obj.scraper_s_a(args.feature)

elif args.all is not None and args.all_country is not None:
    
    # all covid 19 data to all country
    obj.scraper_a_a()

else:    
    print("Please read 'README.md' file carefully ...!")
