# Own
from dependencies.scraping.scraper import get_articles
from dependencies.cleaning.cleaning import clean_data
from dependencies.geocoding.geocoder import get_geodecoded_data
from dependencies.standardization.standardizer import standardize_data
from dependencies.utils.utils import initialize_directories, empty_directories


# Python package
import logging

logging.basicConfig(level=logging.INFO)

initialize_directories()


def step_1():
    logging.info('Scraping data')
    get_articles()

    return None


def step_2():
    logging.info('Clean data')
    clean_data()

    return None


def step_3():
    logging.info('Geodecoded data')
    get_geodecoded_data()

    return None


def step_4():
    logging.info('Standarized data')
    standardize_data()

    return None


def step_empty():
    logging.info('Empty directories')
    empty_directories()

    return None


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--step", help="step to be choosen for execution")

    args = parser.parse_args()

    eval(f"step_{args.step}()")
