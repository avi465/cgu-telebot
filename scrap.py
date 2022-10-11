import csv
import requests
import os.path
from bs4 import BeautifulSoup


# file name
filename = 'notice.csv'
# list to store notice data
notice = []
stored_link = []
changes = []


def check_new_notice():
    # Making a GET request
    try:
        url = requests.get('https://cgu-odisha.ac.in/notice-board/')
    except:
        print("can't make request")

    # Parsing the HTML
    try:
        soup = BeautifulSoup(url.content, 'html.parser')
    except:
        print("beautifulsoup can't parse html")

    # scrapping data
    content = soup.find("table", id="tables")
    tbody = content.tbody
    tr = tbody.find_all("tr")
    for row in tr:
        row_data = []
        row_data.append(row.find_all("td")[0].string)
        row_data.append(row.find_all("td")[1].string)
        row_data.append(row.find_all("td")[2].string)
        row_data.append(row.find_all("td")[3].find("a").get("href"))
        notice.append(row_data)

    if not os.path.isfile(filename):
        with open(filename, "w") as file:
            csvwriter = csv.writer(file)
            csvwriter.writerow(["null", "null", "null", "null"])

    # reading data of csv
    try:
        with open(filename, 'r+') as file:
            csvreader = csv.reader(file)
            for row in csvreader:
                stored_link.append(row[3])
    except:
        print("file reading error")
    file.close()

    # writing data in csv
    try:
        with open(filename, 'w', newline='') as file:
            csvwriter = csv.writer(file)
            csvwriter.writerows(notice)
    except:
        print("file writing error")
    file.close()


# comparing changes
def changelog():
    for row in notice:
        try:
            if (stored_link[0] == row[3]):
                break
            changes.append(row)
        except IndexError:
            print("index error occured and handled")
