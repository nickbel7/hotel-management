from flask import Flask, render_template, request
import pypyodbc, re, json, os
from datetime import datetime

app = Flask(__name__)

sql_user = 'sa'
sql_password = '2019'
sql_server_name = 'BELLOS-DELL-G3\SQL2019'
sql_database_name = 'HotelManagement'
connection = pypyodbc.connect('Driver={SQL Server};Server='+sql_server_name+';Database='+sql_database_name+';uid='+sql_user+';pwd='+sql_password)

@app.route("/hello/<name>")
def hello_there(name):
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")

    # Filter the name argument to letters only using regular expressions. URL arguments
    # can contain arbitrary text, so we restrict to safe characters only.
    match_object = re.match("[a-zA-Z]+", name)

    if match_object:
        clean_name = match_object.group(0)
    else:
        clean_name = "Friend"

    content = "Hello there, " + clean_name + "! It's " + formatted_now
    return content

#########
# CUSTOMERS VIEW
##############
@app.route("/customers", methods=['GET', 'POST'])
def customers_view():
    rs = connection.cursor()   

    queryString = """
    SELECT DISTINCT 
    First_name + ' ' + Last_name as Full_name,
    datediff( YY, Birth_date, getdate()) as Age,
    Issuing_authority, 
    Email,
    Phone
    FROM Customers
    """
    rs.execute(queryString)
    customers = rs.fetchall()

    return render_template("customers.html", customers=customers)

#########
# SERVICE PURCHASES
##############
@app.route("/purchases", methods=['GET', 'POST'])
def purchases_view():
    rs = connection.cursor()   

    queryString = """
    SELECT HotelService_name
    FROM HotelServices
    WHERE HotelService_name NOT IN ('Elevator', 'Reception')
    """
    rs.execute(queryString)
    serviceTypes = rs.fetchall()

    queryString = """
    SELECT DISTINCT
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
    WHERE HotelService_name = '{}'
    ORDER BY Time_of_entry DESC
    """
    purchases = []
    for item in serviceTypes:
        print(item[0])
        rs.execute(queryString.format(item[0]))
        purchasesBuff = rs.fetchall()
        purchases.append(
            {
                'title': item[0],
                'items': purchasesBuff,
            } 
        )

    return render_template("purchases.html", purchases=purchases)

#########
# SERVICE ACCESSES
##############
@app.route("/accesses", methods=['GET', 'POST'])
def accesses_view():
    rs = connection.cursor()   

    queryString = """
    SELECT HotelService_name
    FROM HotelServices
    WHERE HotelService_name NOT IN ('Elevator', 'Reception')
    """
    rs.execute(queryString)
    serviceTypes = rs.fetchall()

    selected_service_type = str(request.form.get('select-service-type'))
    if (selected_service_type == 'None'):
        selected_service_type = '\'\''

    min_price = str(request.form.get('min-price'))
    if (min_price != 'None' and min_price != ''):
        min_price_query = 'AND Price >= ' + str(min_price) + ' '
    else:
        min_price_query = ''

    max_price = str(request.form.get('max-price'))
    if (max_price != 'None' and max_price != ''):
        max_price_query = 'AND Price <= ' + str(max_price) + ' '
    else:
        max_price_query = ''

    min_time = request.form.get('min-time')
    if (min_time != None):
        min_time = datetime.strptime(min_time, '%Y-%m-%dT%H:%M')
        min_time_query = 'AND Entry_time >= \'' + datetime.strftime(min_time, '%m-%d-%Y %H:%M:%S') + '\' '
    else:
        min_time_query = ''

    max_time = request.form.get('max-time')
    if (max_time != None):
        max_time = datetime.strptime(max_time, '%Y-%m-%dT%H:%M')
        max_time_query = 'AND Entry_time <= \'' + datetime.strftime(max_time, '%m-%d-%Y %H:%M:%S') + '\' '
    else:
        max_time_query = ''

    queryString = """
    SELECT DISTINCT
    Location_name
    FROM DoorAccessLog
    INNER JOIN ReservationCustomers ON ReservationCustomers.ReservationCustomer_ID = DoorAccessLog.ReservationCustomer_ID
    INNER JOIN Doors ON Doors.Door_ID = DoorAccessLog.Door_ID
    LEFT JOIN HotelLocations ON Doors.HotelLocation_ID = HotelLocations.HotelLocation_ID
    INNER JOIN HotelServices ON HotelLocations.HotelService_ID = HotelServices.HotelService_ID
    WHERE HotelService_name = '{}'
    """.format(selected_service_type)
    queryString = queryString + min_price_query + max_price_query + min_time_query + max_time_query
    rs.execute(queryString)
    visitedServices = rs.fetchall()

    selected_service = str(request.form.get('select-service'))
    if (selected_service == 'None'):
        selected_service = ''

    queryString = """
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
    WHERE Location_name = '{}'
    """.format(selected_service)
    rs.execute(queryString)
    visits = rs.fetchall()

    return render_template("accesses.html", serviceTypes=serviceTypes, visitedServices=visitedServices, selected_service_type=selected_service_type, visits=visits, selected_service=selected_service)

