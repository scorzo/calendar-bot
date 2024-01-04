# README for Google Calendar Event Scheduling Script

## Overview:
This script integrates with Google Calendar using the Google Calendar API to schedule events. It utilizes OpenAI's GPT-3.5 for processing natural language inputs for scheduling requests.

## Setup and Usage

Install necessary libraries: google-api-python-client and google-auth.
Set up Google Cloud service account and download the credentials file.
Replace 'path/to/service_account.json' with the path to your credentials file in the script.
Running the Script:

Execute the script: python script_name.py.
The script listens for event scheduling commands (e.g., "Schedule a meeting with John on January 10 at 10 am") and processes these requests to add events to your Google Calendar.

Note: Ensure that you have the necessary permissions and correct calendar ID before running the script.