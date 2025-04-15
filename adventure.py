"""
Scoopy de poopy?
"""

import re
from datetime import datetime
import pandas as pd


def load_artifact_data(excel_filepath):
    """
    gets artifact data from an Excel file
    """
    artifact_df = pd.read_excel(excel_filepath, sheet_name='Main Chamber', skiprows=3)
    return artifact_df


def load_location_notes(tsv_filepath):
    """
    gets location notes from a TSV file
    """
    location_df = pd.read_csv(tsv_filepath, sep='\t')
    return location_df


def extract_journal_dates(journal_text):
    """
    gets all valid dates in the journal text, in format mm/dd/yyyy
    """
    date_candidates = re.findall(r"\d{2}/\d{2}/\d{4}", journal_text)
    valid_dates = []
    for date_str in date_candidates:
        try:
            datetime.strptime(date_str, '%m/%d/%Y')
            valid_dates.append(date_str)
        except ValueError:
            continue
    return valid_dates


def extract_secret_codes(journal_text):
    """
    gets all secret codes in the journal text
    """
    secret_codes = re.findall(r"AZMAR-\d{3}", journal_text)
    return secret_codes


if __name__ == '__main__':
    # define vars
    EXCEL_FILE = 'artifacts.xlsx'
    TSV_FILE = 'locations.tsv'
    JOURNAL_FILE = 'journal.txt'

    print("--- Loading Artifact Data ---")
    try:
        artifact_data = load_artifact_data(EXCEL_FILE)
        print(artifact_data.head())
    except FileNotFoundError:
        print(f"Error: File not found at {EXCEL_FILE}")

    print("\n--- Loading Location Notes ---")
    try:
        location_data = load_location_notes(TSV_FILE)
        print(location_data.head())
    except FileNotFoundError:
        print(f"Error: File not found at {TSV_FILE}")

    print("\n--- Extracting Journal Data ---")
    try:
        with open(JOURNAL_FILE, 'r', encoding='utf-8') as file:
            journal_content = file.read()
        journal_dates = extract_journal_dates(journal_content)
        codes = extract_secret_codes(journal_content)
        print("Extracted Dates:", journal_dates)
        print("Extracted Secret Codes:", codes)
    except FileNotFoundError:
        print(f"Error: File not found at {JOURNAL_FILE}")
