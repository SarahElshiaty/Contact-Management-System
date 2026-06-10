import os
import re
import shutil
from datetime import datetime

FILE_NAME = "project1.txt"
BACKUP_FOLDER = "backups"
CANCEL_WORDS = ["q", "quit"]


def menu():
    print("\n========== Contact Management System ==========")
    print("1. Add Contact")
    print("2. View All Contacts")
    print("3. Search Contact")
    print("4. Update Contact")
    print("5. Delete Contact")
    print("6. Save Contacts")
    print("7. Exit")
    print("===============================================")


def is_cancel(user_input):
    return user_input.strip().lower() in CANCEL_WORDS


def cancel_message():
    print("Operation cancelled. Returning to main menu.")


def is_valid_full_name(name):
    pattern = r"^[A-Za-z]+(?:[ '-][A-Za-z]+)+$"

    if not re.match(pattern, name.strip()):
        return False, "Enter first and last name using letters only."

    return True, ""


def is_valid_id(student_id):
    if not re.match(r"^S\d{8}$", student_id):
        return False, "ID must start with S followed by 8 digits. Example: S12345678"

    return True, ""


def is_valid_email(email):
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    if not re.match(pattern, email):
        return False, "Email format is invalid. Example: first.last@example.com"

    return True, ""


def normalize_phone(phone):
    phone = phone.strip().replace(" ", "").replace("-", "")

    if phone.startswith("0"):
        return None

    if phone.startswith("+"):
        return phone

    return "+" + phone


def is_valid_phone(phone):
    if phone is None:
        return False, "Phone number must include country code and should not start with 0."

    if not re.match(r"^\+\d{10,15}$", phone):
        return False, "Phone number must include country code. Example: +966XXXXXXXXX"

    return True, ""


def ask_valid_id(contacts=None, allow_existing=False):
    while True:
        user_input = input("Enter ID. It must start with S followed by 8 digits, or type q to cancel: ").strip()

        if is_cancel(user_input):
            cancel_message()
            return None

        student_id = user_input.upper()
        valid, message = is_valid_id(student_id)

        if not valid:
            print("Error:", message)
            continue

        if contacts is not None and not allow_existing and student_id in contacts:
            print("Error: A contact with this ID already exists. Please enter a different ID.")
            continue

        return student_id


def ask_valid_name():
    while True:
        name = input("Enter full name, first and last name, or type q to cancel: ").strip()

        if is_cancel(name):
            cancel_message()
            return None

        name = name.title()
        valid, message = is_valid_full_name(name)

        if not valid:
            print("Error:", message)
            continue

        return name


def ask_valid_email(contacts, current_id=None):
    while True:
        email = input("Enter email, or type q to cancel: ").strip()

        if is_cancel(email):
            cancel_message()
            return None

        email = email.lower()
        valid, message = is_valid_email(email)

        if not valid:
            print("Error:", message)
            continue

        if email_exists(contacts, email, current_id):
            print("Error: This email is already used by another contact. Please enter a different email.")
            continue

        return email


def ask_valid_phone(contacts, current_id=None):
    while True:
        phone_input = input("Enter phone number including country code, or type q to cancel: ").strip()

        if is_cancel(phone_input):
            cancel_message()
            return None

        phone = normalize_phone(phone_input)
        valid, message = is_valid_phone(phone)

        if not valid:
            print("Error:", message)
            continue

        if phone_exists(contacts, phone, current_id):
            print("Error: This phone number is already linked to another contact. Please enter a different phone number.")
            continue

        return phone


