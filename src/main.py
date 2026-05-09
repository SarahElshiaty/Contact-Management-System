def menu():
    print('Main Menu:')
    print('1. Add Contact')
    print('2. View Contact')
    print('3. Search Contact')
    print('4. Update Contact')
    print('5. Delete Contact')
    print('6. Save Contact to File')
    print('7. Exit')

def saveFile(contact):
    print('\tSave Contacts to File')
    fileName = input('Enter the file name to save contacts: ')
    try:
        with open(fileName, 'w') as file:
            for ID, contact_info in contact.items():
                file.write(f"{ID},{contact_info['name']},{contact_info['email']},{contact_info['phone']}\n")
        print(f'Contacts saved to {fileName} successfully')
    except Exception as e:
        print(f'An error occurred: {e}')

def addContact(contact):
    name = input('Enter the name: ')
    ID = input('Enter the ID: ')
    email = input('Enter the email: ')
    phone = input('Enter the phone number: ')

    while True:
        if not all(word.isalpha() for word in name.split()) or '@' not in email or '.' not in email or len(phone) != 12 or not phone.isnumeric():
            print('Invalid input. Please enter valid information.')
            break
        elif ID not in contact:
            contact[ID] = {'name': name, 'email': email, 'phone': phone}
            print('Successfully stored in file')
            saveFile(contact)
            break
        else:
            print('Contact with the same ID already exists. Try updating it.')
            break
    return contact

def viewContact(contact):
    if not contact:
        print("No contacts available.")
    for ID,contact_info in contact.items():
        print(f"ID: {ID}, Name: {contact_info['name']}, Email: {contact_info['email']}, Phone: {contact_info['phone']}")


def searchContact(contact):
    search_name = input('Enter the name you are searching for: ')
    for key, value in contact.items():
        if value['name'] == search_name:
            print(f"Contact found: {value}")
            break
    else:
        print(f"No contact found for {search_name}")

def deleteContact(contact):
    phone = input('Enter the phone number: ')
    for key, value in contact.items():
        if value['phone'] == phone:
            del contact[key]
            saveFile(contact)
            print(f'Contact with phone number "{phone}" deleted successfully.')
            break
    else:
        print(f'No contact found with the phone number "{phone}".')
    return contact

def updateContact(contact):
    ID = input("Enter the ID of the contact to update: ")
    if ID in contact:
        name = input("Enter the updated name: ")
        email = input("Enter the updated email: ")
        phone = input("Enter the updated phone number: ")
        contact[ID] = {'name': name, 'email': email, 'phone': phone}
        print(f'Contact updated successfully.')
        saveFile(contact)
    else:
        print(f'No contact found with the ID "{ID}".')
    return contact

def main(contact):
    while True:
        menu()
        choice = input("Enter your choice (1-7): ")
        if choice == '1':
            contact = addContact(contact)
        elif choice == '2':
            viewContact(contact)
        elif choice == '3':
            searchContact(contact)
        elif choice == '4':
            contact = updateContact(contact)
        elif choice == '5':
            contact = deleteContact(contact)
        elif choice == '6':
            saveFile(contact)
        elif choice == '7':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")

try:
    with open('project1.txt', 'r') as contact_file:
        file = contact_file.readlines()
        contact = {}
        for line in file:
                contact_info = {}
                lines = line.split('\t\t')
                contact_info['name'] = lines[0]
                contact_info['email'] = lines[2]
                contact_info['phone'] = lines[3].strip()
                contact[lines[1]] = contact_info
    main(contact)
except FileNotFoundError:
    print("Contacts file not found.")
