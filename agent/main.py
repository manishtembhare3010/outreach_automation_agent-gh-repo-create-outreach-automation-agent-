"""
Outreach Automation Agent for Matherson and Sons
Main entry point that orchestrates the complete outreach workflow
"""
import os
import time
from datetime import datetime, timedelta

# Try to import APScheduler, but make it optional for demo mode
try:
    from apscheduler.schedulers.background import BackgroundScheduler
    SCHEDULER_AVAILABLE = True
except ImportError:
    print("⚠️ APScheduler not available. Running in demo mode only.")
    SCHEDULER_AVAILABLE = False

from agent.scraper.data_sources import find_companies_and_contacts
from agent.emailing.sender import send_initial_emails, send_followup_emails, send_personalized_emails
from agent.reply_handler.processor import process_responses
from agent.slack.notifier import notify_on_interest
from agent.calendar.booker import book_meeting

# Initialize campaign data store (in-memory for demo)
campaign_data = {
    "contacts": [],
    "sent_initial": [],
    "bounced": [],
    "unsubscribed": [],
    "replied": [],
    "interested": [],
    "meetings_booked": []
}

def run_campaign():
    """Starts the outreach campaign and schedules follow-up actions"""
    if not SCHEDULER_AVAILABLE:
        print("❌ Cannot run full campaign without APScheduler. Please use demo mode.")
        return
        
    print("🚀 Starting outreach campaign for Matherson and Sons...")
    
    # Step 1: Find target companies and contacts
    companies = find_companies_and_contacts("manufacturing, construction", "Australia", 
                                            ["CFO", "Head of Digital Transformation", "Digital Transformation Lead"])
    campaign_data["contacts"] = companies
    
    # Step 2: Send initial emails
    print(f"📧 Sending initial emails to {len(companies)} contacts...")
    send_initial_emails(companies)
    campaign_data["sent_initial"] = [contact["email"] for contact in companies]
    
    # Step 3: Schedule follow-ups
    scheduler = BackgroundScheduler()
    
    # Day 3 follow-up
    followup_date = datetime.now() + timedelta(days=3)
    scheduler.add_job(day3_followup, 'date', run_date=followup_date)
    
    # Day 4 personalized emails
    personalized_date = datetime.now() + timedelta(days=4)
    scheduler.add_job(day4_personalized, 'date', run_date=personalized_date)
    
    # Continuous response checking (every hour)
    scheduler.add_job(check_responses, 'interval', hours=1)
    
    scheduler.start()
    print(f"📅 Scheduled follow-ups for Day 3 ({followup_date.strftime('%Y-%m-%d')}) and Day 4 ({personalized_date.strftime('%Y-%m-%d')})")
    print("📊 Campaign started. Monitoring for responses...")
    
    # Keep the main thread alive for demo purposes
    try:
        while True:
            time.sleep(10)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("Campaign monitoring ended.")

def day3_followup():
    """Day 3 follow-up logic"""
    print("\n📅 Day 3: Sending follow-up emails...")
    
    # Filter out bounced, unsubscribed, and replied contacts
    eligible_contacts = [
        contact for contact in campaign_data["contacts"]
        if contact["email"] not in campaign_data["bounced"]
        and contact["email"] not in campaign_data["unsubscribed"]
        and contact["email"] not in campaign_data["replied"]
    ]
    
    print(f"📧 Sending follow-up emails to {len(eligible_contacts)} contacts who haven't responded...")
    send_followup_emails(eligible_contacts)

def day4_personalized():
    """Day 4 personalized emails logic"""
    print("\n📅 Day 4: Sending personalized 1-on-1 emails...")
    
    # Filter for contacts who received follow-up but haven't replied
    eligible_contacts = [
        contact for contact in campaign_data["contacts"]
        if contact["email"] not in campaign_data["bounced"]
        and contact["email"] not in campaign_data["unsubscribed"]
        and contact["email"] not in campaign_data["replied"]
    ]
    
    print(f"📧 Sending personalized emails to {len(eligible_contacts)} contacts...")
    send_personalized_emails(eligible_contacts)

def check_responses():
    """Check for new responses and handle them"""
    new_responses = process_responses(campaign_data["sent_initial"])
    
    for response in new_responses:
        email = response["email"]
        if response["status"] == "bounced":
            campaign_data["bounced"].append(email)
        elif response["status"] == "unsubscribed":
            campaign_data["unsubscribed"].append(email)
        elif response["status"] == "replied":
            campaign_data["replied"].append(email)
            
            if response["is_interested"]:
                campaign_data["interested"].append(email)
                # Notify team on Slack
                notify_on_interest(email, response["content"])
                
                # Book a meeting
                if book_meeting(email):
                    campaign_data["meetings_booked"].append(email)

def demo_mode():
    """Demo mode that simulates a compressed campaign timeline"""
    print("🚀 Starting DEMO mode with compressed timeline...")
    
    # Step 1: Find target companies and contacts
    companies = find_companies_and_contacts("manufacturing, construction", "Australia", 
                                            ["CFO", "Head of Digital Transformation", "Digital Transformation Lead"])
    campaign_data["contacts"] = companies
    
    # Step 2: Send initial emails
    print(f"📧 Sending initial emails to {len(companies)} contacts...")
    send_initial_emails(companies)
    campaign_data["sent_initial"] = [contact["email"] for contact in companies]
    
    # Demo: Check for immediate responses (simulated)
    print("\n⏳ Simulating time passing... checking for responses")
    check_responses()
    
    # Demo: Day 3 follow-up (compressed to a few seconds)
    print("\n⏳ Simulating Day 3...")
    day3_followup()
    
    # Demo: More responses come in
    print("\n⏳ Simulating more time passing... checking for responses")
    check_responses()
    
    # Demo: Day 4 personalized emails
    print("\n⏳ Simulating Day 4...")
    day4_personalized()
    
    # Demo: Final check for responses
    print("\n⏳ Simulating final response check...")
    check_responses()
    
    # Campaign summary
    print("\n📊 Campaign Summary:")
    print(f"Total contacts: {len(campaign_data['contacts'])}")
    print(f"Bounced emails: {len(campaign_data['bounced'])}")
    print(f"Unsubscribed: {len(campaign_data['unsubscribed'])}")
    print(f"Replied: {len(campaign_data['replied'])}")
    print(f"Interested: {len(campaign_data['interested'])}")
    print(f"Meetings booked: {len(campaign_data['meetings_booked'])}")

if __name__ == "__main__":
    # Set to True for demo mode (compressed timeline for testing)
    DEMO_MODE = True
    
    if DEMO_MODE or not SCHEDULER_AVAILABLE:
        demo_mode()
    else:
        run_campaign()