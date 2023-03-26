# Football Match Data Scraper and Analysis
This Python script enables you to scrape and analyze football match data. It's designed to be executed from the command line and offers a range of options for data scraping, analysis, and visualization. The script empowers you to access a wide variety of football match data and analyze it in different ways. Additionally, you can use the script to create visualizations that help you gain insights from the data.

## Getting Started
### Prerequisites
Before running the script, make sure you have installed the following packages:
- `pandas`
- `rich`
- `matplotlib`
- `mysql-connector-python`
- `selenium`
- `beautifulsoup4`

You will also need the Chrome browser and the corresponding ChromeDriver.

## Installation
- Install Python 3.6 or higher from the [official website](https://www.python.org/downloads/).
- Install the required Python modules using pip:
``` python
pip install pandas rich matplotlib mysql-connector-python selenium beautifulsoup4
```
- Download the Chrome browser from the [official website](https://www.google.com/chrome/).
- Download the ChromeDriver from the [official website](https://chromedriver.chromium.org/downloads).

### Virtualenv
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

## Match Data Scraper
This Python script uses Selenium and BeautifulSoup to scrape match data from a website and save it to a CSV file or a MySQL database. It also includes an option to send an email notification once the data has been scraped.

### Usage
To use the Match Data Scraper script:

- Open the script in your Python editor of choice.
- Modify the script as needed (e.g. change the database credentials, email settings, etc.).
- Run the script using the command:
``` python
python footscraping.py [options]
```
Replace [options] with any of the following:

- `-c` or `--country`: Specify the name of the country to scrape data for (default: `"England"`).
- `-o` or `--output`: Specify the name of the output file (default: `"matches.csv"`).
- `-s` or `--save-to-db`: Save the data to a MySQL database (default: `False`).
- `-e` or `--send-email`: Send an email notification once the data has been scraped (default: `False`).

For example:
``` python
python footscraping.py -c Spain -o spain_matches.csv -s -e
```
This command will scrape match data for Spain, save it to a MySQL database, and send an email notification.

## Football Match Data Analysis
This Python script analyzes football match data. The script is designed to be run from the command line and provides various options for analyzing and visualizing the data.

### Usage
To use the Football Match Data Analysis script:

- Make sure you have scraped some match data using the Match Data Scraper script, or use the provided `input_matches_file.csv` file.
- Modify the script as needed (e.g. change the plot type, email settings, etc.).
- Run the script using the command:
``` python
python footanalysis.py [input_file][output_file][plot_type]
```
Replace [options] with the following arguments:
- `-i` or `--input_file`: The path to the input CSV file (default: `input_matches_file.csv`).
- `-o` or `--output_file`: The path to the output CSV file (default: `output_matches_file.csv`).
- `-p` or `--plot_type`: The type of plot to display. Possible values are: all, percentage, and `total_goals` (default: `all`).
- `-s` or `--show_plot`: If present, only shows the plot and does not perform any data analysis.
for example:
``` python
python footanalysis.py -i input.csv -o output.csv -p percentage
```
This command will perform data analysis on the `input.csv` file, create a `output.csv` file containing the analyzed data, and display a bar chart showing the percentage of wins, draws, and losses for each team.
``` python
python footanalysis.py -i input.csv -o output.csv -p total_goals -s
```
This command will perform data analysis on the `input.csv` file, create a `output.csv` file containing the analyzed data, and display a line chart showing the total number of goals scored in each match.

## Contributing 
If you have any suggestions for improving the program or finding bugs, please submit an [issue](https://github.com/TheHumanoidTyphoon/football-match-data-scraper-and-analysis/issues) or pull request on the [GitHub repository](https://github.com/TheHumanoidTyphoon/match-data-scraper).

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/TheHumanoidTyphoon/football-match-data-scraper-and-analysis/blob/main/LICENSE) file for details.

## Acknowledgments
[Adam Choi](https://www.adamchoi.co.uk/) for providing the website used to scrape the data.
