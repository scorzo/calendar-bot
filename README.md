# README for Google Calendar Event Scheduling Script

## Overview:
This script integrates with Google Calendar using the Google Calendar API to schedule events. It utilizes OpenAI's GPT-3.5 for processing natural language inputs for scheduling requests.

## Setup and Usage

Install Required Libraries:
Ensure you have the google-auth, google-auth-oauthlib, and google-auth-httplib2 libraries installed.

Set Up OAuth 2.0 Credentials:

Go to the Google Cloud Console.
Create OAuth 2.0 credentials for a desktop application.
Download the credentials JSON file.

Execute the script: python script_name.py.
The script listens for event scheduling commands (e.g., "Schedule a meeting with John on January 10 at 10 am") and processes these requests to add events to your Google Calendar.

Note: Ensure that you have the necessary permissions and correct calendar ID before running the script.