#########
# COVID DASHBOARD
##############
@app.route("/covid",methods=["GET", "POST"])
def covid(): 
    rs = connection.cursor() 
    selected_nfc = str(request.form.get('select-nfc-code'))
    if (selected_nfc == 'None'):
        selected_nfc = ''
    nfc_query = """SELECT ReservationCustomers.NFC_code 
    FROM ReservationCustomers
    """
    rs.execute(nfc_query)
    nfcs = rs.fetchall()
    myquery = """SELECT Doors.Door_name, NFC_code, DoorAccessLog.Entry_time, DoorAccessLog.Exit_time
    FROM DoorAccessLog
    INNER JOIN ReservationCustomers ON ReservationCustomers.ReservationCustomer_ID = DoorAccessLog.ReservationCustomer_ID
    INNER JOIN Doors ON Doors.Door_ID = DoorAccessLog.Door_ID
    LEFT JOIN HotelLocations ON Doors.HotelLocation_ID = HotelLocations.HotelLocation_ID
    LEFT JOIN HotelRooms ON Doors.Door_ID = HotelRooms.Door_ID
    WHERE ReservationCustomers.NFC_code = '{}'
    ORDER BY DoorAccessLog.Entry_time""".format(selected_nfc)
    rs.execute(myquery)
    covid_custs = rs.fetchall()

    queryString = """
    SELECT DISTINCT ReservationCustomers.NFC_code, Customers.First_name, Customers.Last_name, Customers.Issuing_authority, Customers.Email, Customers.Phone
    FROM
    (SELECT DoorAccessLog.ReservationCustomer_ID, DoorAccessLog.Door_ID, Entry_time, Exit_time
    FROM DoorAccessLog inner join ReservationCustomers on ReservationCustomers.ReservationCustomer_ID = DoorAccessLog.ReservationCustomer_ID
    inner join Customers on Customers.Customer_ID = ReservationCustomers.Customer_ID
    WHERE ReservationCustomers.NFC_code = '{}') AS Covid
    INNER JOIN DoorAccessLog ON DoorAccessLog.Door_ID = Covid.Door_ID
    inner join ReservationCustomers on ReservationCustomers.ReservationCustomer_ID = DoorAccessLog.ReservationCustomer_ID
    inner join Customers on Customers.Customer_ID = ReservationCustomers.Customer_ID
    WHERE (DoorAccessLog.Entry_time > Covid.Entry_time AND DoorAccessLog.Entry_time <= DATEADD(HOUR, 1,Covid.Exit_time))
    OR (Covid.Entry_time > DoorAccessLog.Entry_time AND Covid.Entry_time < DoorAccessLog.Exit_time)
    """.format(selected_nfc)
    rs.execute(queryString)
    suspects = rs.fetchall()

    return render_template("covid.html",covid_custs = covid_custs, nfcs = nfcs,selected_nfc =json.dumps(selected_nfc), suspects=suspects)

