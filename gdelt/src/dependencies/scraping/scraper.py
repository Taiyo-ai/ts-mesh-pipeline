# Third library
from gdeltdoc import GdeltDoc, Filters
from dependencies.utils.utils import save_json_file


def get_articles():
    """
        Get the last 100 articles for theme GENERAL_HEALTH
    """

    f = Filters(
        theme="GENERAL_HEALTH",
        timespan='1week',
        num_records=100,
    )

    gd = GdeltDoc()

    # Search for articles matching the filters
    articles = gd.article_search(f)

    # Convert dataframe to json
    json_data = articles.to_json(orient='index')

    save_json_file(json_data, 'scraped_main_data', 'scraped_main_data.json')

    return None
