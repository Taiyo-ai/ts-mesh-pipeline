# own
from dependencies.cleaning.cleaning import fix_data, clean_data
from dependencies.geocoding.geocoder import add_geocode_data
from dependencies.scraping.scraper import get_data
from dependencies.standardization.standardizer import standarized_data
from dependencies.utils.utils import check_directories_structure, clean_directories


# python
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

check_directories_structure()


def step_1():
    logging.info("Scraped Metadata")
    get_data()


def step_2():
    logging.info("Scraped Main Data")
    fix_data()


def step_3():
    logging.info("Cleaned Main Data")
    clean_data()


def step_4():
    logging.info("Geocoded Cleaned Data")
    add_geocode_data()


def step_5():
    logging.info("Standardized Geocoded Data")
    standarized_data()


def step_clean():
    logging.info("Clean data structure")
    clean_directories()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--step", help="step to be choosen for execution")

    args = parser.parse_args()

    eval(f"step_{args.step}()")

    logging.info(
        {
            "last_executed": str(datetime.now()),
            "status": "Pipeline executed successfully",
        }
    )
