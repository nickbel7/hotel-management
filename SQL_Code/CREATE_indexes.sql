CREATE INDEX idx_reservation_id ON ReservationCustomers(Reservation_ID)
CREATE INDEX idx_nfc ON ReservationCustomers(NFC_Code)
CREATE INDEX idx_door_id ON DoorAccessLog(Door_ID)
CREATE INDEX idx_hotellocation_id ON Doors(HotelLocation_ID)
CREATE INDEX idx_door_id ON HotelRooms(Door_ID)