def create_backup():
    if os.path.exists(FILE_NAME):
        os.makedirs(BACKUP_FOLDER, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = os.path.join(BACKUP_FOLDER, f"project1_backup_{timestamp}.txt")
        shutil.copy(FILE_NAME, backup_name)


def load_contacts():
    contacts = {}

    if not os.path.exists(FILE_NAME):
        open(FILE_NAME, "w", encoding="utf-8").close()
        return contacts

    with open(FILE_NAME, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            if line == "":
                continue

            parts = [part.strip() for part in line.split(",")]

            if len(parts) != 4:
                print(f"Warning: Skipped corrupted line {line_number}.")
                continue

            student_id, name, email, phone = parts
            phone = normalize_phone(phone)

            valid_id, _ = is_valid_id(student_id)
            valid_name, _ = is_valid_full_name(name)
            valid_email, _ = is_valid_email(email)
            valid_phone, _ = is_valid_phone(phone)

            if valid_id and valid_name and valid_email and valid_phone:
                contacts[student_id] = {
                    "name": name,
                    "email": email,
                    "phone": phone
                }
            else:
                print(f"Warning: Skipped invalid contact on line {line_number}.")

    return contacts


def save_contacts(contacts):
    create_backup()

    with open(FILE_NAME, "w", encoding="utf-8") as file:
        for student_id in sorted(contacts):
            info = contacts[student_id]
            file.write(f"{student_id},{info['name']},{info['email']},{info['phone']}\n")

    print("Contacts saved successfully.")


def email_exists(contacts, email, current_id=None):
    for student_id, info in contacts.items():
        if student_id != current_id and info["email"].lower() == email.lower():
            return True
    return False


def phone_exists(contacts, phone, current_id=None):
    for student_id, info in contacts.items():
        if student_id != current_id and info["phone"] == phone:
            return True
    return False


def add_contact(contacts):
    print("\n--- Add New Contact ---")

    student_id = ask_valid_id(contacts)
    if student_id is None:
        return

    name = ask_valid_name()
    if name is None:
        return

    email = ask_valid_email(contacts)
    if email is None:
        return

    phone = ask_valid_phone(contacts)
    if phone is None:
        return

    contacts[student_id] = {
        "name": name,
        "email": email,
        "phone": phone
    }

    save_contacts(contacts)
    print("Contact added successfully.")


def view_contacts(contacts):
    print("\n--- All Contacts ---")

    if not contacts:
        print("No contacts available.")
        return

    for student_id in sorted(contacts):
        info = contacts[student_id]
        print("--------------------------------")
        print(f"ID: {student_id}")
        print(f"Name: {info['name']}")
        print(f"Email: {info['email']}")
        print(f"Phone: {info['phone']}")

    print("--------------------------------")


def search_contact(contacts):
    print("\n--- Search Contact ---")

    while True:
        keyword = input("Enter name, ID, email, or phone, or type q to cancel: ").strip()

        if is_cancel(keyword):
            cancel_message()
            return

        if keyword == "":
            print("Error: Search cannot be empty.")
            continue

        keyword = keyword.lower()
        break

    found = False

    for student_id in sorted(contacts):
        info = contacts[student_id]

        if (
            keyword in student_id.lower()
            or keyword in info["name"].lower()
            or keyword in info["email"].lower()
            or keyword in info["phone"]
        ):
            print("\nContact found:")
            print(f"ID: {student_id}")
            print(f"Name: {info['name']}")
            print(f"Email: {info['email']}")
            print(f"Phone: {info['phone']}")
            found = True

    if not found:
        print("No matching contact found.")


def update_contact(contacts):
    print("\n--- Update Contact ---")

    while True:
        user_input = input("Enter the ID of the contact to update, or type q to cancel: ").strip()

        if is_cancel(user_input):
            cancel_message()
            return

        student_id = user_input.upper()
        valid, message = is_valid_id(student_id)

        if not valid:
            print("Error:", message)
            continue

        if student_id not in contacts:
            print("Error: No contact found with this ID. Please try again.")
            continue

        break

    old_contact = contacts[student_id].copy()

    print("\nCurrent Contact:")
    print(f"Name: {old_contact['name']}")
    print(f"Email: {old_contact['email']}")
    print(f"Phone: {old_contact['phone']}")

    print("\nLeave a field empty if you do not want to change it.")
    print("Type q in any field to cancel the update.")

    updated_contact = old_contact.copy()
    changed = False

    new_name = input("Enter new full name: ").strip()

    if is_cancel(new_name):
        cancel_message()
        return

    if new_name != "":
        while True:
            new_name = new_name.title()
            valid, message = is_valid_full_name(new_name)

            if valid:
                updated_contact["name"] = new_name
                changed = True
                break

            print("Error:", message)
            new_name = input("Enter new full name again, or type q to cancel: ").strip()

            if is_cancel(new_name):
                cancel_message()
                return

    new_email = input("Enter new email: ").strip()

    if is_cancel(new_email):
        cancel_message()
        return

    if new_email != "":
        while True:
            new_email = new_email.lower()
            valid, message = is_valid_email(new_email)

            if not valid:
                print("Error:", message)
                new_email = input("Enter new email again, or type q to cancel: ").strip()

                if is_cancel(new_email):
                    cancel_message()
                    return

                continue

            if email_exists(contacts, new_email, student_id):
                print("Error: This email is already used by another contact.")
                new_email = input("Enter new email again, or type q to cancel: ").strip()

                if is_cancel(new_email):
                    cancel_message()
                    return

                continue

            updated_contact["email"] = new_email
            changed = True
            break

    new_phone = input("Enter new phone including country code: ").strip()

    if is_cancel(new_phone):
        cancel_message()
        return

    if new_phone != "":
        while True:
            new_phone = normalize_phone(new_phone)
            valid, message = is_valid_phone(new_phone)

            if not valid:
                print("Error:", message)
                new_phone = input("Enter new phone again, or type q to cancel: ").strip()

                if is_cancel(new_phone):
                    cancel_message()
                    return

                continue

            if phone_exists(contacts, new_phone, student_id):
                print("Error: This phone number is already linked to another contact.")
                new_phone = input("Enter new phone again, or type q to cancel: ").strip()

                if is_cancel(new_phone):
                    cancel_message()
                    return

                continue

            updated_contact["phone"] = new_phone
            changed = True
            break

    if not changed:
        print("No changes were made.")
        return

    print("\nUpdated Contact Preview:")
    print(f"Name: {updated_contact['name']}")
    print(f"Email: {updated_contact['email']}")
    print(f"Phone: {updated_contact['phone']}")

    confirm = input("Save these changes? (Y/N): ").strip().lower()

    if is_cancel(confirm):
        cancel_message()
        return

    if confirm == "y":
        contacts[student_id] = updated_contact
        save_contacts(contacts)
        print("Contact updated successfully.")
    else:
        print("Update cancelled.")


def delete_contact(contacts):
    print("\n--- Delete Contact ---")

    while True:
        user_input = input("Enter the ID of the contact to delete, or type q to cancel: ").strip()

        if is_cancel(user_input):
            cancel_message()
            return

        student_id = user_input.upper()
        valid, message = is_valid_id(student_id)

        if not valid:
            print("Error:", message)
            continue

        if student_id not in contacts:
            print("Error: No contact found with this ID. Please try again.")
            continue

        break

    print("\nContact found:")
    print(f"Name: {contacts[student_id]['name']}")
    print(f"Email: {contacts[student_id]['email']}")
    print(f"Phone: {contacts[student_id]['phone']}")

    confirm = input("Are you sure you want to delete this contact? (Y/N): ").strip().lower()

    if is_cancel(confirm):
        cancel_message()
        return

    if confirm == "y":
        del contacts[student_id]
        save_contacts(contacts)
        print("Contact deleted successfully.")
    else:
        print("Delete cancelled.")


def main():
    contacts = load_contacts()

    while True:
        menu()
        choice = input("Enter your choice from 1 to 7: ").strip()

        if choice == "1":
            add_contact(contacts)
        elif choice == "2":
            view_contacts(contacts)
        elif choice == "3":
            search_contact(contacts)
        elif choice == "4":
            update_contact(contacts)
        elif choice == "5":
            delete_contact(contacts)
        elif choice == "6":
            save_contacts(contacts)
        elif choice == "7":
            save_contacts(contacts)
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 7.")


if __name__ == "__main__":
    main()