"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Jelena Půžová
email: elenabaskova19@gmail.com
"""

import requests
import sys
import csv
from bs4 import BeautifulSoup

# Checking arguments

if len(sys.argv) != 3:
    print("Error: You must provide exactly two arguments.")
    print("Usage: python main.py <URL> <output_file.csv>")
    sys.exit(1)

DISTRICT_URL = sys.argv[1]
OUTPUT_FILE = sys.argv[2]

if not DISTRICT_URL.startswith("https://www.volby.cz/pls/ps2017nss/"):
    print("Error: The provided URL is not valid for the election results.")
    sys.exit(1)

if not OUTPUT_FILE.endswith(".csv"):
    print("ERROR: The second argument must be a .csv file!")
    sys.exit(1)

# Server response

def get_server_response(url):
    response = requests.get(url)
    if response.status_code != 200:
        sys.exit()
    return BeautifulSoup(response.text, "html.parser")


# Extract all municipalities in České Budějovice district

def get_municipality_links():
    soup = get_server_response(DISTRICT_URL)
    if not soup:
        return {}

    tables = soup.find_all("table", class_="table")[:3]
    municipalities = extract_municipalities_from_tables(tables)

    print(f" There are {len(municipalities)} municipalities in České Budějovice district.")
    return municipalities

# Extract municipalities details from the tables

def extract_municipalities_from_tables(tables):
    municipalities = {}

    for table in tables:
        for row in table.find_all("tr")[2:]:
            columns = row.find_all("td")
            if len(columns) < 3:
                continue

            code = columns[0].text.strip()
            name = columns[1].text.strip()
            link_tag = columns[0].find("a")

            if link_tag and "href" in link_tag.attrs:
                url = "https://www.volby.cz/pls/ps2017nss/" + link_tag["href"]
                municipalities[code] = (name, url)

    return municipalities

# Extract results for a specific municipality

def extract_municipality_results(municipality_url, municipality_code, municipality_name):
    print(f"⬇️ Extracting data for: {municipality_name} ({municipality_code})")

    soup = get_server_response(municipality_url)
    if not soup:
        return [municipality_code, municipality_name, "-", "-", "-", {}]

    tables = soup.find_all("table")

    # Voters data extraction
    registered_voters, envelopes_issued, valid_votes = extract_voter_data(tables)
    print(f"{municipality_name}: {registered_voters} voters, {envelopes_issued} envelopes, {valid_votes} votes")

    # Party votes extraction
    party_votes = extract_party_votes(tables)

    return [municipality_code, municipality_name, registered_voters, envelopes_issued, valid_votes, party_votes]

# Extract voter statistics from the first table

def extract_voter_data(tables):
    if not tables or len(tables[0].find_all("tr")) <= 2:
        return "-", "-", "-"

    summary_row = tables[0].find_all("tr")[2]
    columns = summary_row.find_all("td")

    return (
        clean_text(columns[3].text) if len(columns) > 3 else "-",
        clean_text(columns[4].text) if len(columns) > 4 else "-",
        clean_text(columns[7].text) if len(columns) > 7 else "-",
    )

# Extract party votes from the tables

def extract_party_votes(tables):
    party_votes = {}

    for table in tables[1:]:
        if "Platné hlasy" not in table.text:
            continue
        for row in table.find_all("tr")[2:]:
            columns = row.find_all("td")
            if len(columns) >= 3:
                party_name = columns[1].text.strip()
                votes = clean_text(columns[2].text)
                party_votes[party_name] = votes

    return party_votes if party_votes else {"No data": "0"}

# Data cleaning: Removing non-breaking spaces

def clean_text(text):
    return text.strip().replace("\u00a0", "")

# Saving results to CSV

CSV_HEADERS = ["Code", "Location", "Voters", "Envelopes issued", "Valid votes"]

def save_results_to_csv(results, filename, party_names):
    headers = CSV_HEADERS + sorted(party_names)
    
    with open(filename, mode="w", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        writer.writerow(headers)
        for result in results:
            municipality_data = result[:5]
            votes = result[5]
            row = municipality_data + [votes.get(party, "0") for party in sorted(party_names)]
            writer.writerow(row)

    print(f" CSV file '{filename}' was saved successfully.")

# Running the scraper

def main():
    print(f"⬇️ Scraping data for: {DISTRICT_URL}")

    municipalities = get_municipality_links()
    print(f" Extracted {len(municipalities)} municipalities.")

    all_results = []
    all_party_names = set()

    for municipality_code, (municipality_name, municipality_url) in municipalities.items():
        results = extract_municipality_results(municipality_url, municipality_code, municipality_name)
        if isinstance(results[-1], dict):
            all_party_names.update(results[-1].keys())
        all_results.append(results)

    all_party_names.discard("-")
    save_results_to_csv(all_results, OUTPUT_FILE, sorted(all_party_names))

if __name__ == "__main__":
    main()