#########
# DASHBOARD VIEW
##############
@app.route("/", methods=["GET", "POST"])
def dashboard():
    rs = connection.cursor() 
    min_age = request.form.get('min_age')
    if (min_age != None and min_age != ''):
        min_age_query = 'datediff(YY, Customers.Birth_date, getdate()) BETWEEN ' + str(min_age) + ' '
    else: 
        min_age_query = 'datediff(YY, Customers.Birth_date, getdate()) BETWEEN 0 '

    max_age = request.form.get('max_age')
    if (max_age != None and max_age != ''):
        max_age_query = 'AND ' + str(max_age) + ' ' + 'AND '
    else: 
        max_age_query = 'AND 200 AND '
    min_date = request.form.get('min_date')
    if (min_date != None and min_date != ''):
        min_date = datetime.strptime(min_date, '%Y-%m-%dT%H:%M')
    else: 
        min_date = datetime.strptime('2020-01-01', '%Y-%m-%d')
    min_date_query = 'DoorAccessLog.Entry_time BETWEEN \'' + datetime.strftime(min_date, '%m-%d-%Y %H:%M:%S') + '\' '

    max_date = request.form.get('max_date')
    if (max_date != None and max_date != ''):
        max_date = datetime.strptime(max_date, '%Y-%m-%dT%H:%M')
    else: 
        max_date = datetime.strptime('2022-01-01', '%Y-%m-%d')
    max_date_query = 'AND \'' + datetime.strftime(max_date, '%m-%d-%Y %H:%M:%S') + '\' '

    end_query = """GROUP BY HotelLocations.Location_name
    ORDER BY times_visited DESC;""" 

    my_query_ = """SELECT HotelLocations.Location_name, COUNT(HotelLocations.Location_name) as times_visited
    FROM DoorAccessLog
    INNER JOIN ReservationCustomers ON ReservationCustomers.ReservationCustomer_ID = DoorAccessLog.ReservationCustomer_ID
    INNER JOIN Doors ON Doors.Door_ID = DoorAccessLog.Door_ID
    INNER JOIN HotelLocations ON Doors.HotelLocation_ID = HotelLocations.HotelLocation_ID
    INNER JOIN Customers ON ReservationCustomers.Customer_ID = Customers.Customer_ID
    WHERE """  
    my_query1 = my_query_ + min_age_query + max_age_query + min_date_query +max_date_query + end_query
    rs.execute(my_query1)
    results = rs.fetchall()
    Names = [] 
    Data = []
    for result in results: 
        Names.append(result[0])
        Data.append(result[1])
    my_query_2 = """SELECT HotelServices.HotelService_name, COUNT(HotelServices.HotelService_name) as serv_visited
    FROM DoorAccessLog INNER JOIN ReservationCustomers ON ReservationCustomers.Customer_ID = DoorAccessLog.ReservationCustomer_ID
    INNER JOIN Doors ON Doors.Door_ID = DoorAccessLog.Door_ID
    INNER JOIN HotelLocations ON Doors.HotelLocation_ID = HotelLocations.HotelLocation_ID
    INNER JOIN HotelServices ON  HotelServices.HotelService_ID = HotelLocations.HotelService_ID
    INNER JOIN Customers ON ReservationCustomers.Customer_ID = Customers.Customer_ID
    WHERE """ 
    end_query2 = """GROUP BY HotelServices.HotelService_name
    ORDER BY serv_visited DESC;""" 
    my_query2 = my_query_2 + min_age_query + max_age_query + min_date_query +max_date_query + end_query2
    rs.execute(my_query2)
    res_2 = rs.fetchall() 
    Services = [] 
    Answers = [] 
    for ans in res_2: 
        Services.append(ans[0])
        Answers.append(ans[1])
    my_query3 = """SELECT  Serv_cust.HotelService_name, COUNT( Serv_cust.HotelService_name) AS VAL_OC
    FROM (SELECT DISTINCT  ReservationCustomers.Customer_ID, HotelServices.HotelService_name
    FROM DoorAccessLog
    INNER JOIN ReservationCustomers ON ReservationCustomers.Customer_ID = DoorAccessLog.ReservationCustomer_ID
    INNER JOIN Doors ON Doors.Door_ID = DoorAccessLog.Door_ID
    INNER JOIN HotelLocations ON Doors.HotelLocation_ID = HotelLocations.HotelLocation_ID
    INNER JOIN HotelServices ON  HotelServices.HotelService_ID = HotelLocations.HotelService_ID) AS Serv_cust
    GROUP BY Serv_cust.HotelService_name
    ORDER BY VAL_OC DESC; """
    rs.execute(my_query3) 
    res_3 = rs.fetchall()
    Serv_name = [] 
    Val_oc = [] 
    for ans in res_3:
        Serv_name.append(ans[0])
        Val_oc.append(ans[1])

    return render_template("dashboard.html",results = results,names = json.dumps(Names),datas = json.dumps(Data),
    services = json.dumps(Services),answers = json.dumps(Answers),
    Serv_name = json.dumps(Serv_name), Val_oc = json.dumps(Val_oc)) 

