from typing import Dict, List, Optional, Any, Union

def format_contact(contact: Dict[str, Any]) -> str:
    """Format a contact dictionary into a readable string with comprehensive field support.
    
    Args:
        contact: Dictionary containing contact information
        
    Returns:
        Formatted string representation of the contact
    """
    if not contact:
        return "No contact data available"
        
    if "status" in contact and contact["status"] == "error":
        return f"Error: {contact.get('message', 'Unknown error')}"
        
    parts = []
    
    # Name information
    if "displayName" in contact and contact["displayName"]:
        parts.append(f"📝 Name: {contact['displayName']}")
    elif "givenName" in contact or "familyName" in contact:
        name_parts = []
        if contact.get("givenName"):
            name_parts.append(contact["givenName"])
        if contact.get("familyName"):
            name_parts.append(contact["familyName"])
        if name_parts:
            parts.append(f"📝 Name: {' '.join(name_parts)}")
    
    # Nickname
    if contact.get("nickname"):
        parts.append(f"🏷️  Nickname: {contact['nickname']}")
    
    # Contact information
    if contact.get("emails"):
        if isinstance(contact["emails"], list):
            email_parts = []
            for email in contact["emails"]:
                if isinstance(email, dict):
                    label = email.get("label", email.get("type", ""))
                    label_text = f" ({label})" if label else ""
                    email_parts.append(f"   • {email.get('value', '')}{label_text}")
                else:
                    email_parts.append(f"   • {email}")
            parts.append(f"📧 Email(s):\n" + "\n".join(email_parts))
    elif contact.get("email"):
        parts.append(f"📧 Email: {contact['email']}")
    
    if contact.get("phones"):
        if isinstance(contact["phones"], list):
            phone_parts = []
            for phone in contact["phones"]:
                if isinstance(phone, dict):
                    label = phone.get("label", phone.get("type", ""))
                    label_text = f" ({label})" if label else ""
                    phone_parts.append(f"   • {phone.get('value', '')}{label_text}")
                else:
                    phone_parts.append(f"   • {phone}")
            parts.append(f"📱 Phone(s):\n" + "\n".join(phone_parts))
    elif contact.get("phone"):
        parts.append(f"📱 Phone: {contact['phone']}")
    
    # Professional information
    if contact.get("organization") or contact.get("jobTitle") or contact.get("department"):
        org_parts = []
        if contact.get("organization"):
            org_parts.append(f"Company: {contact['organization']}")
        if contact.get("jobTitle"):
            org_parts.append(f"Title: {contact['jobTitle']}")
        if contact.get("department"):
            org_parts.append(f"Department: {contact['department']}")
        parts.append(f"🏢 Work:\n   • " + "\n   • ".join(org_parts))
    
    # Addresses
    if contact.get("addresses"):
        if isinstance(contact["addresses"], list):
            addr_parts = []
            for addr in contact["addresses"]:
                if isinstance(addr, dict):
                    formatted_addr = addr.get("formatted", "")
                    addr_type = addr.get("type", addr.get("label", ""))
                    type_text = f" ({addr_type})" if addr_type else ""
                    addr_parts.append(f"   • {formatted_addr}{type_text}")
                else:
                    addr_parts.append(f"   • {addr}")
            parts.append(f"🏠 Address(es):\n" + "\n".join(addr_parts))
    
    # Birthday
    if contact.get("birthday"):
        birthday = contact["birthday"]
        if isinstance(birthday, dict):
            year = birthday.get("year", "")
            month = birthday.get("month", "")
            day = birthday.get("day", "")
            if year and month and day:
                parts.append(f"🎂 Birthday: {year}-{month:02d}-{day:02d}")
            elif month and day:
                parts.append(f"🎂 Birthday: {month:02d}-{day:02d}")
        else:
            parts.append(f"🎂 Birthday: {birthday}")
    
    # Websites/URLs
    if contact.get("urls"):
        if isinstance(contact["urls"], list):
            url_parts = []
            for url in contact["urls"]:
                if isinstance(url, dict):
                    url_value = url.get("value", "")
                    url_type = url.get("type", url.get("label", ""))
                    type_text = f" ({url_type})" if url_type else ""
                    url_parts.append(f"   • {url_value}{type_text}")
                else:
                    url_parts.append(f"   • {url}")
            parts.append(f"🌐 Website(s):\n" + "\n".join(url_parts))
    
    # Notes/Biography
    if contact.get("notes"):
        notes = contact["notes"]
        # Truncate very long notes
        if len(notes) > 200:
            notes = notes[:200] + "..."
        parts.append(f"📝 Notes: {notes}")
    
    # Relations
    if contact.get("relations"):
        if isinstance(contact["relations"], list):
            rel_parts = []
            for relation in contact["relations"]:
                if isinstance(relation, dict):
                    person = relation.get("person", "")
                    rel_type = relation.get("type", relation.get("label", ""))
                    type_text = f" ({rel_type})" if rel_type else ""
                    rel_parts.append(f"   • {person}{type_text}")
                else:
                    rel_parts.append(f"   • {relation}")
            parts.append(f"👥 Relations:\n" + "\n".join(rel_parts))
    
    # Events
    if contact.get("events"):
        if isinstance(contact["events"], list):
            event_parts = []
            for event in contact["events"]:
                if isinstance(event, dict):
                    event_type = event.get("type", event.get("label", "Event"))
                    event_date = event.get("date", {})
                    if isinstance(event_date, dict):
                        month = event_date.get("month", "")
                        day = event_date.get("day", "")
                        year = event_date.get("year", "")
                        if month and day:
                            date_str = f"{month:02d}-{day:02d}"
                            if year:
                                date_str = f"{year}-{date_str}"
                            event_parts.append(f"   • {event_type}: {date_str}")
                    else:
                        event_parts.append(f"   • {event_type}: {event_date}")
                else:
                    event_parts.append(f"   • {event}")
            if event_parts:
                parts.append(f"📅 Events:\n" + "\n".join(event_parts))
    
    # Custom fields
    if contact.get("customFields"):
        if isinstance(contact["customFields"], list):
            custom_parts = []
            for field in contact["customFields"]:
                if isinstance(field, dict):
                    key = field.get("key", "")
                    value = field.get("value", "")
                    if key and value:
                        custom_parts.append(f"   • {key}: {value}")
            if custom_parts:
                parts.append(f"🔧 Custom Fields:\n" + "\n".join(custom_parts))
    
    # Contact groups
    if contact.get("groups"):
        group_count = len(contact["groups"])
        if group_count > 0:
            parts.append(f"📂 Groups: {group_count} group(s)")
    
    # Photo
    if contact.get("photoUrl"):
        parts.append(f"📷 Photo: Available")
    
    # Resource ID for reference
    if contact.get("resourceName"):
        parts.append(f"🔗 ID: {contact['resourceName']}")
        
    return "\n".join(parts) if parts else "Contact has no details"

