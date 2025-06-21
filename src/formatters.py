"""Formatting utilities for Google Contacts data display."""

from typing import Any, Dict, List, Optional


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
        return "Error: " + contact.get("message", "Unknown error")

    parts = []

    # Format basic contact information
    parts.extend(_format_contact_names(contact))
    parts.extend(_format_contact_info(contact))
    parts.extend(_format_professional_info(contact))
    parts.extend(_format_address_info(contact))
    parts.extend(_format_personal_info(contact))
    parts.extend(_format_additional_info(contact))

    return "\n".join(parts) if parts else "Contact has no details"


def _format_contact_names(contact: Dict[str, Any]) -> List[str]:
    """Format name-related fields for a contact."""
    parts = []

    # Name information
    if "displayName" in contact and contact["displayName"]:
        parts.append("📝 Name: " + contact["displayName"])
    elif "givenName" in contact or "familyName" in contact:
        name_parts = []
        if contact.get("givenName"):
            name_parts.append(contact["givenName"])
        if contact.get("familyName"):
            name_parts.append(contact["familyName"])
        if name_parts:
            parts.append("📝 Name: " + " ".join(name_parts))

    # Nickname
    if contact.get("nickname"):
        parts.append("🏷️  Nickname: " + contact["nickname"])

    return parts


def _format_contact_info(contact: Dict[str, Any]) -> List[str]:
    """Format contact information (emails, phones) for a contact."""
    parts = []

    # Email addresses
    if contact.get("emails"):
        if isinstance(contact["emails"], list):
            email_parts = []
            for email in contact["emails"]:
                if isinstance(email, dict):
                    label = email.get("label", email.get("type", ""))
                    label_text = " (" + label + ")" if label else ""
                    email_parts.append("   • " + email.get("value", "") + label_text)
                else:
                    email_parts.append("   • " + email)
            parts.append("📧 Email(s):\n" + "\n".join(email_parts))
    elif contact.get("email"):
        parts.append("📧 Email: " + contact["email"])

    # Phone numbers
    if contact.get("phones"):
        if isinstance(contact["phones"], list):
            phone_parts = []
            for phone in contact["phones"]:
                if isinstance(phone, dict):
                    label = phone.get("label", phone.get("type", ""))
                    label_text = " (" + label + ")" if label else ""
                    phone_parts.append("   • " + phone.get("value", "") + label_text)
                else:
                    phone_parts.append("   • " + phone)
            parts.append("📱 Phone(s):\n" + "\n".join(phone_parts))
    elif contact.get("phone"):
        parts.append("📱 Phone: " + contact["phone"])

    return parts


def _format_professional_info(contact: Dict[str, Any]) -> List[str]:
    """Format professional information for a contact."""
    parts = []

    # Professional information
    if contact.get("organization") or contact.get("jobTitle") or contact.get("department"):
        org_parts = []
        if contact.get("organization"):
            org_parts.append("Company: " + contact["organization"])
        if contact.get("jobTitle"):
            org_parts.append("Title: " + contact["jobTitle"])
        if contact.get("department"):
            org_parts.append("Department: " + contact["department"])
        parts.append("🏢 Work:\n   • " + "\n   • ".join(org_parts))

    return parts


def _format_address_info(contact: Dict[str, Any]) -> List[str]:
    """Format address information for a contact."""
    parts = []

    # Addresses
    if contact.get("addresses"):
        if isinstance(contact["addresses"], list):
            addr_parts = []
            for addr in contact["addresses"]:
                if isinstance(addr, dict):
                    formatted_addr = addr.get("formatted", "")
                    addr_type = addr.get("type", addr.get("label", ""))
                    type_text = " (" + addr_type + ")" if addr_type else ""
                    addr_parts.append("   • " + formatted_addr + type_text)
                else:
                    addr_parts.append("   • " + addr)
            parts.append("🏠 Address(es):\n" + "\n".join(addr_parts))

    return parts


def _format_personal_info(contact: Dict[str, Any]) -> List[str]:
    """Format personal information for a contact."""
    parts = []

    # Birthday
    if contact.get("birthday"):
        birthday = contact["birthday"]
        if isinstance(birthday, dict):
            year = birthday.get("year", "")
            month = birthday.get("month", "")
            day = birthday.get("day", "")
            if year and month and day:
                parts.append("🎂 Birthday: " + f"{year}-{month:02d}-{day:02d}")
            elif month and day:
                parts.append("🎂 Birthday: " + f"{month:02d}-{day:02d}")
        else:
            parts.append("🎂 Birthday: " + birthday)

    # Websites/URLs
    if contact.get("urls"):
        if isinstance(contact["urls"], list):
            url_parts = []
            for url in contact["urls"]:
                if isinstance(url, dict):
                    url_value = url.get("value", "")
                    url_type = url.get("type", url.get("label", ""))
                    type_text = " (" + url_type + ")" if url_type else ""
                    url_parts.append("   • " + url_value + type_text)
                else:
                    url_parts.append("   • " + url)
            parts.append("🌐 Website(s):\n" + "\n".join(url_parts))

    # Notes/Biography
    if contact.get("notes"):
        notes = contact["notes"]
        # Truncate very long notes
        if len(notes) > 200:
            notes = notes[:200] + "..."
        parts.append("📝 Notes: " + notes)

    return parts


