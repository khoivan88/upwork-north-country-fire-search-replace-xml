# upwork-north-country-fire-manual-generation

# UPWORK - NORTH COUNTRY FIRE - SEARCH AND REPLACE OLD ID WITH NEW ONES

Search and Replace all instance of oldID with newID (except for those inside a URL) inside XML file

## CONTENT

- [Repo structure](#repo-structure)
- [Database structure](#images-folder-explanation)
- [Requirements](#requirements)
- [Usage](#usage)

<br/>

## REPO STRUCTURE

- [`requirements.txt`](requirements.txt): contains python packages required for the python code in this repo
- All codes and data are stored in [`src/`](/src/) folder:
  - [`src/scrape_ncf_images.py`](src/scrape_ncf_images.py): Scrapy spider to scrape images from northcountryfire.com. Using [original input file from NCF](src/data/imageNames.csv) as input source. Scraping log file for this spider is at [`src/logs/scrape_log_ncf.log`](/src/logs/scrape_log_ncf.log). Images not found from this source is documented at [`src/data/images_not_found_ncf.csv`](/src/data/images_not_found_ncf.csv). This spider run takes about 4-5 mins.
  - [`src/data/`](src/data): contains all data for this repo
  - [`src/logs/`](src/logs): contains all scraping logs for this repo


<br/>

## `DATA` FOLDER EXPLANATION

All of the images are in the [`/images`](/images/) folder. Within `images` folder:

- [`src/data/productIdDirectory.csv`](src/data/productIdDirectory.csv): contains mapping of oldIDs that need to be replaced with newIDs
- [`src/data/ncfCatalogIdSwitch.xml`](src/data/ncfCatalogIdSwitch.xml): the XML file that search-and-replace needs to be done on!
- [`src/data/ncfCatalogIdSwitch-fixed.xml`](src/data/ncfCatalogIdSwitch-fixed.xml): the finished search-and-replace XML file.

<br/>

## REQUIREMENTS

- Python 3.6+
- [Dependencies](requirements.txt)

<br/>

## USAGE

1. Clone this repository:

   ```console
   $ git clone https://github.com/khoivan88/upwork-north-country-fire-search-replace-xml    #if you have git
   # if you don't have git, you can download the zip file then unzip
   ```

2. (Optional): create virtual environment for python to install dependency:
   Note: you can change the `pyvenv` to another name if desired.

   ```console
   $ python -m venv pyvenv   # Create virtual environment
   $ source pyvenv/bin/activate    # Activate the virtual environment on Linux
   # pyvenv\Scripts\activate    # Activate the virtual environment on Windows
   ```

3. Install python dependencies:

   ```console
   $ pip install -r requirements.txt
   ```

4. Example usage:

    - `replace_product_id.py`

      ```console
      $ python src/replace_product_id.py
      ```

<br/>