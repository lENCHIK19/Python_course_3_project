# Election Results Scraper

## Overview

This Python script scrapes election results from the official Czech election website (volby.cz). It extracts data for all municipalities in a given district - České Budějovice, including voter statistics and votes for each political party. The results are saved in a CSV file.

## Features

- Extracts election results for a given district.
- Scrapes voter statistics (registered voters, issued envelopes, valid votes).
- Scrapes votes for all participating political parties.
- Saves the results in a structured CSV format.
- Requires two command-line arguments: the election results URL and the output CSV file name.

### Installation of external libraries:

pip install requests
pip install beautifulsoup4

We also need two built-in modules:

sys - that provides access to system-specific parameters and functions, such as handling command-line arguments (sys.argv)

csv - or reading and writing CSV file

## Requirements

This project requires Python 3 and the following libraries, which can be installed using the `requirements.txt` file:

### `requirements.txt`:

```
beautifulsoup4==4.13.3
certifi==2025.1.31
charset-normalizer==3.4.1
et_xmlfile==2.0.0
idna==3.10
openpyxl==3.1.5
requests==2.32.3
soupsieve==2.6
typing_extensions==4.12.2
urllib3==2.3.0
```

## Usage

Run the script with two arguments:

1. The election results URL (e.g., from `volby.cz`).
2. The name of the output CSV file.

### Example usage:

1 argument: "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=3&xnumnuts=3101"
2 argument: 'results.csv'

Run the script:

python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=3&xnumnuts=3101" "results.csv"

## Expected Output

A CSV file (`scraper_results.csv`) with the following format:

Code,Location,Voters,Envelopes issued,Valid votes,Party 1,Party 2,Party 3,...
535826,Adamov,682,474,472,126,0,2,...
536156,Bečice,82,63,63,17,0,0,...

## Error Handling

- If incorrect arguments are provided, the script prints an error message and exits.
- If the provided URL does not match the expected election results structure, the script prints an error message and exits.
- If the output file does not have a `.csv` extension, an error is displayed.

## License

This project is open-source and free to use for educational purposes.
