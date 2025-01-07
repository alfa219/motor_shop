import requests
import json

API_BASE_URL = "http://127.0.0.1:8000"

def print_response(response):
    """Print response data in a formatted way."""
    if response.status_code in [200, 201]:
        print(json.dumps(response.json(), indent=4))
    else:
        print(f"Error {response.status_code}: {response.text}")

def create_motor():
    """Create a new motor."""
    print("\nEnter motor details:")
    name = input("Name: ")
    brand = input("Brand: ")
    category = input("Category (Sport/Matic/Bebek): ")
    
    while True:
        try:
            engine_capacity = int(input("Engine Capacity (cc): "))
            break  
        except ValueError:
            print("Invalid input. Engine capacity must be an integer. Please try again.")
    
 
    while True:
        try:
            year_of_production = int(input("Year of Production: "))
            break 
        except ValueError:
            print("Invalid input. Year of production must be an integer. Please try again.")
    

    while True:
        try:
            price = float(input("Price: "))
            break  
        except ValueError:
            print("Invalid input. Price must be a number. Please try again.")
    
    payload = {
        "name": name,
        "brand": brand,
        "category": category,
        "engine_capacity": engine_capacity,
        "year_of_production": year_of_production,
        "price": price
    }
    response = requests.post(f"{API_BASE_URL}/motors", json=payload)
    print_response(response)

def get_all_motors():
    """Retrieve all motors."""
    response = requests.get(f"{API_BASE_URL}/motors")
    print_response(response)

def get_motor_by_id():
    """Retrieve a motor by ID."""
    while True:
        try:
            motor_id = int(input("Enter Motor ID: "))
            break 
        except ValueError:
            print("Invalid input. Motor ID must be an integer. Please try again.")
    
    response = requests.get(f"{API_BASE_URL}/motors/{motor_id}")
    print_response(response)

def update_motor():
    """Update a motor."""
    while True:
        try:
            motor_id = int(input("Enter Motor ID to update: "))
            break  
        except ValueError:
            print("Invalid input. Motor ID must be an integer. Please try again.")
    
    print("\nEnter updated motor details:")
    name = input("Name: ")
    brand = input("Brand: ")
    category = input("Category (Sport/Matic/Bebek): ")
    
 
    while True:
        try:
            engine_capacity = int(input("Engine Capacity (cc): "))
            break 
        except ValueError:
            print("Invalid input. Engine capacity must be an integer. Please try again.")
    

    while True:
        try:
            year_of_production = int(input("Year of Production: "))
            break 
        except ValueError:
            print("Invalid input. Year of production must be an integer. Please try again.")
    

    while True:
        try:
            price = float(input("Price: "))
            break  
        except ValueError:
            print("Invalid input. Price must be a number. Please try again.")
    
    payload = {
        "name": name,
        "brand": brand,
        "category": category,
        "engine_capacity": engine_capacity,
        "year_of_production": year_of_production,
        "price": price
    }
    response = requests.put(f"{API_BASE_URL}/motors/{motor_id}", json=payload)
    print_response(response)

def delete_motor():
    """Delete a motor."""
    while True:
        try:
            motor_id = int(input("Enter Motor ID to delete: "))
            break
        except ValueError:
            print("Invalid input. Motor ID must be an integer. Please try again.")
    
    response = requests.delete(f"{API_BASE_URL}/motors/{motor_id}")
    print_response(response)


def create_accessory():
    """Create a new accessory."""
    print("\nEnter accessory details:")
    name = input("Name: ")
    type = input("Type (e.g., Helmet, Gloves): ")
    description = input("Description: ")
    

    while True:
        try:
            price = float(input("Price: "))
            break 
        except ValueError:
            print("Invalid input. Price must be a number. Please try again.")
    
    payload = {
        "name": name,
        "type": type,
        "description": description,
        "price": price
    }
    response = requests.post(f"{API_BASE_URL}/accessories", json=payload)
    print_response(response)

def get_all_accessories():
    """Retrieve all accessories."""
    response = requests.get(f"{API_BASE_URL}/accessories")
    print_response(response)

def get_accessory_by_id():
    """Retrieve an accessory by ID."""
    while True:
        try:
            accessory_id = int(input("Enter Accessory ID: "))
            break  
        except ValueError:
            print("Invalid input. Accessory ID must be an integer. Please try again.")
    
    response = requests.get(f"{API_BASE_URL}/accessories/{accessory_id}")
    print_response(response)

def update_accessory():
    """Update an accessory."""
    while True:
        try:
            accessory_id = int(input("Enter Accessory ID to update: "))
            break 
        except ValueError:
            print("Invalid input. Accessory ID must be an integer. Please try again.")
    
    print("\nEnter updated accessory details:")
    name = input("Name: ")
    type = input("Type (e.g., Helmet, Gloves): ")
    description = input("Description: ")
    

    while True:
        try:
            price = float(input("Price: "))
            break  
        except ValueError:
            print("Invalid input. Price must be a number. Please try again.")
    
    payload = {
        "name": name,
        "type": type,
        "description": description,
        "price": price
    }
    response = requests.put(f"{API_BASE_URL}/accessories/{accessory_id}", json=payload)
    print_response(response)

def delete_accessory():
    """Delete an accessory."""
    while True:
        try:
            accessory_id = int(input("Enter Accessory ID to delete: "))
            break  
        except ValueError:
            print("Invalid input. Accessory ID must be an integer. Please try again.")
    
    response = requests.delete(f"{API_BASE_URL}/accessories/{accessory_id}")
    print_response(response)

# Main menu
def main():
    """Main menu for managing motors and accessories."""
    while True:
        print("\nMenu:")
        print("1. Add Motor")
        print("2. View All Motors")
        print("3. View Motor by ID")
        print("4. Update Motor")
        print("5. Delete Motor")
        print("6. Add Accessory")
        print("7. View All Accessories")
        print("8. View Accessory by ID")
        print("9. Update Accessory")
        print("10. Delete Accessory")
        print("11. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            create_motor()
        elif choice == "2":
            get_all_motors()
        elif choice == "3":
            get_motor_by_id()
        elif choice == "4":
            update_motor()
        elif choice == "5":
            delete_motor()
        elif choice == "6":
            create_accessory()
        elif choice == "7":
            get_all_accessories()
        elif choice == "8":
            get_accessory_by_id()
        elif choice == "9":
            update_accessory()
        elif choice == "10":
            delete_accessory()
        elif choice == "11":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
