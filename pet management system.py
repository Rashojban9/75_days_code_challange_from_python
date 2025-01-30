import sqlite3

# Database Manager
class DatabaseManager:
    @staticmethod
    def connect():
        return sqlite3.connect("pet_shelter.db")

    @staticmethod
    def initialize():
        with DatabaseManager.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS pets (
                id INTEGER PRIMARY KEY, name TEXT, species TEXT, breed TEXT, age INTEGER, health TEXT)''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS adopters (
                id INTEGER PRIMARY KEY, name TEXT, contact TEXT)''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS adoptions (
                id INTEGER PRIMARY KEY, pet_id INTEGER, adopter_id INTEGER,
                FOREIGN KEY(pet_id) REFERENCES pets(id), FOREIGN KEY(adopter_id) REFERENCES adopters(id))''')
            print("Database Ready.")

# Pet Model
class Pet:
    def __init__(self, pet_id, name, breed, age, health):
        self.id = pet_id
        self.name = name
        self.breed = breed
        self.age = age
        self.health = health

    def display_info(self):
        print(f"🐾 {self.name} | Breed: {self.breed} | Age: {self.age} | Health: {self.health}")

# Pet Service
class PetService:
    @staticmethod
    def add_pet(name, species, breed, age, health):
        with DatabaseManager.connect() as conn:
            conn.execute("INSERT INTO pets (name, species, breed, age, health) VALUES (?, ?, ?, ?, ?)",
                         (name, species, breed, age, health))
            print(f"{name} added to the shelter.")

    @staticmethod
    def get_all_pets():
        with DatabaseManager.connect() as conn:
            pets = conn.execute("SELECT * FROM pets").fetchall()
        return [Pet(*pet) for pet in pets]

    @staticmethod
    def search_pet_by_name(name):
        with DatabaseManager.connect() as conn:
            pets = conn.execute("SELECT * FROM pets WHERE name LIKE ?", ('%' + name + '%',)).fetchall()
        for pet in pets:
            print(f"🔎 Found: {pet[1]} | Breed: {pet[3]}")

    @staticmethod
    def update_pet_health(pet_id, new_health):
        with DatabaseManager.connect() as conn:
            conn.execute("UPDATE pets SET health = ? WHERE id = ?", (new_health, pet_id))
            print("Pet health updated.")

    @staticmethod
    def delete_pet(pet_id):
        with DatabaseManager.connect() as conn:
            conn.execute("DELETE FROM pets WHERE id = ?", (pet_id,))
            print("Pet removed.")

# Adopter Model
class Adopter:
    def __init__(self, adopter_id, name, contact):
        self.id = adopter_id
        self.name = name
        self.contact = contact

    def display_info(self):
        print(f"👤 {self.name} | Contact: {self.contact}")

# Adopter Service
class AdopterService:
    @staticmethod
    def register_adopter(name, contact):
        with DatabaseManager.connect() as conn:
            conn.execute("INSERT INTO adopters (name, contact) VALUES (?, ?)", (name, contact))
            print(f"{name} registered as adopter.")

    @staticmethod
    def view_all_adopters():
        with DatabaseManager.connect() as conn:
            adopters = conn.execute("SELECT * FROM adopters").fetchall()
        for adopter in adopters:
            print(f"👤 {adopter[1]} | Contact: {adopter[2]}")

# Adoption Service
class AdoptionService:
    @staticmethod
    def adopt_pet(pet_id, adopter_id):
        with DatabaseManager.connect() as conn:
            conn.execute("INSERT INTO adoptions (pet_id, adopter_id) VALUES (?, ?)", (pet_id, adopter_id))
            conn.execute("DELETE FROM pets WHERE id = ?", (pet_id,))
            print(f"✅ Pet ID {pet_id} adopted by Adopter ID {adopter_id}.")

# Main Application
def main():
    DatabaseManager.initialize()
    while True:
        print("\n📌 Pet Shelter Management")
        print("1. Register Pet\n2. View Pets\n3. Search Pet\n4. Update Pet Health\n5. Delete Pet\n6. Register Adopter\n7. View Adopters\n8. Adopt Pet\n9. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            name = input("Enter Name: ")
            species = input("Enter Species (dog/cat): ")
            breed = input("Enter Breed: ")
            age = int(input("Enter Age: "))
            health = input("Enter Health Status: ")
            PetService.add_pet(name, species, breed, age, health)

        elif choice == '2':
            pets = PetService.get_all_pets()
            for pet in pets:
                pet.display_info()

        elif choice == '3':
            name = input("Enter Name: ")
            PetService.search_pet_by_name(name)

        elif choice == '4':
            pet_id = int(input("Enter Pet ID: "))
            new_health = input("Enter New Health Status: ")
            PetService.update_pet_health(pet_id, new_health)

        elif choice == '5':
            pet_id = int(input("Enter Pet ID: "))
            PetService.delete_pet(pet_id)

        elif choice == '6':
            name = input("Enter Adopter Name: ")
            contact = input("Enter Contact: ")
            AdopterService.register_adopter(name, contact)

        elif choice == '7':
            AdopterService.view_all_adopters()

        elif choice == '8':
            pet_id = int(input("Enter Pet ID to Adopt: "))
            adopter_id = int(input("Enter Adopter ID: "))
            AdoptionService.adopt_pet(pet_id, adopter_id)

        elif choice == '9':
            print("Exiting... 🏠")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
