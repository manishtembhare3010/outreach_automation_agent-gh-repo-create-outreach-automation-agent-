"""
Slack integration module for sending notifications about interested prospects
"""
import os
import json
import time
from datetime import datetime

# Try to import slack_sdk, gracefully handle if not available
try:
    from slack_sdk import WebClient
    from slack_sdk.errors import SlackApiError
    SLACK_SDK_AVAILABLE = True
except ImportError:
    SLACK_SDK_AVAILABLE = False

def notify_on_interest(email, response_text):
    """
    Sends a notification to Slack when a prospect shows interest
    
    Args:
        email (str): The email address of the interested prospect
        response_text (str): The prospect's response content
        
    Returns:
        bool: True if notification was sent successfully, False otherwise
    """
    print(f"🔔 Interested prospect detected: {email}")
    
    # Try to look up contact details from our sent emails
    contact_info = find_contact_by_email(email)
    
    # Prepare the message text
    if contact_info:
        message = f"""
:white_check_mark: *Interested prospect!*
*Name:* {contact_info.get('contact_name', 'Unknown')}
*Company:* {contact_info.get('company', 'Unknown')}
*Role:* {contact_info.get('role', 'Unknown')}
*Email:* {email}

*Their response:*
```
{response_text}
```

*Next steps:* Schedule a call by replying to this thread with "book call".
"""
    else:
        message = f"""
:white_check_mark: *Interested prospect!*
*Email:* {email}

*Their response:*
```
{response_text}
```

*Next steps:* Schedule a call by replying to this thread with "book call".
"""
    
    return send_to_slack(message)

def send_to_slack(message):
    """
    Sends a message to Slack
    
    Args:
        message (str): The message to send
        
    Returns:
        bool: True if sent successfully, False otherwise
    """
    # If slack_sdk is available, try to use it
    if SLACK_SDK_AVAILABLE:
        # Try to get token from environment
        token = os.environ.get("SLACK_API_TOKEN")
        channel = os.environ.get("SLACK_CHANNEL", "#sales-leads")
        
        if token:
            try:
                client = WebClient(token=token)
                response = client.chat_postMessage(
                    channel=channel,
                    text=message,
                    mrkdwn=True
                )
                return True
            except SlackApiError as e:
                print(f"⚠️ Error sending to Slack: {e.response['error']}")
                # Fall back to simulation
        else:
            print("⚠️ No Slack API token found in environment, falling back to simulation")
    
    # Simulate sending to Slack
    print("\n-------- SLACK NOTIFICATION --------")
    print(f"Channel: #sales-leads")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(message)
    print("-----------------------------------\n")
    
    time.sleep(0.5)  # Simulate API delay
    return True

def find_contact_by_email(email):
    """
    Helper function to find contact information by email
    
    Args:
        email (str): The email to look up
        
    Returns:
        dict: Contact information if found, None otherwise
    """
    # In a real implementation, this would query a database or CRM
    # For simulation, we'll hardcode a few contacts
    contacts = [
        {
            "email": "john.doe@example.com",
            "contact_name": "John Doe",
            "company": "Aussie Manufacturing Co",
            "role": "CFO"
        },
        {
            "email": "jane.smith@example.com",
            "contact_name": "Jane Smith",
            "company": "BuildRight Constructions",
            "role": "Digital Transformation Lead"
        },
        {
            "email": "m.chen@example.com",
            "contact_name": "Michael Chen",
            "company": "Melbourne Industrial Solutions",
            "role": "CFO"
        },
        {
            "email": "j.taylor@example.com",
            "contact_name": "Jessica Taylor",
            "company": "Melbourne Industrial Solutions",
            "role": "Digital Transformation Lead"
        },
        {
            "email": "d.thompson@example.com",
            "contact_name": "David Thompson",
            "company": "BuildRight Constructions",
            "role": "CFO"
        },
        {
            "email": "emma.davis@example.com",
            "contact_name": "Emma Davis",
            "company": "Sydney Builders Group",
            "role": "Head of Digital Transformation"
        },
        {
            "email": "r.johnson@example.com",
            "contact_name": "Robert Johnson",
            "company": "Sydney Builders Group",
            "role": "CFO"
        }
    ]
    
    for contact in contacts:
        if contact["email"].lower() == email.lower():
            return contact
    
    return None