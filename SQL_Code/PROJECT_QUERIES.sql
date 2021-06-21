/* =====================
	MAIN QUERIES 
======================*/

/* =====================
		QUERY 7
======================*/
SELECT HotelService_name
FROM HotelServices
WHERE HotelService_name NOT IN ('Elevator', 'Reception')

SELECT DISTINCT
Location_name
FROM DoorAccessLog
INNER JOIN ReservationCustomers ON ReservationCustomers.ReservationCustomer_ID = DoorAccessLog.ReservationCustomer_ID
INNER JOIN Doors ON Doors.Door_ID = DoorAccessLog.Door_ID
LEFT JOIN HotelLocations ON Doors.HotelLocation_ID = HotelLocations.HotelLocation_ID
INNER JOIN HotelServices ON HotelLocations.HotelService_ID = HotelServices.HotelService_ID
WHERE HotelService_name = 'Bar' 
AND Entry_time >= getdate() - 10 
AND Entry_time <= getdate() + 10
AND Price >= 10 
AND Price <= 30

SELECT DISTINCT
First_name + ' ' + Last_name as Full_name,
Entry_time as Time_of_entry,
Location_name
FROM DoorAccessLog
INNER JOIN ReservationCustomers ON ReservationCustomers.ReservationCustomer_ID = DoorAccessLog.ReservationCustomer_ID
INNER JOIN Customers ON ReservationCustomers.Customer_ID = Customers.Customer_ID
INNER JOIN Doors ON Doors.Door_ID = DoorAccessLog.Door_ID
LEFT JOIN HotelLocations ON Doors.HotelLocation_ID = HotelLocations.HotelLocation_ID
INNER JOIN HotelServices ON HotelLocations.HotelService_ID = HotelServices.HotelService_ID
WHERE Location_name = 'Bar 1'

/* =====================
		QUERY 8
======================*/
set statistics time on

--CREATE VIEW services_visits AS
SELECT DISTINCT
HotelService_name,
Location_name,
First_name + ' ' + Last_name as Full_name,
Price,
Entry_time as Time_of_entry,
Exit_time as Time_of_exit
FROM DoorAccessLog
INNER JOIN ReservationCustomers ON ReservationCustomers.ReservationCustomer_ID = DoorAccessLog.ReservationCustomer_ID
INNER JOIN Customers ON ReservationCustomers.Customer_ID = Customers.Customer_ID
INNER JOIN Doors ON Doors.Door_ID = DoorAccessLog.Door_ID
LEFT JOIN HotelLocations ON Doors.HotelLocation_ID = HotelLocations.HotelLocation_ID
INNER JOIN HotelServices ON HotelLocations.HotelService_ID = HotelServices.HotelService_ID 
ORDER BY HotelService_name

set statistics time off

set statistics time on

--CREATE VIEW customer_info AS 
SELECT DISTINCT 
First_name + ' ' + Last_name as Full_name,
datediff( YY, Customers.Birth_date, getdate()) as Age,
Issuing_authority, 
Email,
Phone
FROM ReservationCustomers
INNER JOIN Customers ON ReservationCustomers.Customer_ID = Customers.Customer_ID
INNER JOIN Reservations ON ReservationCustomers.Reservation_ID = Reservations.Reservation_ID
WHERE GETDATE() BETWEEN Arrival AND Departure

set statistics time off

/* =====================
		QUERY 9
======================*/

set statistics time on

SELECT Doors.Door_name, NFC_code, DoorAccessLog.Entry_time, DoorAccessLog.Exit_time
FROM DoorAccessLog
INNER JOIN ReservationCustomers ON ReservationCustomers.ReservationCustomer_ID = DoorAccessLog.ReservationCustomer_ID
INNER JOIN Doors ON Doors.Door_ID = DoorAccessLog.Door_ID
LEFT JOIN HotelLocations ON Doors.HotelLocation_ID = HotelLocations.HotelLocation_ID
LEFT JOIN HotelRooms ON Doors.Door_ID = HotelRooms.Door_ID
WHERE ReservationCustomers.NFC_code = 9297324
ORDER BY DoorAccessLog.Entry_time

set statistics time off

/* =====================
		QUERY 10
======================*/

set statistics time on 