#########
# RESERVATION FORM
##############
@app.route("/reservation", methods=["GET", "POST"])
def reservation():
    rs = connection.cursor()
    
    IssuingAuthority = str(request.form.get('inputIssuingAuthority'))
    Arrival = str(request.form.get('inputArrivalDate'))
    if(Arrival != 'None'):
        Arrival = datetime.strptime(Arrival, '%Y-%m-%d')
    Departure = str(request.form.get('inputDeprartureDate'))
    if(Departure != 'None'):
        Departure = datetime.strptime(Departure, '%Y-%m-%d')
    Total_price = '0'
    Payment_method =  str(request.form.get('inputPaymentMethod'))
    No_persons = str(request.form.get('inputNumberOfPerson'))
    First_name = str(request.form.get('inputFirstName'))
    Last_name = str(request.form.get('inputLastName'))
    Birth_date = str(request.form.get('inputBirthDate'))
    if(Birth_date != 'None'):
        Birth_date = datetime.strptime(Birth_date, '%Y-%m-%d')
    Email = str(request.form.get('inputEmailAddress'))
    Phone = str(request.form.get('inputPhoneNumber'))

    if (Arrival == 'None' or Departure == 'None' or Payment_method == 'None' or No_persons == 'None'):
        return render_template("reservation.html")

    queryString = """
    SELECT Customer_ID
    FROM Customers
    WHERE Customers.Issuing_authority = '{}'
    """.format(IssuingAuthority)
    rs.execute(queryString)
    newCustomer_ID = rs.fetchall()

    if(newCustomer_ID == []):
        queryString = """
        select max(Customers.Customer_ID)
        from Customers
        """
        rs.execute(queryString)
        newCustomer_ID = rs.fetchall()[0][0]+1
    else:
        newCustomer_ID = newCustomer_ID[0][0]

    Reservation_maker_ID = newCustomer_ID
    Customer_ID = newCustomer_ID

    queryString = """
    INSERT INTO Customers
           (First_name
           ,Last_name
           ,Birth_date
           ,Issuing_authority
           ,Email
           ,Phone)
     VALUES
           ('{}'
           ,'{}'
           ,'{}'
           ,'{}'
           ,'{}'
           ,'{}')
    """.format(First_name, Last_name, Birth_date, IssuingAuthority, Email, Phone)
    rs.execute(queryString)
    connection.commit()
    
    queryString = """
    INSERT INTO [dbo].[Reservations]
            ([Arrival]
            ,[Departure]
            ,[Total_price]
            ,[Payment_method]
            ,[No_persons]
            ,[Reservation_maker_ID])
        VALUES
            ('{}'
            ,'{}'
            ,'{}'
            ,'{}'
            ,'{}'
            ,'{}')
    """.format(Arrival, Departure, Total_price, Payment_method, No_persons, Reservation_maker_ID)
    rs.execute(queryString)
    connection.commit()
    
    queryString = """
        select max(ReservationCustomers.Reservation_ID)
        from ReservationCustomers
        """
    rs.execute(queryString) 
    Reservation_ID = rs.fetchall()[0][0]+1
    NumberOfBeds = str(request.form.get("inputNumberOfBeds"))
    
    queryString = """ SELECT max(ReservationRooms.HotelRoom_ID)
    FROM ReservationRooms
    INNER JOIN HotelRooms ON HotelRooms.HotelRoom_ID = ReservationRooms.HotelRoom_ID
    WHERE HotelRooms.No_beds = '{}'""".format(NumberOfBeds)
    rs.execute(queryString)
    HotelRoom_ID = rs.fetchall()[0][0]+1

    queryString = """
    INSERT INTO ReservationRooms
           ([Reservation_ID]
           ,[HotelRoom_ID])
     VALUES
           ('{}',
           '{}')
           """.format(Reservation_ID,HotelRoom_ID)
    rs.execute(queryString)
    connection.commit()

    queryString = """
        select max(ReservationCustomers.NFC_code)
        from ReservationCustomers
        """
    rs.execute(queryString) 
    NFC_code = rs.fetchall()[0][0]+1

    queryString = """
    INSERT INTO ReservationCustomers
           (Customer_ID
           ,Reservation_ID
           ,NFC_code)
     VALUES
           ('{}'
           ,'{}'
           ,'{}')
    """.format(Customer_ID, Reservation_ID, NFC_code)
    rs.execute(queryString) 
    connection.commit()
    Sauna = str(request.form.get('Sauna'))
    Gym = str(request.form.get('Gym'))
    Workroom = str(request.form.get('Workroom'))
    ServiceList = [Sauna,Gym,Workroom]
    for HotelService_ID in ServiceList: 
        if HotelService_ID != 'None': 
            queryString = """
            INSERT INTO ReservationServices
                ([Reservation_ID]
                ,[HotelService_ID])
            VALUES
                ('{}'
                ,'{}')
            """.format(Reservation_ID,HotelService_ID)
            rs.execute(queryString) 
            connection.commit()

    return render_template("reservation.html")

