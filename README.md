# Hotel-Management
This is a project for the Databases class in NTUA Electrical and Computer Engineering Department 

## Tools used
![Python](https://img.shields.io/badge/python-v3.7+-red.svg)
![Dependencies](https://img.shields.io/badge/flask-v2.0.1-red)
![pypyodbc](https://img.shields.io/badge/pypyodbc-v1.3.4-red.svg)
![sqlserver](https://img.shields.io/badge/sql_server-v2019-yellow.svg)

## [Requirements](https://github.com/AlexandrosKyriakakis/DataBase/blob/master/requirements.txt)
- sql server 2019
- Flask 2.0.1
- pypyodbc 1.3.4

## ER-Diagram

![](https://github.com/AlexandrosKyriakakis/DataBase/blob/master/img/er-diagram.png?raw=true)

## Relational Model

![](https://github.com/nickbel7/hotel-management/blob/main/Diagrams(ERD%2CRelational)/RelationalDiagram.png?raw=true)

## Installation
1. At first, make sure you have installed sql server 2019 (express) on your computer.
2. Then, connect to the server throught a DBMS (preferably Microsoft SQL Management Studio) with sa (system administrator) credentials.

### Run the following sql queries inside the DMBS (at this spesific order !).

3. [CREATE_tables.sql](SQL_Code/CREATE_tables.sql) to create the database and the tables.
4. [CREATE_indexes.sql](SQL_Code/CREATE_indexes.sql) to create the indexes.
5. [CREATE_views_1.sql](SQL_Code/CREATE_views_1.sql) and [CREATE_views_2.sql](SQL_Code/CREATE_views_2.sql) to create the required views.
6. [past_price_trigger.sql](https://github.com/AlexandrosKyriakakis/DataBase/blob/master/sql/trigers/past_price_trigger.sql) to create the trigger for auto-update past prices.
7. [addStores.sql](https://github.com/AlexandrosKyriakakis/DataBase/blob/master/sql/addStores/addStores.sql) to add all the stores.

### Back in the terminal

8. Run,

```bash
	$ git clone https://github.com/AlexandrosKyriakakis/DataBase.git
	$ cd DataBase
	$ git clone https://github.com/AlexandrosKyriakakis/MarketDataset.git
```

9. Add your database credentials at the top '\*\*\*\*' of each of the following files,
   - [addCustomersAndPhone.py](https://github.com/AlexandrosKyriakakis/DataBase/blob/master/addData/addCustomersAndPhone.py)
   - [addProductsPastPricesHas.py](https://github.com/AlexandrosKyriakakis/DataBase/blob/master/addData/addProductsPastPricesHas.py)
   - [addTransactionsBought.py](https://github.com/AlexandrosKyriakakis/DataBase/blob/master/addData/addTransactionsBought.py)
   - [server_guest.py](https://github.com/AlexandrosKyriakakis/DataBase/blob/master/server_guest.py)
10. Run the following strictly at this order,

```bash
	$ pip3 install -r requirements.txt
	$ python3 ./addData/addCustomersAndPhone.py
	$ python3 ./addData/addProductsPastPricesHas.py
	$ python3 ./addData/addTransactionsBought.py
```

11. Now, that the database is full with random generated data, start the back-end server to finish the installation,

```bash
	$ python3 server_guest.py
```

12. Open your favorite browser and type <http://localhost:8587/> to preview the website.

## Sql Queries

Queries to construct database,

- [AlexJohnChris](https://github.com/AlexandrosKyriakakis/DataBase/tree/master/sql)
- [Indexes](https://github.com/AlexandrosKyriakakis/DataBase/tree/master/sql/Indexes)
- [Trigers](https://github.com/AlexandrosKyriakakis/DataBase/tree/master/sql/trigers)
- [Add Stores](https://github.com/AlexandrosKyriakakis/DataBase/tree/master/sql/addStores)

Here we show all the [queries](https://github.com/AlexandrosKyriakakis/DataBase/tree/master/sql) used in the site at each page,

- [SearchPerCondition](https://github.com/AlexandrosKyriakakis/DataBase/tree/master/sql/SearchPerCondition) for page [/search](https://damp-thicket-93938.herokuapp.com/search)
- [CustomerData](https://github.com/AlexandrosKyriakakis/DataBase/tree/master/sql/CustomerData) for pages [/customers_visit_data](https://damp-thicket-93938.herokuapp.com/customers_visit_data) and [/customers](https://damp-thicket-93938.herokuapp.com/customers)
- [ProductData](https://github.com/AlexandrosKyriakakis/DataBase/tree/master/sql/ProductData) for pages at [Product Data](https://damp-thicket-93938.herokuapp.com)
- [Views](https://github.com/AlexandrosKyriakakis/DataBase/tree/master/sql/views) for pages [/customer_info](https://damp-thicket-93938.herokuapp.com/customer_info) and [/sales_category_store](https://damp-thicket-93938.herokuapp.com/sales_category_store)
- [EditData](https://github.com/AlexandrosKyriakakis/DataBase/tree/master/sql/EditData) for pages at [Edit Data](https://damp-thicket-93938.herokuapp.com)

## Authors

- [Alexandros Kyriakakis](https://github.com/AlexandrosKyriakakis)
- [Ioannis Alexopoulos](https://github.com/galexo)
## YouTube
Explaining in Greek language how to use our Site.<br />
<https://www.youtube.com/watch?v=YaeIKbiKvYA&feature=youtu.be>

## Licence

This project uses [MIT license](https://github.com/AlexandrosKyriakakis/DataBase/blob/master/LICENCE)