SELECT DISTINCT ReservationCustomers.NFC_code, Customers.First_name, Customers.Last_name, Customers.Issuing_authority, Customers.Email, Customers.Phone
FROM
(SELECT DoorAccessLog.ReservationCustomer_ID, DoorAccessLog.Door_ID, Entry_time, Exit_time
FROM DoorAccessLog inner join ReservationCustomers on ReservationCustomers.ReservationCustomer_ID = DoorAccessLog.ReservationCustomer_ID
inner join Customers on Customers.Customer_ID = ReservationCustomers.Customer_ID
WHERE ReservationCustomers.NFC_code = 9297324) AS Covid
INNER JOIN DoorAccessLog ON DoorAccessLog.Door_ID = Covid.Door_ID
inner join ReservationCustomers on ReservationCustomers.ReservationCustomer_ID = DoorAccessLog.ReservationCustomer_ID
inner join Customers on Customers.Customer_ID = ReservationCustomers.Customer_ID
WHERE (DoorAccessLog.Entry_time > Covid.Entry_time AND DoorAccessLog.Entry_time <= DATEADD(HOUR, 1,Covid.Exit_time))
OR (Covid.Entry_time > DoorAccessLog.Entry_time AND Covid.Entry_time < DoorAccessLog.Exit_time)


set statistics time off

/* =====================
		QUERY 11
======================*/
-- Query 11 i --

SELECT HotelLocations.Location_name, COUNT(HotelLocations.Location_name) as times_visited
FROM DoorAccessLog
INNER JOIN ReservationCustomers ON ReservationCustomers.ReservationCustomer_ID = DoorAccessLog.ReservationCustomer_ID
INNER JOIN Doors ON Doors.Door_ID = DoorAccessLog.Door_ID
INNER JOIN HotelLocations ON Doors.HotelLocation_ID = HotelLocations.HotelLocation_ID
INNER JOIN Customers ON ReservationCustomers.Customer_ID = Customers.Customer_ID
WHERE datediff(YY, Customers.Birth_date, getdate())  BETWEEN '20' AND '40' AND DoorAccessLog.Access_time BETWEEN '2020-07-01' AND '2021-07-31' AND DoorAccessLog.Type_of_access = 'Entry'
GROUP BY HotelLocations.Location_name
ORDER BY times_visited DESC;

-- Query 11 ii --

SELECT HotelServices.HotelService_name, COUNT(HotelServices.HotelService_name) as serv_visited
FROM (DoorAccessLog
INNER JOIN ReservationCustomers ON ReservationCustomers.Customer_ID = DoorAccessLog.ReservationCustomer_ID)
INNER JOIN Doors ON Doors.Door_ID = DoorAccessLog.Door_ID
INNER JOIN HotelLocations ON Doors.HotelLocation_ID = HotelLocations.HotelLocation_ID
INNER JOIN HotelServices ON  HotelServices.HotelService_ID = HotelLocations.HotelService_ID
INNER JOIN Customers ON ReservationCustomers.Customer_ID = Customers.Customer_ID
WHERE datediff( YY, Customers.Birth_date, getdate())  BETWEEN '20' AND '40'AND DoorAccessLog.Access_time BETWEEN '2020-07-01' AND '2021-07-31' AND DoorAccessLog.Type_of_access = 'Entry'
GROUP BY HotelServices.HotelService_name
ORDER BY serv_visited DESC;



-- Query 11 iii --
SELECT  Serv_cust.HotelService_name, COUNT( Serv_cust.HotelService_name) AS VAL_OC
FROM 
	(SELECT DISTINCT  ReservationCustomers.Customer_ID, HotelServices.HotelService_name
	FROM DoorAccessLog
	INNER JOIN ReservationCustomers ON ReservationCustomers.Customer_ID = DoorAccessLog.ReservationCustomer_ID
	INNER JOIN Doors ON Doors.Door_ID = DoorAccessLog.Door_ID
	INNER JOIN HotelLocations ON Doors.HotelLocation_ID = HotelLocations.HotelLocation_ID
	INNER JOIN HotelServices ON  HotelServices.HotelService_ID = HotelLocations.HotelService_ID) AS Serv_cust
	GROUP BY Serv_cust.HotelService_name
	ORDER BY VAL_OC DESC;