def format_contacts_list(contacts: List[Dict[str, Any]]) -> str:
    """Format a list of contacts into a readable string with enhanced display.
    
    Args:
        contacts: List of contact dictionaries
        
    Returns:
        Formatted string representation of the contacts list
    """
    if not contacts:
        return "No contacts found."
        
    if isinstance(contacts, dict) and "status" in contacts and contacts["status"] == "error":
        return f"Error: {contacts.get('message', 'Unknown error')}"
        
    parts = []
    
    for i, contact in enumerate(contacts, 1):
        # Create a compact summary for lists
        contact_summary = _format_contact_summary(contact, i)
        parts.append(contact_summary)
        parts.append("")  # Add blank line between contacts
        
    summary = f"📊 Found {len(contacts)} contact(s)"
    
    # Add statistics
    stats = _calculate_contact_stats(contacts)
    if stats:
        summary += f"\n📈 Statistics: {stats}"
    
    parts.append("=" * 50)
    parts.append(summary)
    
    return "\n".join(parts)

def _format_contact_summary(contact: Dict[str, Any], index: int) -> str:
    """Format a single contact as a summary for list display."""
    summary_parts = [f"Contact {index}:"]
    
    # Name
    name = contact.get("displayName") or f"{contact.get('givenName', '')} {contact.get('familyName', '')}".strip()
    if name:
        summary_parts.append(f"  📝 {name}")
    
    # Primary email
    if contact.get("emails") and isinstance(contact["emails"], list):
        primary_email = contact["emails"][0]
        if isinstance(primary_email, dict):
            summary_parts.append(f"  📧 {primary_email.get('value', '')}")
    elif contact.get("email"):
        summary_parts.append(f"  📧 {contact['email']}")
    
    # Primary phone
    if contact.get("phones") and isinstance(contact["phones"], list):
        primary_phone = contact["phones"][0]
        if isinstance(primary_phone, dict):
            summary_parts.append(f"  📱 {primary_phone.get('value', '')}")
    elif contact.get("phone"):
        summary_parts.append(f"  📱 {contact['phone']}")
    
    # Organization
    if contact.get("organization"):
        job_title = contact.get("jobTitle", "")
        org_text = f"{contact['organization']}"
        if job_title:
            org_text += f" - {job_title}"
        summary_parts.append(f"  🏢 {org_text}")
    
    return "\n".join(summary_parts)

