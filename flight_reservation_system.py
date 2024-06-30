import mysql.connector
from mysql.connector import Error

# MySQL connection parameters
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '12345678',
    'database': 'flight_reservation'
}

# Function to establish MySQL connection
def connect_database():
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            print('Connected to MySQL database')
            return conn
    except Error as e:
        print(f'Error: {e}')
        return None

# Function to display main menu
def display_main_menu():
    print("Flight Reservation System")
    print("1. Search Flights")
    print("2. Reserve Seat")
    print("3. View Bookings")
    print("4. Exit")

# Function to search flights
def search_flights(conn):
    departure_city = input("Enter Departure City: ")
    arrival_city = input("Enter Arrival City: ")

    query = f"SELECT * FROM flights WHERE departure_city='{departure_city}' AND arrival_city='{arrival_city}'"
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        flights = cursor.fetchall()
        
        if not flights:
            print("No flights found.")
        else:
            print("Flight ID\tFlight Number\tDeparture City\tArrival City\tDeparture Date\tAvailable Seats")
            for flight in flights:
                print("\t".join(map(str, flight)))
    except Error as e:
        print(f"Error: {e}")

# Function to reserve seat
def reserve_seat(conn):
    flight_id = input("Enter Flight ID to reserve seat: ")

    try:
        cursor = conn.cursor()
        
        # Check available seats
        cursor.execute(f"SELECT available_seats FROM flights WHERE flight_id={flight_id}")
        available_seats = cursor.fetchone()[0]
        
        if available_seats > 0:
            username = "user1"  # Example username
            insert_query = f"INSERT INTO bookings (user_id, flight_id) VALUES ((SELECT user_id FROM users WHERE username='{username}'), {flight_id})"
            cursor.execute(insert_query)
            conn.commit()

            # Update available seats
            update_query = f"UPDATE flights SET available_seats=available_seats-1 WHERE flight_id={flight_id}"
            cursor.execute(update_query)
            conn.commit()

            print("Seat booked successfully!")
        else:
            print("No available seats for this flight.")
    except Error as e:
        print(f"Error: {e}")

# Function to view bookings
def view_bookings(conn):
    username = "user1"  # Example username
    query = f"SELECT flights.flight_number, flights.departure_city, flights.arrival_city, flights.departure_date, bookings.booking_date FROM flights INNER JOIN bookings ON flights.flight_id = bookings.flight_id INNER JOIN users ON bookings.user_id = users.user_id WHERE users.username='{username}'"

    try:
        cursor = conn.cursor()
        cursor.execute(query)
        bookings = cursor.fetchall()

        if not bookings:
            print("No bookings found.")
        else:
            print("Flight Number\tDeparture City\tArrival City\tDeparture Date\tBooking Date")
            for booking in bookings:
                print("\t".join(map(str, booking)))
    except Error as e:
        print(f"Error: {e}")

# Main function
def main():
    conn = connect_database()
    if not conn:
        return
    
    while True:
        display_main_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            search_flights(conn)
        elif choice == '2':
            reserve_seat(conn)
        elif choice == '3':
            view_bookings(conn)
        elif choice == '4':
            print("Exiting the program. Thank you!")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

    conn.close()

if __name__ == "__main__":
    main()
