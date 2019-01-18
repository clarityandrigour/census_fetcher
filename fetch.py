# imports

from ftplib import FTP
import os
import sys

# main namespace

if __name__ == '__main__':

    # constants/variables

    OUTPUT_PATH = ['.', 'downloads', ]

    CENSUS_FTP_SITE = 'ftp2.census.gov'
    CENSUS_TIGER_PATH = "geo/tiger/TIGER{census_year}/{geography_code}"
    CENSUS_YEARS = ['2018', ]

    GEOGRAPHY_CODES = ["TABBLOCK",]
    print(GEOGRAPHY_CODES)

    FTP_USER = 'anonymous'
    FTP_PASSWORD = 'anonymous'
    FTP_SUCCESS_STRING_NEEDLE = '230-Server'

    # create FTP object

    try:
        ftp = FTP(CENSUS_FTP_SITE)
        print("Successfully created an FTP object")
    except Exception :

        print("Cannot create an FTP object: {e}")
        sys.exit()

    # use FTP object to login

    try:
        census_server_respose_haystack = ftp.login(FTP_USER, FTP_PASSWORD)
        if FTP_SUCCESS_STRING_NEEDLE in census_server_respose_haystack:
            print("Successfully connected to FTP server")
        else:
            print("Was not able to connect to FTP server: {result}".format({'result': census_server_respose_haystack}))
            sys.exit()

    except Exception:
        print("Cannot log in to FTP server")
        sys.exit()

    # Set up loops to go through and download the files we wan - this could tke a while
    # There's no way to make this more efficient - you have to run everything against everything
    # LOOPS OF FURY!

    print("Beginning the loops of fury!")

    for census_year in CENSUS_YEARS:

        print(census_year)

        for geography_code in GEOGRAPHY_CODES:

            print(geography_code)

            # first make sure that there's a place locally for the downloaded files to live

            try:
                output_path = "/".join(OUTPUT_PATH + [census_year, geography_code])
                os.makedirs(output_path, exist_ok=True)
                print("Successfully created a directory at {output_path}".format({'output_path': output_path}))

            except Exception as e:
                print("Could not create a directory at {output_path}: {e}".format({'output_path': output_path, 'e': e}))
                sys.exit()

            # now we are going to list the files that we want on the remote server

            remote_census_path = CENSUS_TIGER_PATH.format({
                'census_year': census_year,
                'geography_code': geography_code
            })

            print(remote_census_path)

            files = ftp.nlst(remote_census_path)

            for file in files:
                print("Downloading...." + file)
                ftp.retrbinary("RETR" + file, open(output_path + '/' + file, 'wb').write)

            print("Finished downloading {census_year} : {geography_code}".format(
                {
                    'census_year': census_year,
                    'geography_code': geography_code
                }
            )
            )

        print("Just finished working on {census_year}".format({'census_year': census_year}))
