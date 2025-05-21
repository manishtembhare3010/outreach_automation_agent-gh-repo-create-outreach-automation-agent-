"""
Calendar booking module for scheduling meetings with interested prospects
Simulates integration with calendar APIs (Google Calendar, Outlook, etc.)
"""
import random
import time
from datetime import datetime, timedelta

def book_meeting(email):
    """
    Books a meeting with an interested prospect
    
    Args:
        email (str): Email address of the interested prospect
        
    Returns:
        bool: True if meeting was booked successfully, False otherwise
    """
    print(f"📅 Attempting to book a meeting with {email}...")
    time.sleep(0.5)  # Simulate API delay
    
    # Find available slots in the next 7 days
    available_slots = find_available_slots()
    
    if not available_slots:
        print(f"❌ No available slots found for meeting with {email}")
        return False
    
    # In a real implementation, we would send a calendar invite
    # Here we simulate a successful booking
    meeting_slot = random.choice(available_slots)
    
    # Simulate sending calendar invite
    success = simulate_calendar_booking(email, meeting_slot)
    
    if success:
        print(f"✅ Meeting booked with {email} for {meeting_slot['start_time'].strftime('%Y-%m-%d %H:%M')}")
        return True
    else:
        print(f"❌ Failed to book meeting with {email}")
        return False

def find_available_slots(days_ahead=7, daily_slots=3):
    """
    Finds available meeting slots in the next N days
    
    Args:
        days_ahead (int): Number of days to look ahead
        daily_slots (int): Number of slots per day to check
        
    Returns:
        list: List of available time slots
    """
    # In a real implementation, this would query the calendar API
    # Here we simulate finding available slots
    
    available_slots = []
    now = datetime.now()
    
    # Create slots for the next N days
    for day in range(1, days_ahead + 1):
        date = now + timedelta(days=day)
        
        # Skip weekends
        if date.weekday() >= 5:  # 5=Saturday, 6=Sunday
            continue
        
        # Generate slots for business hours (9AM-5PM)
        for hour in range(9, 17, 8 // daily_slots):
            # Create datetime for the slot
            slot_time = date.replace(hour=hour, minute=0, second=0, microsecond=0)
            
            # Simulate some slots being already booked
            is_available = random.random() > 0.3  # 30% chance slot is booked
            
            if is_available:
                available_slots.append({
                    "start_time": slot_time,
                    "end_time": slot_time + timedelta(minutes=30),
                    "id": f"slot_{slot_time.strftime('%Y%m%d%H%M')}"
                })
    
    return available_slots

def simulate_calendar_booking(email, time_slot):
    """
    Simulates creating a calendar event and sending invites
    
    Args:
        email (str): Email of the attendee
        time_slot (dict): Time slot information
        
    Returns:
        bool: True if successful, False otherwise
    """
    # In a real implementation, this would:
    # 1. Create a calendar event
    # 2. Add the prospect as an attendee
    # 3. Add relevant details (Zoom/Teams link, etc.)
    # 4. Send the invite
    
    # Event details
    event = {
        "summary": "Matherson and Sons - Introductory Call",
        "location": "Zoom (link in description)",
        "description": """
Meeting to discuss how Matherson and Sons can help with your digital transformation initiatives.

Zoom link: https://zoom.us/j/123456789
Password: matherson

Please let us know if you need to reschedule.
""",
        "start": {
            "dateTime": time_slot["start_time"].isoformat(),
            "timeZone": "Australia/Sydney",
        },
        "end": {
            "dateTime": time_slot["end_time"].isoformat(),
            "timeZone": "Australia/Sydney",
        },
        "attendees": [
            {"email": email},
            {"email": "alex@mathersonandsons.com"},
        ],
        "reminders": {
            "useDefault": False,
            "overrides": [
                {"method": "email", "minutes": 24 * 60},
                {"method": "popup", "minutes": 10},
            ],
        },
    }
    
    # Simulate API call latency
    time.sleep(0.3)
    
    # Simulate success with high probability
    return random.random() < 0.95  # 95% success rate 