def _format_additional_info(contact: Dict[str, Any]) -> List[str]:
    """Format additional information for a contact."""
    parts = []

    # Format different sections
    parts.extend(_format_relations_info(contact))
    parts.extend(_format_events_info(contact))
    parts.extend(_format_custom_fields_info(contact))
    parts.extend(_format_metadata_info(contact))

    return parts


def _format_relations_info(contact: Dict[str, Any]) -> List[str]:
    """Format relations information for a contact."""
    parts = []
    if contact.get("relations"):
        if isinstance(contact["relations"], list):
            rel_parts = []
            for relation in contact["relations"]:
                if isinstance(relation, dict):
                    person = relation.get("person", "")
                    rel_type = relation.get("type", relation.get("label", ""))
                    type_text = " (" + rel_type + ")" if rel_type else ""
                    rel_parts.append("   • " + person + type_text)
                else:
                    rel_parts.append("   • " + relation)
            parts.append("👥 Relations:\n" + "\n".join(rel_parts))
    return parts


def _format_events_info(contact: Dict[str, Any]) -> List[str]:
    """Format events information for a contact."""
    parts = []
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
                            event_parts.append("   • " + event_type + ": " + date_str)
                    else:
                        event_parts.append("   • " + event_type + ": " + event_date)
                else:
                    event_parts.append("   • " + event)
            if event_parts:
                parts.append("📅 Events:\n" + "\n".join(event_parts))
    return parts


def _format_custom_fields_info(contact: Dict[str, Any]) -> List[str]:
    """Format custom fields information for a contact."""
    parts = []
    if contact.get("customFields"):
        if isinstance(contact["customFields"], list):
            custom_parts = []
            for field in contact["customFields"]:
                if isinstance(field, dict):
                    key = field.get("key", "")
                    value = field.get("value", "")
                    if key and value:
                        custom_parts.append("   • " + key + ": " + value)
            if custom_parts:
                parts.append("🔧 Custom Fields:\n" + "\n".join(custom_parts))
    return parts


def _format_metadata_info(contact: Dict[str, Any]) -> List[str]:
    """Format metadata information for a contact."""
    parts = []

    # Contact groups
    if contact.get("groups"):
        group_count = len(contact["groups"])
        if group_count > 0:
            parts.append("📂 Groups: " + str(group_count) + " group(s)")

    # Photo
    if contact.get("photoUrl"):
        parts.append("📷 Photo: Available")

    # Resource ID for reference
    if contact.get("resourceName"):
        parts.append("🔗 ID: " + contact["resourceName"])

    return parts


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
        return "Error: " + contacts.get("message", "Unknown error")

    parts = []

    for i, contact in enumerate(contacts, 1):
        # Create a compact summary for lists
        contact_summary = _format_contact_summary(contact, i)
        parts.append(contact_summary)
        parts.append("")  # Add blank line between contacts

    summary = "📊 Found " + str(len(contacts)) + " contact(s)"

    # Add statistics
    stats = _calculate_contact_stats(contacts)
    if stats:
        summary += "\n📈 Statistics: " + stats

    parts.append("=" * 50)
    parts.append(summary)

    return "\n".join(parts)


def _format_contact_summary(contact: Dict[str, Any], index: int) -> str:
    """Format a single contact as a summary for list display."""
    summary_parts = ["Contact " + str(index) + ":"]

    # Name
    name = (
        contact.get("displayName")
        or f"{contact.get('givenName', '')} {contact.get('familyName', '')}".strip()
    )
    if name:
        summary_parts.append("  📝 " + name)

    # Primary email
    if contact.get("emails") and isinstance(contact["emails"], list):
        primary_email = contact["emails"][0]
        if isinstance(primary_email, dict):
            summary_parts.append("  📧 " + primary_email.get("value", ""))
    elif contact.get("email"):
        summary_parts.append("  📧 " + contact["email"])

    # Primary phone
    if contact.get("phones") and isinstance(contact["phones"], list):
        primary_phone = contact["phones"][0]
        if isinstance(primary_phone, dict):
            summary_parts.append("  📱 " + primary_phone.get("value", ""))
    elif contact.get("phone"):
        summary_parts.append("  📱 " + contact["phone"])

    # Organization
    if contact.get("organization"):
        job_title = contact.get("jobTitle", "")
        org_text = contact["organization"]
        if job_title:
            org_text += " - " + job_title
        summary_parts.append("  🏢 " + org_text)

    return "\n".join(summary_parts)


