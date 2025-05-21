# Outreach Automation Agent for Matherson and Sons

A production-level AI agent that automates outreach campaigns for Australian manufacturing & construction companies.

## Features
- Discovers companies & decision-makers in target industries (CFOs, Heads of Digital Transformation)
- Sends personalized emails using HubSpot templates (simulated)
- Implements multi-stage follow-up sequences (3-day wait, Day 4 personalized emails)
- Filters out bounced emails, unsubscribes, and out-of-office replies
- Sends interested replies to Slack
- Automatically books meetings when interest is detected

## Project Structure
- `scraper/`: Simulates LinkedIn/Apollo for company & contact discovery
- `emailing/`: Handles email sending via HubSpot API (simulated)
- `reply_handler/`: Processes email responses
- `slack/`: Posts interested replies to Slack
- `calendar/`: Manages automated meeting booking
- `scheduler/`: Controls campaign timing and follow-ups

## Setup
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with necessary credentials (for production use)

## Usage
```bash
python -m agent.main
```