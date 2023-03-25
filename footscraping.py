import time
import argparse
import smtplib
import pandas as pd
import mysql.connector
from rich import print
from rich.console import Console
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

def get_driver():
    """
    Return a Chrome driver instance.

    Returns:
        An instance of Chrome webdriver configured with the required options.
    """
    # Configure Chrome options
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--log-level=3')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # Set Chrome driver path
    path = Service("D:/Program Files/chromedriver/chromedriver.exe")

    try:
        # Create and return Chrome driver instance
        return webdriver.Chrome(options=options, service=path)
    except WebDriverException as e:
        print(f"[bold red]An error occurred while trying to create the Chrome driver:[/bold red] {e}")
        return None

def fetch_data(driver, country):
    """
    Extract match data for the specified country from the website.

    Args:
        driver (webdriver): An instance of Chrome webdriver.
        country (str): A string specifying the name of the country.

    Returns:
        A list of lists containing the match data.
    """
    # Navigate to website
    driver.get('https://www.adamchoi.co.uk/overs/detailed')

    try:
        # Click on 'All matches' button
        driver.find_element(By.XPATH, "//label[@analytics-event='All matches']").click()

        # Select country from dropdown menu
        select = Select(driver.find_element(By.ID, 'country'))
        select.select_by_visible_text(country)

        # Wait for page to load
        time.sleep(5)

        # Extract match data
        matches = driver.find_elements(By.TAG_NAME, 'tr')
        data = []

        for match in matches:
            row = [
                match.find_element(By.XPATH, './td[1]').text,
                match.find_element(By.XPATH, './td[2]').text,
                match.find_element(By.XPATH, './td[3]').text,
                match.find_element(By.XPATH, './td[4]').text
            ]
            data.append(row)

        return data
    except (WebDriverException, TimeoutException) as e:
        print(f"[bold red]An error occurred while trying to fetch data:[/bold red] {e}")
        return []

def save_to_csv(data, output_file):
    """
    Save the data to a CSV file.

    Args:
        data (list): A list of lists containing the match data.
        output_file (str): A string specifying the name of the output file.

    Returns:
        A Pandas DataFrame containing the saved data.
    """
    try:
        df = pd.DataFrame(data, columns=['date', 'home_team', 'score', 'away_team'])
        df.to_csv(output_file, index=False)
        return df
    except Exception as e:
        print(f"[bold red]An error occurred while trying to save data to CSV file:[/bold red] {e}")

def save_to_db(data):
    """
    Save the data to a MySQL database.

    Args:
        data (list): A list of lists containing the match data.
    """
    try:
        # Connect to MySQL database
        mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Test@123',
            database='foot_database'
        )

        # Create table if it does not exist
        cursor = mydb.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS matches (id INT AUTO_INCREMENT PRIMARY KEY, date VARCHAR(255), home_team VARCHAR(255), score VARCHAR(255), away_team VARCHAR(255))')

        # Insert data into table
        sql = 'INSERT INTO matches (date, home_team, score, away_team) VALUES (%s, %s, %s, %s)'
        cursor.executemany(sql, data)
        mydb.commit()

        # Add notes using rich module
        console = Console()
        console.print('\n[bold green]Added to database[/bold green]')
        console.print(f'{len(data)} rows inserted into "matches" table.')
    except Exception as e:
        console.print(f"[bold red]An error occurred while trying to save data to MySQL[/bold red]")


def send_email(sender_email, sender_password, recipient_email, subject, body):
    """
    Send an email notification to the recipient using the sender's email address and password.

    Args:
        sender_email (str): A string containing the sender's email address.
        sender_password (str): A string containing the sender's email password.
        recipient_email (str): A string containing the recipient's email address.
        subject (str): A string containing the email subject.
        body (str): A string containing the email body.

    Returns:
        None
    """
    if not isinstance(sender_email, str):
        raise TypeError("sender_email must be a string")
    if not isinstance(sender_password, str):
        raise TypeError("sender_password must be a string")
    if not isinstance(recipient_email, str):
        raise TypeError("recipient_email must be a string")
    if not isinstance(subject, str):
        raise TypeError("subject must be a string")
    if not isinstance(body, str):
        raise TypeError("body must be a string")

    try:
        # Create SMTP session
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        # Login to sender email account
        server.login(sender_email, sender_password)

        # Compose email message
        message = f"Subject: {subject}\n\n{body}"

        # Send email
        server.sendmail(sender_email, recipient_email, message)

        # Close SMTP session
        server.quit()

        console = Console()
        console.print("[bold green]Email sent successfully[/bold green]")
    except Exception as e:
        print(f"[bold red]An error occurred while trying to send email:[/bold red] {e}")

def main():
    """
    Orchestrate the entire process of fetching match data from a website, saving it to CSV and MySQL, and sending email notifications.

    Returns:
        None
    """
    # Add command-line arguments
    parser = argparse.ArgumentParser(description='Fetch and save match data from website')
    parser.add_argument('-c', '--country', type=str, default='England', help='Specify the country name (default: England)')
    parser.add_argument('-o', '--output', type=str, default='matches.csv', help='Specify the output filename (default: matches.csv)')
    parser.add_argument('-s', '--save-to-db', action='store_true', help='Save the data to a MySQL database (default: False)')
    parser.add_argument('-e', '--send-email', action='store_true', help='Send an email notification once the data has been scraped (default: False)')
    args = parser.parse_args()

    # Get command-line arguments
    country = args.country
    output_file = args.output
    save_to_db = args.save_to_db
    send_email_flag = args.send_email

    # Read existing data from CSV file
    try:
        existing_df = pd.read_csv(output_file)
    except FileNotFoundError:
        existing_df = pd.DataFrame()

    # Get match data
    driver = get_driver()
    data = fetch_data(driver, country)
    driver.quit()

    # Save data to CSV file and print DataFrame
    save_to_csv(data, output_file)

    # Load data into Pandas DataFrame
    df = pd.read_csv(output_file)

    # Check if new data was added to the CSV file
    if len(df) > len(existing_df):
        # Save data to MySQL database
        if save_to_db:
            save_to_db(data)

        # Send email notification
        if send_email_flag:
            sender_email = "fe861282@gmail.com"
            sender_password = "h2os&vlo0AzqSh(+??cwE2dyK3FWnV"
            recipient_email = "lukbr25@gmail.com"
            subject = "New match data available"
            body = "New match data has been added to the CSV file. Check the website for more details."
            send_email(sender_email, sender_password, recipient_email, subject, body)

if __name__ == '__main__':
    main()


