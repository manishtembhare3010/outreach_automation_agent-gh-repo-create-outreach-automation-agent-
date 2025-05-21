"""
Data sources module for retrieving company and contact information
Simulates APIs like LinkedIn and Apollo
"""
import random

def find_companies_and_contacts(industry_keywords, region, target_roles=None):
    """
    Simulates retrieving company and contact data from LinkedIn/Apollo
    
    Args:
        industry_keywords (str): Keywords for industries to target
        region (str): Geographic region to focus on
        target_roles (list): List of job titles/roles to target
        
    Returns:
        list: List of dictionaries containing company and contact information
    """
    print(f"🔍 Searching for {target_roles} in {industry_keywords} companies in {region}...")
    
    # In a real implementation, this would use APIs or web scraping
    # Here we simulate data returned from such services
    
    # Manufacturing companies data
    manufacturing_companies = [
        {
            "company": "Aussie Manufacturing Co",
            "industry": "Manufacturing",
            "website": "www.aussiemfg.com.au",
            "size": "50-200 employees",
            "contacts": [
                {
                    "name": "John Doe",
                    "role": "CFO",
                    "email": "john.doe@example.com",
                    "linkedin_url": "linkedin.com/in/johndoe"
                },
                {
                    "name": "Sarah Wilson",
                    "role": "Head of Digital Transformation",
                    "email": "sarah.wilson@example.com",
                    "linkedin_url": "linkedin.com/in/sarahwilson"
                }
            ]
        },
        {
            "company": "Melbourne Industrial Solutions",
            "industry": "Manufacturing",
            "website": "www.melbourneindustrial.com.au",
            "size": "200-500 employees",
            "contacts": [
                {
                    "name": "Michael Chen",
                    "role": "CFO",
                    "email": "m.chen@example.com",
                    "linkedin_url": "linkedin.com/in/michaelchen"
                },
                {
                    "name": "Jessica Taylor",
                    "role": "Digital Transformation Lead",
                    "email": "j.taylor@example.com",
                    "linkedin_url": "linkedin.com/in/jtaylor"
                }
            ]
        }
    ]
    
    # Construction companies data
    construction_companies = [
        {
            "company": "BuildRight Constructions",
            "industry": "Construction",
            "website": "www.buildright.com.au",
            "size": "100-250 employees",
            "contacts": [
                {
                    "name": "David Thompson",
                    "role": "CFO",
                    "email": "d.thompson@example.com",
                    "linkedin_url": "linkedin.com/in/davidthompson"
                },
                {
                    "name": "Jane Smith",
                    "role": "Digital Transformation Lead",
                    "email": "jane.smith@example.com",
                    "linkedin_url": "linkedin.com/in/janesmith"
                }
            ]
        },
        {
            "company": "Sydney Builders Group",
            "industry": "Construction",
            "website": "www.sydneybuilders.com.au",
            "size": "500-1000 employees",
            "contacts": [
                {
                    "name": "Robert Johnson",
                    "role": "CFO",
                    "email": "r.johnson@example.com",
                    "linkedin_url": "linkedin.com/in/robertjohnson"
                },
                {
                    "name": "Emma Davis",
                    "role": "Head of Digital Transformation",
                    "email": "emma.davis@example.com",
                    "linkedin_url": "linkedin.com/in/emmadavis"
                }
            ]
        }
    ]
    
    all_companies = []
    
    # Process based on industry keywords
    if "manufacturing" in industry_keywords.lower():
        all_companies.extend(manufacturing_companies)
        
    if "construction" in industry_keywords.lower():
        all_companies.extend(construction_companies)
    
    # Filter contacts based on target roles if provided
    result = []
    for company in all_companies:
        filtered_contacts = []
        
        for contact in company["contacts"]:
            if target_roles is None or any(role.lower() in contact["role"].lower() for role in target_roles):
                # Format the contact info for the email system
                contact_info = {
                    "company": company["company"],
                    "company_size": company["size"],
                    "industry": company["industry"],
                    "website": company["website"],
                    "contact_name": contact["name"],
                    "role": contact["role"],
                    "email": contact["email"],
                    "linkedin_url": contact["linkedin_url"]
                }
                filtered_contacts.append(contact_info)
        
        result.extend(filtered_contacts)
    
    print(f"✅ Found {len(result)} contacts matching criteria")
    return result

def enrich_contact_data(contact_list):
    """
    Simulates enriching contact data with additional information
    like personal interests, recent company news, etc.
    
    Args:
        contact_list (list): List of contact dictionaries
        
    Returns:
        list: Enriched contact list
    """
    interests = [
        "AI and automation", "Digital transformation", "Industry 4.0",
        "Sustainable manufacturing", "Supply chain optimization",
        "Cloud infrastructure", "Data analytics", "IoT implementation"
    ]
    
    company_news = [
        "recently expanded operations",
        "announced a sustainability initiative",
        "is implementing new ERP system",
        "acquired a smaller competitor",
        "launched a digital transformation project",
        "hired new technology leadership",
        "reported strong quarterly results"
    ]
    
    for contact in contact_list:
        # Add random interests (1-3 per contact)
        contact["interests"] = random.sample(interests, random.randint(1, 3))
        
        # Add random company news
        contact["recent_news"] = f"Company {random.choice(company_news)}"
        
        # Add random contact activity
        days_ago = random.randint(1, 30)
        contact["last_activity"] = f"Posted on LinkedIn {days_ago} days ago"
    
    return contact_list 