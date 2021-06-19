/* =====================
	CREATE DATABASE 
======================*/
USE [master]
GO

IF NOT EXISTS (SELECT name FROM master.dbo.sysdatabases 
WHERE name = 'HotelManagement')
CREATE DATABASE [HotelManagement] COLLATE Greek_CI_AI -- Collatiom : CI = Case Insensitive, AI = Accent Insensitive
GO

/* =====================
	CREATE ENTITIES 
======================*/
USE [HotelManagement]
GO

IF OBJECT_ID ('Customers', 'U') IS NULL
BEGIN
CREATE TABLE Customers
(
	Customer_ID int IDENTITY(1,1) PRIMARY KEY, 
	First_name varchar (50) not null, 
	Last_name varchar (50) not null, 
	Birth_date datetime,
	Issuing_authority varchar (50) not null, 
	Email varchar (50),
	Phone varchar (50)
)
END
GO

IF OBJECT_ID ('Reservations', 'U') IS NULL
BEGIN
CREATE TABLE Reservations
(
	Reservation_ID int IDENTITY(1,1) PRIMARY KEY, 
	Arrival datetime,
	Departure datetime, 
	Total_price float, 
	Payment_method varchar (50), 
	No_persons int
)
END
GO

IF OBJECT_ID ('Doors', 'U') IS NULL
BEGIN
CREATE TABLE Doors
(
	Door_ID int IDENTITY(1,1) PRIMARY KEY,
	Door_name varchar (50)
)
END
GO

IF OBJECT_ID ('HotelServices', 'U') IS NULL
BEGIN
CREATE TABLE HotelServices
(
	HotelService_ID int IDENTITY(1,1) PRIMARY KEY,
	HotelService_name varchar (50),
	Is_free bit,
	Price float
)
END
GO

IF OBJECT_ID ('HotelLocations', 'U') IS NULL
BEGIN
CREATE TABLE HotelLocations
(
	HotelLocation_ID int IDENTITY(1,1) PRIMARY KEY,
	Location_name varchar (50)
)
END
GO

IF OBJECT_ID ('HotelRooms', 'U') IS NULL
BEGIN
CREATE TABLE HotelRooms
(
	HotelRoom_ID int IDENTITY(1,1) PRIMARY KEY,
	Room_No int,
	Room_name varchar (20),
	No_beds int,
	Corridor_No int, 
	Floor_No int
)
END
GO

/* =====================
	CREATE ENTITY RELATIONS 
======================*/
IF OBJECT_ID ('ReservationCustomers', 'U') IS NULL
BEGIN
CREATE TABLE ReservationCustomers
(
	ReservationCustomer_ID int IDENTITY(1,1) PRIMARY KEY,
	Customer_ID int FOREIGN KEY REFERENCES Customers(Customer_ID),
	Reservation_ID int FOREIGN KEY REFERENCES Reservations(Reservation_ID),
	NFC_code int
)
END
GO

IF OBJECT_ID ('DoorAccessLog', 'U') IS NULL
BEGIN
CREATE TABLE DoorAccessLog
(
	DoorAccessLog_ID int IDENTITY(1,1) PRIMARY KEY,
	Entry_time datetime,
	Exit_time datetime,
	Service_desc varchar (255),
	ReservationCustomer_ID int FOREIGN KEY REFERENCES ReservationCustomers(ReservationCustomer_ID),
	Door_ID int FOREIGN KEY REFERENCES Doors(Door_ID)
)
END
GO

IF OBJECT_ID ('ReservationServices', 'U') IS NULL
BEGIN
CREATE TABLE ReservationServices
(
	ReservationService_ID int IDENTITY(1,1) PRIMARY KEY,
	Reservation_ID int FOREIGN KEY REFERENCES Reservations(Reservation_ID),
	HotelService_ID int FOREIGN KEY REFERENCES HotelServices(HotelService_ID)
)
END
GO

IF OBJECT_ID ('ReservationRooms', 'U') IS NULL
BEGIN
CREATE TABLE ReservationRooms
(
	ReservationRoom_ID int IDENTITY(1,1) PRIMARY KEY,
	Reservation_ID int FOREIGN KEY REFERENCES Reservations(Reservation_ID),
	HotelRoom_ID int FOREIGN KEY REFERENCES HotelRooms(HotelRoom_ID)
)
END
GO

/* =====================
	ADD ALL FOREIGN KEYS (1-N relations)
======================*/
ALTER TABLE Reservations 
ADD Reservation_maker_ID int FOREIGN KEY REFERENCES Customers(Customer_ID)
GO

ALTER TABLE Doors 
ADD HotelLocation_ID int FOREIGN KEY REFERENCES HotelLocations(HotelLocation_ID)
GO

ALTER TABLE HotelLocations
ADD HotelService_ID int FOREIGN KEY REFERENCES HotelServices(HotelService_ID)
GO

ALTER TABLE HotelRooms
ADD Door_ID int FOREIGN KEY REFERENCES Doors(Door_ID)
GO