def _calculate_contact_stats(contacts: List[Dict[str, Any]]) -> str:
    """Calculate and return statistics about the contacts list."""
    if not contacts:
        return ""

    stats = []

    # Count contacts with emails
    with_email = sum(
        1 for c in contacts if c.get("email") or (c.get("emails") and len(c["emails"]) > 0)
    )
    if with_email > 0:
        stats.append(str(with_email) + " with email")

    # Count contacts with phones
    with_phone = sum(
        1 for c in contacts if c.get("phone") or (c.get("phones") and len(c["phones"]) > 0)
    )
    if with_phone > 0:
        stats.append(str(with_phone) + " with phone")

    # Count contacts with organizations
    with_org = sum(1 for c in contacts if c.get("organization"))
    if with_org > 0:
        stats.append(str(with_org) + " with organization")

    # Count contacts with addresses
    with_addr = sum(1 for c in contacts if c.get("addresses") and len(c["addresses"]) > 0)
    if with_addr > 0:
        stats.append(str(with_addr) + " with addresses")

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
            return "No directory members found matching '" + query + "'."
        return "No directory members found."

    # Count how many users have emails
    users_with_email = _count_users_with_email(people)

    # Format the results
    formatted_users = []
    for i, user in enumerate(people, 1):
        user_parts = _format_single_directory_user(user, i)
        formatted_users.append("\n".join(user_parts))

    # Add summary
    query_part = " matching '" + query + "'" if query else ""
    summary = (
        "📊 Found "
        + str(len(people))
        + " directory member(s)"
        + query_part
        + ". "
        + str(users_with_email)
        + " have email addresses."
    )
    formatted_users.append("=" * 50)
    formatted_users.append(summary)

    return "\n\n".join(formatted_users)


def _count_users_with_email(people: List[Dict[str, Any]]) -> int:
    """Count how many users in the list have email addresses."""
    return sum(
        1
        for user in people
        if user.get("email") or (user.get("emails") and len(user["emails"]) > 0)
    )


def _format_single_directory_user(user: Dict[str, Any], index: int) -> List[str]:
    """Format a single directory user's information."""
    user_parts = []
    user_parts.append("📁 Directory Member " + str(index) + ":")

    # Name
    if user.get("displayName"):
        user_parts.append("  📝 Name: " + user["displayName"])

    # Email
    if user.get("emails") and isinstance(user["emails"], list):
        primary_email = user["emails"][0]
        if isinstance(primary_email, dict):
            user_parts.append("  📧 Email: " + primary_email.get("value", ""))
    elif user.get("email"):
        user_parts.append("  📧 Email: " + user["email"])

    # Organization info
    if user.get("organization"):
        user_parts.append("  🏢 Organization: " + user["organization"])
    if user.get("department"):
        user_parts.append("  🏛️  Department: " + user["department"])
    if user.get("jobTitle"):
        user_parts.append("  💼 Title: " + user["jobTitle"])

    # Phone
    if user.get("phones") and isinstance(user["phones"], list):
        primary_phone = user["phones"][0]
        if isinstance(primary_phone, dict):
            user_parts.append("  📱 Phone: " + primary_phone.get("value", ""))
    elif user.get("phone"):
        user_parts.append("  📱 Phone: " + user["phone"])

    # Resource ID
    if user.get("resourceName"):
        user_parts.append("  🔗 ID: " + user["resourceName"])

    return user_parts


