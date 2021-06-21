/* =====================
		QUERY 8
======================*/

CREATE VIEW customer_info AS 
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