def _calculate_contact_stats(contacts: List[Dict[str, Any]]) -> str:
    """Calculate and return statistics about the contacts list."""
    if not contacts:
        return ""
    
    stats = []
    
    # Count contacts with emails
    with_email = sum(1 for c in contacts if c.get('email') or (c.get('emails') and len(c['emails']) > 0))
    if with_email > 0:
        stats.append(f"{with_email} with email")
    
    # Count contacts with phones
    with_phone = sum(1 for c in contacts if c.get('phone') or (c.get('phones') and len(c['phones']) > 0))
    if with_phone > 0:
        stats.append(f"{with_phone} with phone")
    
    # Count contacts with organizations
    with_org = sum(1 for c in contacts if c.get('organization'))
    if with_org > 0:
        stats.append(f"{with_org} with organization")
    
    # Count contacts with addresses
    with_addr = sum(1 for c in contacts if c.get('addresses') and len(c['addresses']) > 0)
    if with_addr > 0:
        stats.append(f"{with_addr} with addresses")
    
    return ", ".join(stats)

def format_directory_people(people: List[Dict[str, Any]], query: Optional[str] = None) -> str:
    """Format a list of directory people into a readable string with enhanced display.
    
    Args:
        people: List of directory people dictionaries
        query: Optional search query used to find these people
        
    Returns:
        Formatted string representation of the directory people
    """
    if not people:
        if query:
            return f"No directory members found matching '{query}'."
        return "No directory members found."
    
    # Count how many users have emails
    users_with_email = sum(1 for user in people if user.get('email') or (user.get('emails') and len(user['emails']) > 0))
    
    # Format the results
    formatted_users = []
    for i, user in enumerate(people, 1):
        user_parts = []
        user_parts.append(f"📁 Directory Member {i}:")
        
        # Name
        if user.get('displayName'):
            user_parts.append(f"  📝 Name: {user['displayName']}")
        
        # Email
        if user.get('emails') and isinstance(user['emails'], list):
            primary_email = user['emails'][0]
            if isinstance(primary_email, dict):
                user_parts.append(f"  📧 Email: {primary_email.get('value', '')}")
        elif user.get('email'):
            user_parts.append(f"  📧 Email: {user['email']}")
        
        # Organization info
        if user.get('organization'):
            user_parts.append(f"  🏢 Organization: {user['organization']}")
        if user.get('department'):
            user_parts.append(f"  🏛️  Department: {user['department']}")
        if user.get('jobTitle'):
            user_parts.append(f"  💼 Title: {user['jobTitle']}")
        
        # Phone
        if user.get('phones') and isinstance(user['phones'], list):
            primary_phone = user['phones'][0]
            if isinstance(primary_phone, dict):
                user_parts.append(f"  📱 Phone: {primary_phone.get('value', '')}")
        elif user.get('phone'):
            user_parts.append(f"  📱 Phone: {user['phone']}")
        
        # Resource ID
        if user.get('resourceName'):
            user_parts.append(f"  🔗 ID: {user['resourceName']}")
        
        formatted_users.append("\n".join(user_parts))
    
    query_part = f" matching '{query}'" if query else ""
    summary = f"📊 Found {len(people)} directory member(s){query_part}. {users_with_email} have email addresses."
    formatted_users.append("=" * 50)
    formatted_users.append(summary)
    
    return "\n\n".join(formatted_users)
