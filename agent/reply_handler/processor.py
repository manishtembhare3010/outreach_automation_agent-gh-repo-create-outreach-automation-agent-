"""
Reply Handler module for processing email responses
Handles bounces, unsubscribes, and parses replies for interest
"""
import random
import time

def simulate_fetch_responses(email_addresses):
    """
    Simulates fetching responses from an email system (like HubSpot, Gmail API, etc.)
    
    Args:
        email_addresses (list): List of email addresses to check for responses
        
    Returns:
        list: List of response objects
    """
    responses = []
    
    # Simulate checking each email for bounce/unsubscribe/reply
    for email in email_addresses:
        # Simulate a small percentage of emails bouncing
        if random.random() < 0.05:  # 5% bounce rate
            responses.append({
                "email": email,
                "status": "bounced",
                "reason": random.choice(["invalid_email", "mailbox_full", "domain_not_found"]),
                "timestamp": time.time()
            })
            continue
            
        # Simulate a small percentage of unsubscribes
        if random.random() < 0.03:  # 3% unsubscribe rate
            responses.append({
                "email": email,
                "status": "unsubscribed",
                "reason": "recipient_request",
                "timestamp": time.time()
            })
            continue
            
        # Simulate some replies (about 10% of remaining emails)
        if random.random() < 0.1:
            # Randomly choose if it's an out-of-office reply
            is_ooo = random.random() < 0.3  # 30% chance of out-of-office
            
            # Randomly choose if it's a positive reply (interested)
            is_interested = not is_ooo and random.random() < 0.4  # 40% of non-OOO replies are interested
            
            if is_ooo:
                content = "I'm currently out of the office until next week with limited access to email. I'll respond to your message when I return."
            elif is_interested:
                content = random.choice([
                    "Thanks for reaching out. This sounds interesting. I'd be happy to schedule a call next week to discuss further.",
                    "Your email caught my attention. We've been looking into digital transformation recently. Let's set up a time to chat.",
                    "I'm interested in learning more about your services. Can you send over some case studies from similar companies in our industry?"
                ])
            else:
                content = random.choice([
                    "Thanks, but we're not looking for these services at the moment.",
                    "We've recently signed with another provider for this. Perhaps we can connect in the future.",
                    "Please remove me from your list. This isn't relevant to our needs right now."
                ])
                
            responses.append({
                "email": email,
                "status": "replied",
                "content": content,
                "is_out_of_office": is_ooo,
                "is_interested": is_interested and not is_ooo,
                "timestamp": time.time()
            })
    
    return responses

def process_responses(email_addresses):
    """
    Processes email responses to detect status and intent
    
    Args:
        email_addresses (list): List of email addresses to check
        
    Returns:
        list: Processed response objects with status and interest flags
    """
    print(f"📬 Processing responses for {len(email_addresses)} contacts...")
    
    # Fetch responses (simulated)
    raw_responses = simulate_fetch_responses(email_addresses)
    
    # Process each response
    processed_responses = []
    for response in raw_responses:
        if response["status"] == "bounced":
            print(f"❌ Email to {response['email']} bounced: {response['reason']}")
            processed_responses.append(response)
            
        elif response["status"] == "unsubscribed":
            print(f"🚫 Contact {response['email']} unsubscribed")
            processed_responses.append(response)
            
        elif response["status"] == "replied":
            # Handle out-of-office replies
            if response.get("is_out_of_office", False):
                print(f"🏝️ Out of office reply from {response['email']}")
                # We don't mark them as replied for follow-up purposes
                continue
                
            # Analyze content for interest
            is_interested = response.get("is_interested", False)
            
            if is_interested:
                print(f"✅ Interested reply from {response['email']}: {response['content'][:50]}...")
            else:
                print(f"❓ Non-interested reply from {response['email']}")
                
            processed_responses.append(response)
    
    return processed_responses

def analyze_sentiment(text):
    """
    Analyzes text for sentiment and key phrases
    Very basic simulation of NLP capabilities
    
    Args:
        text (str): The email text to analyze
        
    Returns:
        dict: Sentiment analysis results
    """
    # In a real implementation, this would use NLP to analyze the text
    # Here we use a very basic approach
    
    positive_phrases = [
        "interested", "sounds good", "let's talk", "schedule", "call", "meet", 
        "learn more", "tell me more", "happy to", "case studies"
    ]
    
    negative_phrases = [
        "not interested", "no thanks", "remove", "unsubscribe", "don't contact", 
        "not relevant", "not looking", "no need"
    ]
    
    text_lower = text.lower()
    
    # Count positive and negative phrases
    positive_count = sum(1 for phrase in positive_phrases if phrase in text_lower)
    negative_count = sum(1 for phrase in negative_phrases if phrase in text_lower)
    
    # Calculate sentiment score (-1 to 1)
    total = positive_count + negative_count
    if total == 0:
        sentiment = 0
    else:
        sentiment = (positive_count - negative_count) / total
    
    # Determine overall sentiment
    if sentiment > 0.3:
        overall = "positive"
    elif sentiment < -0.3:
        overall = "negative"
    else:
        overall = "neutral"
    
    return {
        "sentiment_score": sentiment,
        "overall_sentiment": overall,
        "positive_phrases_found": positive_count,
        "negative_phrases_found": negative_count
    } 