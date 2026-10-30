import json
import os
import re

FILE_NAME = "contacts.json"


# ---------- File handling ----------
def load_contacts():
    if not os.path.exists(FILE_NAME):
        return []
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def save_contacts(contacts):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(contacts, f, indent=4)


def valid_phone(phone):
    return phone.isdigit() and 7 <= len(phone) <= 15


def valid_email(email):
    return email == "" or re.fullmatch(r"[\w.+-]+@[\w-]+\.[\w.-]+", email) is not None


def phone_exists(contacts, phone, skip_index=None):
    return any(c["phone"] == phone for i, c in enumerate(contacts) if i != skip_index)

def line(char="=", n=60):
    print(char * n)


def print_header(title):
    print()
    line()
    print(title.center(60))
    line()


def print_contact(index, c):
    print(f"[{index}] Name   : {c['name']}")
    print(f"    Phone  : {c['phone']}")
    print(f"    Email  : {c['email'] or '-'}")
    print(f"    Address: {c['address'] or '-'}")
    line("-")


def choose_contact(contacts, action):
    view_contacts(contacts, show_details=False)
    if not contacts:
        return None
    choice = input(f"\nEnter contact number to {action} (or press Enter to cancel): ").strip()
    if not choice:
        return None
    if choice.isdigit() and 1 <= int(choice) <= len(contacts):
        return int(choice) - 1
    print("Invalid number.")
    return None

def add_contact(contacts):
    print_header("ADD NEW CONTACT")
    name = input("Name    : ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    phone = input("Phone   : ").strip()
    if not valid_phone(phone):
        print("Invalid phone number. Use 7-15 digits only.")
        return
    if phone_exists(contacts, phone):
        print("A contact with this phone number already exists.")
        return

    email = input("Email   (optional): ").strip()
    if not valid_email(email):
        print("Invalid email format.")
        return

    address = input("Address (optional): ").strip()

    contacts.append({"name": name, "phone": phone, "email": email, "address": address})
    save_contacts(contacts)
    print(f"\nContact '{name}' added successfully!")


def view_contacts(contacts, show_details=True):
    print_header("CONTACT LIST")
    if not contacts:
        print("No contacts saved yet.")
        return
    print(f"{'No.':<5}{'Name':<30}{'Phone':<15}")
    line("-")
    for i, c in enumerate(contacts, start=1):
        print(f"{i:<5}{c['name']:<30}{c['phone']:<15}")
    line("-")
    print(f"Total contacts: {len(contacts)}")


def view_full_contact(contacts):
    idx = choose_contact(contacts, "view in detail")
    if idx is not None:
        print()
        print_contact(idx + 1, contacts[idx])


def search_contact(contacts):
    print_header("SEARCH CONTACT")
    query = input("Enter name or phone number to search: ").strip().lower()
    if not query:
        print("Search term cannot be empty.")
        return
    results = [
        (i, c) for i, c in enumerate(contacts, start=1)
        if query in c["name"].lower() or query in c["phone"]
    ]
    if not results:
        print("No matching contacts found.")
        return
    print(f"\n{len(results)} contact(s) found:\n")
    for i, c in results:
        print_contact(i, c)


def update_contact(contacts):
    print_header("UPDATE CONTACT")
    idx = choose_contact(contacts, "update")
    if idx is None:
        return

    c = contacts[idx]
    print("\nPress Enter to keep the current value.\n")

    name = input(f"Name [{c['name']}]: ").strip() or c["name"]

    phone = input(f"Phone [{c['phone']}]: ").strip() or c["phone"]
    if not valid_phone(phone):
        print("Invalid phone number. Update cancelled.")
        return
    if phone_exists(contacts, phone, skip_index=idx):
        print("Another contact already uses this phone number. Update cancelled.")
        return

    email_in = input(f"Email [{c['email'] or '-'}]: ").strip()
    email = email_in if email_in else c["email"]
    if not valid_email(email):
        print("Invalid email format. Update cancelled.")
        return

    address_in = input(f"Address [{c['address'] or '-'}]: ").strip()
    address = address_in if address_in else c["address"]

    contacts[idx] = {"name": name, "phone": phone, "email": email, "address": address}
    save_contacts(contacts)
    print("\nContact updated successfully!")


def delete_contact(contacts):
    print_header("DELETE CONTACT")
    idx = choose_contact(contacts, "delete")
    if idx is None:
        return
    confirm = input(f"Delete '{contacts[idx]['name']}'? (y/n): ").strip().lower()
    if confirm == "y":
        removed = contacts.pop(idx)
        save_contacts(contacts)
        print(f"\nContact '{removed['name']}' deleted.")
    else:
        print("Deletion cancelled.")

def show_menu():
    print_header("CONTACT BOOK")
    print("  1. Add Contact")
    print("  2. View Contact List")
    print("  3. View Contact Details")
    print("  4. Search Contact")
    print("  5. Update Contact")
    print("  6. Delete Contact")
    print("  7. Exit")
    line("-")


def main():
    contacts = load_contacts()
    actions = {
        "1": add_contact,
        "2": view_contacts,
        "3": view_full_contact,
        "4": search_contact,
        "5": update_contact,
        "6": delete_contact,
    }

    while True:
        show_menu()
        choice = input("Enter your choice (1-7): ").strip()
        if choice == "7":
            print("\nThank you for using Contact Book 😊 ")
            break
        action = actions.get(choice)
        if action:
            action(contacts)
        else:
            print("Invalid choice. Please enter a number from 1 to 7.")
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()