CREATE VIEW services_visits AS
SELECT DISTINCT
HotelService_name,
First_name + ' ' + Last_name as Full_name,
Price,
Access_time as Time_of_access,
Location_name
FROM DoorAccessLog
INNER JOIN ReservationCustomers ON ReservationCustomers.ReservationCustomer_ID = DoorAccessLog.ReservationCustomer_ID
INNER JOIN Customers ON ReservationCustomers.Customer_ID = Customers.Customer_ID
INNER JOIN Doors ON Doors.Door_ID = DoorAccessLog.Door_ID
LEFT JOIN HotelLocations ON Doors.HotelLocation_ID = HotelLocations.HotelLocation_ID
INNER JOIN HotelServices ON HotelLocations.HotelService_ID = HotelServices.HotelService_ID
WHERE Type_of_access = 'Entry'  
