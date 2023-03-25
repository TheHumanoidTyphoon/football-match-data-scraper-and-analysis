# Match Data Scraper
This Python script uses Selenium and BeautifulSoup to scrape match data from a website and save it to a CSV file or a MySQL database. It also includes an option to send an email notification once the data has been scraped.

## Preview
<img width=100% src="">

## Getting Started
### Prerequisites
To use this script, you will need the following:

- Python 3.6 or higher
- The following Python modules: `pandas`, `mysql-connector-python`, `selenium`, `beautifulsoup4`, `rich`
- Chrome browser and the corresponding ChromeDriver

It is recommended to use a virtual environment for running the Match Data Scraper. If you do not have a virtual environment set up, follow these steps:

- Install virtualenv by running the following command: 
``` python
pip install virtualenv
```
- Create a new virtual environment by running the command: 
``` python
virtualenv venv
```
- Activate the virtual environment by running the command:

On Linux/Mac:
``` python
source venv/bin/activate
```
On Windows:
``` python
./venv/Scripts/activate
```
- Install the required dependencies using pip: 
``` python
pip install -r requirements.txt
```

## Installation
- Install Python 3.6 or higher from the [official website](https://www.python.org/downloads/).

- Install the required Python modules using pip:
``` python
pip install pandas mysql-connector-python selenium beautifulsoup4 rich
```
- Download the Chrome browser from the [official website](https://www.google.com/chrome/).

- Download the ChromeDriver from the [official website](https://chromedriver.chromium.org/downloads).

## Usage
- Open the script in your Python editor of choice.
- Modify the script as needed (e.g. change the database credentials, email settings, etc.).
- Run the script using the command:
``` python
python match_data_scraper.py [options]
```

Replace [options] with any of the following:

- `-c` or `--country`: Specify the name of the country to scrape data for (default: `"England"`).
- `-o` or `--output`: Specify the name of the output file (default: `"matches.csv"`).
- `-s` or `--save-to-db`: Save the data to a MySQL database (default: `False`).
- `-e` or `--send-email`: Send an email notification once the data has been scraped (default: `False`).

For example:
``` python
python match_data_scraper.py -c "Spain" -o "spain_matches.csv" -s -e
```
This command will scrape match data for Spain, save it to a MySQL database, and send an email notification.

## Contributing 
If you have any suggestions for improving the program or finding bugs, please submit an [issue](https://github.com/TheHumanoidTyphoon/match-data-scraper/issues) or pull request on the [GitHub repository](https://github.com/TheHumanoidTyphoon/match-data-scraper).

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/TheHumanoidTyphoon/match-data-scraper/blob/main/LICENSE) file for details.

## Acknowledgments
[Adam Choi](https://www.adamchoi.co.uk/) for providing the website used to scrape the data.
