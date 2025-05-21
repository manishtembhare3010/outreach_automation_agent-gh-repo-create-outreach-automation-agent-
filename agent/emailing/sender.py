"""
Email sender module that handles all outbound communications
Simulates integration with HubSpot API
"""
import time
import random
from datetime import datetime

# Email templates
TEMPLATES = {
    "initial": """
Subject: Modernizing {industry} Operations at {company}

Hi {contact_name},

I noticed {company} {recent_news}. At Matherson and Sons, we specialize in helping {industry} companies like yours optimize operations through digital transformation.

Would you be open to a 15-minute chat about how we've helped similar {industry} companies achieve 30%+ operational efficiency gains?

Best,
Alex Matherson
Matherson and Sons
""",

    "followup": """
Subject: Re: Modernizing {industry} Operations at {company}

Hi {contact_name},

I wanted to follow up on my previous email about helping {company} optimize operations through strategic digital transformation.

Many {industry} companies we work with were initially hesitant until they saw our case studies. I'd be happy to share how we helped a {company_size} {industry} company achieve significant ROI within 6 months.

Would you have 15 minutes this week for a quick call?

Best,
Alex Matherson
Matherson and Sons
""",

    "personalized": """
Subject: Your LinkedIn post on {interests[0]}

Hi {contact_name},

I noticed your recent LinkedIn activity around {interests[0]}, and it resonated with the work we're doing at Matherson and Sons.

Given your role as {role} at {company}, I thought you might be interested in how we're helping {industry} companies implement {interests[0]} solutions that deliver measurable ROI.

I have a specific idea for {company} based on your recent initiatives. Would you be open to a brief discussion?

Best,
Alex Matherson
Matherson and Sons
"""
}

def simulate_hubspot_api_call(endpoint, data):
    """
    Simulates making a call to the HubSpot API
    
    Args:
        endpoint (str): The API endpoint
        data (dict): The data to send
    
    Returns:
        dict: Simulated API response
    """
    print(f"📤 HubSpot API: Calling {endpoint}...")
    time.sleep(0.2)  # Simulate API latency
    
    # Simulate successful response
    return {
        "id": random.randint(10000, 99999),
        "status": "success",
        "timestamp": datetime.now().isoformat()
    }

def format_email_from_template(template_name, contact_data):
    """
    Formats an email using a template and contact data
    
    Args:
        template_name (str): Name of the template to use
        contact_data (dict): Contact data to populate the template
    
    Returns:
        str: Formatted email content
    """
    template = TEMPLATES.get(template_name)
    if not template:
        raise ValueError(f"Unknown template: {template_name}")
    
    # Add default values for optional fields
    contact_data_with_defaults = contact_data.copy()
    if "recent_news" not in contact_data_with_defaults:
        contact_data_with_defaults["recent_news"] = "is in the " + contact_data["industry"] + " sector"
    if "interests" not in contact_data_with_defaults:
        contact_data_with_defaults["interests"] = ["digital transformation"]
    
    # Format the template with contact data
    return template.format(**contact_data_with_defaults)

def send_initial_emails(contacts):
    """
    Sends initial outreach emails to a list of contacts
    
    Args:
        contacts (list): List of contact dictionaries
    
    Returns:
        list: List of email IDs that were sent
    """
    sent_emails = []
    
    for contact in contacts:
        # Format email from template
        email_content = format_email_from_template("initial", contact)
        
        # Simulate sending via HubSpot
        response = simulate_hubspot_api_call("emails/send", {
            "to": contact["email"],
            "content": email_content,
            "campaign_id": "initial_outreach"
        })
        
        if response["status"] == "success":
            print(f"📧 Sent initial email to {contact['contact_name']} ({contact['email']}) at {contact['company']}")
            sent_emails.append(response["id"])
            
            # Simulate delay between emails to avoid triggering spam filters
            time.sleep(0.1)
    
    return sent_emails

def send_followup_emails(contacts):
    """
    Sends follow-up emails to contacts who haven't responded
    
    Args:
        contacts (list): List of contact dictionaries
    
    Returns:
        list: List of email IDs that were sent
    """
    sent_emails = []
    
    for contact in contacts:
        # Format email from template
        email_content = format_email_from_template("followup", contact)
        
        # Simulate sending via HubSpot
        response = simulate_hubspot_api_call("emails/send", {
            "to": contact["email"],
            "content": email_content,
            "campaign_id": "followup_outreach",
            "thread_id": f"thread_{contact['email'].replace('@', '_at_')}"  # Simulate threading
        })
        
        if response["status"] == "success":
            print(f"📧 Sent follow-up email to {contact['contact_name']} ({contact['email']}) at {contact['company']}")
            sent_emails.append(response["id"])
            
            # Simulate delay between emails to avoid triggering spam filters
            time.sleep(0.1)
    
    return sent_emails

def send_personalized_emails(contacts):
    """
    Sends highly personalized 1-on-1 emails based on contact data
    
    Args:
        contacts (list): List of contact dictionaries, ideally enriched with personal info
    
    Returns:
        list: List of email IDs that were sent
    """
    # Enrich contact data if possible
    try:
        from agent.scraper.data_sources import enrich_contact_data
        contacts = enrich_contact_data(contacts)
    except ImportError:
        print("⚠️ Contact enrichment not available, using basic data")
    
    sent_emails = []
    
    for contact in contacts:
        # Format email from template
        email_content = format_email_from_template("personalized", contact)
        
        # Simulate sending via HubSpot
        response = simulate_hubspot_api_call("emails/send", {
            "to": contact["email"],
            "content": email_content,
            "campaign_id": "personalized_outreach",
            "thread_id": f"thread_{contact['email'].replace('@', '_at_')}",  # Simulate threading
            "priority": "high"
        })
        
        if response["status"] == "success":
            print(f"📧 Sent personalized email to {contact['contact_name']} ({contact['email']}) at {contact['company']}")
            sent_emails.append(response["id"])
            
            # Longer delay for personalized emails to ensure quality
            time.sleep(0.2)
    
    return sent_emails