#########
# CUSTOMER FORM
##############
@app.route("/customers/customer-edit", methods=["GET", "POST"])
def customer_edit():
    rs = connection.cursor() 

    current_customer_id = request.args.get("customer_id")
    if (current_customer_id == None):
        current_customer_id = ''

    queryString = """
    SELECT *
    FROM Customers
    WHERE Issuing_authority = '{}'
    """.format(current_customer_id)
    rs.execute(queryString)
    current_customer = rs.fetchall()
    if (current_customer != []):
        birth_date = datetime.strftime(current_customer[0].get('birth_date'), '%Y-%m-%d')
    else:
        birth_date = '1970-01-01'

    First_name = str(request.form.get('inputFirstName'))
    Last_name = str(request.form.get('inputLastName'))
    Birth_date = str(request.form.get('inputBirthDate'))
    if (Birth_date != 'None'):
        Birth_date = datetime.strptime(Birth_date, '%Y-%m-%d')
    #     min_time = datetime.strptime(min_time, '%Y-%m-%dT%H:%M')
    #     min_time_query = 'AND Entry_time >= \'' + datetime.strftime(min_time, '%m-%d-%Y %H:%M:%S') + '\' '
    IssuingAuthority = str(request.form.get('inputIssuingAuthority'))
    Email = str(request.form.get('inputEmailAddress'))
    Phone = str(request.form.get('inputPhoneNumber'))

    if (First_name != 'None' and Last_name != 'None' and Birth_date != 'None' and IssuingAuthority != 'None' and Email != 'None' and Phone != 'None'):
        queryString = """
        IF '{}' IN (select Issuing_authority from Customers)
            UPDATE Customers
            SET First_name = '{}'
                ,Last_name = '{}'
                ,Birth_date = '{}'
                ,Issuing_authority = '{}'
                ,Email = '{}'
                ,Phone = '{}'
            WHERE Issuing_authority = '{}'
        ELSE
            INSERT INTO Customers
                (First_name
                ,Last_name
                ,Birth_date
                ,Issuing_authority
                ,Email
                ,Phone)
            VALUES
                ('{}'
                ,'{}'
                ,'{}'
                ,'{}'
                ,'{}'
                ,'{}')
        """.format(IssuingAuthority,
                First_name,  #repeat for update
                Last_name, 
                Birth_date, 
                IssuingAuthority, 
                Email, 
                Phone,
                IssuingAuthority,
                First_name,  #repeat for insert
                Last_name, 
                Birth_date, 
                IssuingAuthority, 
                Email, 
                Phone)
        rs.execute(queryString)
        connection.commit()

    return render_template("customer-form.html", current_customer=current_customer, birth_date=birth_date)    

