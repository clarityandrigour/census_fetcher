# imports

import requests
import bs4
import os
import sys


# define functions

def check_for_url_code(url, status_code=200):
    """This function uses the requests library to retrieve the status code for a URL."""

    request_url = requests.get(url)

    if request_url.status_code == status_code:

        return True

    else:

        return False


# main namespace

if __name__ == '__main__':

    # constants/variables

    OUTPUT_PATH = ['.', 'downloads', ]

    CENSUS_TIGER_URL = 'https://www2.census.gov/geo/tiger/TIGER{census_year}/'
    CENSUS_YEARS = [str(year) for year in list(range(1992, 2018))]

    GEOGRAPHY_CODES = ["TABBLOCK", "SLDL", "SLDU", "STATE", "COUNTY", "ZCTA5"]

    # Set up loops to go through and download the files we wan - this could tke a while
    # There's no way to make this more efficient - you have to run everything against everything
    # LOOPS OF FURY!

    print("Beginning the loops of fury!")

    for census_year in CENSUS_YEARS:

        print("Beginning work on {census_year}".format(**{'census_year': census_year}))

        census_tiger_url_for_year = CENSUS_TIGER_URL.format(**{'census_year': census_year})

        year_exists_in_tiger = check_for_url_code(url=census_tiger_url_for_year, status_code=200)

        if not year_exists_in_tiger:

            print("There was no Census page for Year {census_year}".format(**{'census_year': census_year}))
            continue

        else:

            print("There was a Census page for Year {census_year}".format(**{'census_year': census_year}))
            for geography_code in GEOGRAPHY_CODES:

                geography_code = geography_code.upper()

                print("Beginning work on {geography_code}".format(**{'geography_code': geography_code}))

                # first make sure that there's a valid url

                census_tiger_url_for_year_and_geography = census_tiger_url_for_year + geography_code + '/'

                year_and_geography_exists_in_tiger = check_for_url_code(url=census_tiger_url_for_year_and_geography,
                                                                        status_code=200)

                if not year_and_geography_exists_in_tiger:
                    print("There was no Census page for Year {census_year} and Geography {geography_code}".format(
                        **{'census_year': census_year,
                           'geography_code': geography_code}))
                    continue

                else:

                    # then make sure that there's a place locally for the downloaded files to live

                    try:
                        output_path = "/".join(OUTPUT_PATH + [census_year, geography_code])
                        os.makedirs(output_path, exist_ok=True)
                        print(
                            "Successfully created or found a directory at {output_path}".format(
                                **{'output_path': output_path}))

                    except Exception as e:
                        print("Could not create or find a directory at {output_path}: {e}".format(
                            {'output_path': output_path, 'e': e}))
                        continue

                    # now we are going to list the files that we want on the remote server

                    downloaded_page_from_census = requests.get(census_tiger_url_for_year_and_geography)

                    census_page_bs4_haystack = bs4.BeautifulSoup(downloaded_page_from_census.text, 'html.parser')

                    for link in census_page_bs4_haystack.find_all("a"):

                        # find only the linked zipfiles

                        if '.zip' in link.contents[0]:

                            r = requests.get(census_tiger_url_for_year_and_geography + link["href"], stream=True)
                            r.raise_for_status()

                            with open("{directory_path}/{file_name}".format(
                                    **{'directory_path': output_path, 'file_name': link.contents[0]}), 'wb') as handle:

                                for block in r.iter_content(1024):
                                    handle.write(block)

                            print("Success for: " + link.contents[0])

                print("Just finished working on {census_year}".format(**{'census_year': census_year}))