def format_contact_group(group: Dict[str, Any]) -> str:
    """Format a contact group dictionary into a readable string.

    Args:
        group: Dictionary containing contact group information

    Returns:
        Formatted string representation of the contact group
    """
    if not group:
        return "No contact group data available"

    parts = []

    # Group name and type
    name = group.get("name", "Unnamed Group")
    group_type = group.get("groupType", "").replace("_", " ").title()
    if group_type:
        parts.append("📂 " + name + " (" + group_type + ")")
    else:
        parts.append("📂 " + name)

    # Member count
    member_count = group.get("memberCount", 0)
    if member_count > 0:
        parts.append("👥 Members: " + str(member_count))
    else:
        parts.append("👥 Members: None")

    # Update time
    if group.get("updateTime"):
        parts.append("🕒 Last Updated: " + group["updateTime"])

    # Resource ID
    if group.get("resourceName"):
        parts.append("🔗 ID: " + group["resourceName"])

    # Client data
    if group.get("clientData"):
        client_data_parts = []
        for data in group["clientData"]:
            key = data.get("key", "")
            value = data.get("value", "")
            if key and value:
                client_data_parts.append("   • " + key + ": " + value)
        if client_data_parts:
            parts.append("🔧 Custom Data:\n" + "\n".join(client_data_parts))

    # Member resource names (if included)
    if group.get("memberResourceNames"):
        member_names = group["memberResourceNames"]
        if len(member_names) <= 5:
            parts.append("📋 Member IDs: " + ", ".join(member_names))
        else:
            parts.append(
                "📋 Member IDs: "
                + ", ".join(member_names[:5])
                + " ... (and "
                + str(len(member_names) - 5)
                + " more)"
            )

    return "\n".join(parts)


def format_contact_groups_list(groups: List[Dict[str, Any]]) -> str:
    """Format a list of contact groups into a readable string.

    Args:
        groups: List of contact group dictionaries

    Returns:
        Formatted string representation of the contact groups list
    """
    if not groups:
        return "No contact groups found."

    parts = []

    # Separate user and system groups
    user_groups = [g for g in groups if g.get("groupType") == "USER_CONTACT_GROUP"]
    system_groups = [g for g in groups if g.get("groupType") == "SYSTEM_CONTACT_GROUP"]

    if user_groups:
        parts.append("👤 USER CONTACT GROUPS:")
        parts.append("")
        for i, group in enumerate(user_groups, 1):
            group_summary = _format_contact_group_summary(group, i)
            parts.append(group_summary)
            parts.append("")

    if system_groups:
        parts.append("🔧 SYSTEM CONTACT GROUPS:")
        parts.append("")
        for i, group in enumerate(system_groups, 1):
            group_summary = _format_contact_group_summary(group, i, is_system=True)
            parts.append(group_summary)
            parts.append("")

    # Summary statistics
    total_members = sum(group.get("memberCount", 0) for group in groups)
    parts.append("=" * 50)
    parts.append(
        "📊 Summary: "
        + str(len(groups))
        + " total groups ("
        + str(len(user_groups))
        + " user, "
        + str(len(system_groups))
        + " system)"
    )
    parts.append("👥 Total contacts across all groups: " + str(total_members))

    return "\n".join(parts)


def _format_contact_group_summary(
    group: Dict[str, Any], index: int, is_system: bool = False
) -> str:
    """Format a single contact group as a summary for list display."""
    icon = "🔧" if is_system else "📂"
    summary_parts = [icon + " Group " + str(index) + ": " + group.get("name", "Unnamed")]

    # Member count
    member_count = group.get("memberCount", 0)
    summary_parts.append("  👥 " + str(member_count) + " member(s)")

    # Resource name
    if group.get("resourceName"):
        summary_parts.append("  🔗 " + group["resourceName"])

    return "\n".join(summary_parts)


def format_group_membership_result(result: Dict[str, Any], operation: str = "modify") -> str:
    """Format the result of adding/removing contacts from a group.

    Args:
        result: Result dictionary from group membership operation
        operation: Type of operation (add/remove)

    Returns:
        Formatted string representation of the operation result
    """
    if not result:
        return f"No result from group membership {operation} operation."

    parts = []

    if result.get("success"):
        parts.append(f"✅ Group membership {operation} operation completed successfully!")

        if "added_count" in result:
            parts.append(f"📥 Added {result['added_count']} contact(s) to group")
        elif "removed_count" in result:
            parts.append(f"📤 Removed {result['removed_count']} contact(s) from group")
    else:
        parts.append(f"❌ Group membership {operation} operation failed.")

    # Handle not found contacts
    if result.get("not_found"):
        not_found = result["not_found"]
        parts.append("⚠️  " + str(len(not_found)) + " contact(s) not found:")
        for contact in not_found:
            parts.append("   • " + contact)

    # Handle contacts that couldn't be modified
    if result.get("could_not_add"):
        parts.append("⚠️  Could not add " + str(len(result["could_not_add"])) + " contact(s)")
    elif result.get("could_not_remove"):
        could_not_remove = result["could_not_remove"]
        parts.append(
            "⚠️  Could not remove " + str(len(could_not_remove)) + " contact(s) (last group):"
        )
        for contact in could_not_remove:
            parts.append("   • " + contact)

    return "\n".join(parts)
