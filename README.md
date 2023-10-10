# Temperature Alert Agent

## Introduction

The Temperature Alert Agent is a collaborative project developed by our team of four using uagents from fetch.ai and Python. This agent offers real-time temperature alerts for your selected location. Set your desired temperature thresholds and receive alerts when the temperature goes beyond those limits. Stay informed and prepared with our Temperature Alert Agent!

## Members

- Priyanshu Gangavati
- Mohd Danish Siddiqui
- Shikhar Kunal
- Varad Patil

## Please Note

The program will only run if all the inputs are valid. For example, the code won't execute if an invalid city name is provided. Similarly, if the minimum temperature is greater than the maximum temperature, the message displayed in the alert box will not make sense and may appear incorrect. These validations have not been implemented in the current code.

## Setup

Follow these steps to set up the project:

1. Clone the repository:

$ git clone https://github.com/ShikharKunal/HackAI_Hack-230619  <br>
$ cd python


2. Install the required dependencies:
3. Move to the required directory and run the file:
$ cd src <br>
$ poetry run python main.py
(Location of main.py --> python/src)


## Usage

The Temperature Alert Agent allows you to monitor real-time temperature conditions in your chosen city. Set minimum and maximum temperature thresholds, click 'SUBMIT,' and receive alerts if the temperature goes beyond your specified limits. Stay informed and prepared with this user-friendly tool.

## Features

- Periodically obtains current temperature information from OpenWeatherMap using an API key and displays it
- Interactive Graphical User Interface (GUI)

&copy; HackAI_TeamID_230619 | 2023
