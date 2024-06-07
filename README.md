# CSS475FinalProject | Pool Reservation

## Running the code
Here is how to run the the database locally:

      git clone https://github.com/timmynugyen/CSS475FinalProject/edit/main/README.md
      cd CSS475FinalProject
      python manage.py runserver

Go to the link listed (it should probably be http://127.0.0.1:8000/ or http://127.0.0.1:8080/)

To access the admin section, go to the subdirectory /admin of the link. Login information should be displayed. The user is "admin", password is "pass123word456".

## Function definitions

**Customer** 
      A model representing a customer.

**Attributes:**

first_name (CharField): The customer's first name. Maximum length is 40 characters.
last_name (CharField): The customer's last name. Maximum length is 40 characters.
email (EmailField): The customer's email address. Maximum length is 40 characters. Must be unique.
phone_number (CharField): The customer's phone number. Maximum length is 10 characters. Can be null or blank.

**Methods:**

getFirstName(): Returns the first name of the customer.
Returns: str

getLastName(): Returns the last name of the customer.
Returns: str

getEmail(): Returns the email of the customer.
Returns: str

getPhoneNumber(): Returns the phone number of the customer.
Returns: str

__str__(): Returns the string representation of the customer.
Returns: str (formatted as "first_name last_name")
___________________________________________________________

**TimeSlot**
      A model representing a time slot for reservations.

**Attributes:**
start_time (DateTimeField): The start time of the time slot.
end_time (DateTimeField): The end time of the time slot.

**Methods:**
getStartTime(): Returns the start time of the time slot.
Returns: datetime

getEndTime(): Returns the end time of the time slot.
Returns: datetime

__str__(): Returns the string representation of the time slot.
Returns: str (formatted as "Starts: start_time, Ends: end_time")
____________________________________________________________________________________________________________

**RoomOption**
    A model representing room options for reservations.
    
**Attributes:**
room_name (IntegerField): The type of room selected. Choices are defined in RoomTypes.
attendees (IntegerField): The number of attendees. Default is 0.
timeslot (ForeignKey): The associated time slot for the room option.
special_orders (TextField): Any special orders or requests for the room option.

**Methods:**
clean(): Validates the maximum number of attendees.
Raises: ValidationError if attendees exceed the maximum allowed for the selected room.

getAttendees(): Returns the number of attendees.
Returns: int

getTimeSlot(): Returns the associated time slot.
Returns: TimeSlot

getSpecialOrder(): Returns the special orders.
Returns: str

__str__(): Returns the string representation of the room option.
Returns: str (room name)

Constants:
MAX_ATTENDEES: A dictionary mapping room types to their maximum number of attendees.
___________________________________________________________________________________________________________________

**PoolOption**
    A model representing pool options for reservations.

**Attributes:**
pool_name (IntegerField): The type of pool selected. Choices are defined in PoolTypes.
attendees (IntegerField): The number of attendees. Default is 0.
timeslot (ForeignKey): The associated time slot for the pool option.
special_orders (TextField): Any special orders or requests for the pool option.

**Methods:**
clean(): Validates the maximum number of attendees.
Raises: ValidationError if attendees exceed the maximum allowed for the selected pool.

getAttendees(): Returns the number of attendees.
Returns: int

getTimeSlot(): Returns the associated time slot.
Returns: TimeSlot

getSpecialOrder(): Returns the special orders.
Returns: str

__str__(): Returns the string representation of the pool option.
Returns: str (pool name)

Constants:
MAX_ATTENDEES: A dictionary mapping pool types to their maximum number of attendees.
________________________________________________________________________________________________

**ServiceType**
A model representing the type of service, which can include room options and/or pool options.

**Attributes:**
room_option (ForeignKey): The associated room option. Can be null or blank.
pool_option (ForeignKey): The associated pool option. Can be null or blank.

**Methods:**
getid(): Returns the ID of the service type.
Returns: int

__str__(): Returns the string representation of the service type.
Returns: str (formatted as "Service Type Room: room_option, Pool: pool_option")

__________________________________________________________________________________

**Service**
    A model representing a service, which includes multiple service types.
    
**Attributes:**
service_type (ManyToManyField): The service types included in the service.

**Methods:**
__str__(): Returns the string representation of the service.
Returns: str (formatted as "Service ID: id")
___________________________________________________________

**Reservation**
A model representing a reservation made by a customer.

**Attributes:**
customer (ForeignKey): The customer making the reservation.
is_exclusive (BooleanField): Indicates if the reservation is exclusive. Default is False.
service (ManyToManyField): The services included in the reservation.

**Methods:**
cost(): Calculates the total cost of the reservation.
Returns: float

__str__(): Returns the string representation of the reservation.
Returns: str (formatted as "Reservation for customer at timeslot")

Meta Class:
unique_together: Ensures that a customer cannot have more than one reservation in the same time slot.


