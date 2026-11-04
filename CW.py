import mysql.connector
from mysql.connector import Error
import datetime
import csv
import plotly.graph_objects as go

#Create and return a MySQL connection
def create_connection(host_name, user_name, user_password):
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=user_password
            )
        if connection.is_connected():
            print("Connected to MySQL")
            return connection
    except Error as e:
        print(f"Error: '{e}'")
        return None

#Create database if it does not exist
def create_database(connection, db_name):
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"Database '{db_name}' created or already exists.")
        cursor.close()
    except Error as e:
        print(f"Error: '{e}'")
        
#Create tables
def create_table(connection,db_name):
    try:
        connection.database = db_name
        cursor = connection.cursor()
        
        #Create DiningTable table
        cursor.execute("""
            CREATE TABLE DiningTable (
            TableNo VARCHAR(5) NOT NULL,
            Capacity INT,
            PRIMARY KEY (TableNo)
        )
        """)
        
        #Create Staff table
        cursor.execute("""
        CREATE TABLE Staff(
            StaffID VARCHAR(20) NOT NULL,
            StaffName VARCHAR(100),
            PhoneNo VARCHAR(20),
            Position VARCHAR(20),
            PRIMARY KEY (StaffID)
        )
        """)
        
        #Create Item table
        cursor.execute("""
            CREATE TABLE Item(
            ItemID VARCHAR(20) NOT NULL,
            ItemName VARCHAR(100),
            ItemPrice DECIMAL(10,2),
            PRIMARY KEY (ItemID)
        )
        """)
        
        #Create Food table
        cursor.execute("""
            CREATE TABLE Food(
            ItemID VARCHAR(20) NOT NULL,
            IsVegetarian BOOLEAN,
            PRIMARY KEY (ItemID),
            FOREIGN KEY (ItemID) REFERENCES Item(ItemID)
            ON DELETE CASCADE
            ON UPDATE CASCADE
        )
        """)
        
        #Create Beverage table
        cursor.execute("""
            CREATE TABLE Beverage(
            ItemID VARCHAR(20) NOT NULL,
            IsCaffeine BOOLEAN,
            PRIMARY KEY (ItemID),
            FOREIGN KEY (ItemID) REFERENCES Item(ItemID)
            ON DELETE CASCADE
            ON UPDATE CASCADE
        )
        """)
        
        #Create Orders table
        cursor.execute("""
            CREATE TABLE Orders(
            OrderID VARCHAR(20) NOT NULL,
            StaffID VARCHAR(20) NOT NULL,
            TableNo VARCHAR(5) NOT NULL,
            OrderTime TIME,
            OrderDate DATE,
            OrderStatus VARCHAR(20),
            Subtotal DECIMAL(10,2),
            PRIMARY KEY (OrderID),
            FOREIGN KEY (StaffID) REFERENCES Staff(StaffID)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
            FOREIGN KEY (TableNo) REFERENCES DiningTable(TableNo) ON DELETE RESTRICT
        )
        """)
        
        #Create OrderItem table
        cursor.execute("""
            CREATE TABLE OrderItem(
            OrderID VARCHAR(20) NOT NULL,
            ItemID VARCHAR(20) NOT NULL,
            Quantity INT,
            PRIMARY KEY (OrderID, ItemID),
            FOREIGN KEY (OrderID) REFERENCES Orders(OrderID)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
            FOREIGN KEY (ItemID) REFERENCES Item(ItemID)
            ON DELETE CASCADE
            ON UPDATE CASCADE
        )
        """)
       
        print("Tables created successfully.")
        cursor.close()
       
    except Error as e:
        print(f"Error: '{e}'")
    
#Populate a specified table from a CSV file
def import_csv(connection, csv_file_path, table_name):
    try:
        cursor = connection.cursor()
        with open(csv_file_path, mode='r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header row
           
            #Insert query based on table
            if table_name == "DiningTable":
                insert_query = """
                INSERT INTO DiningTable(TableNo, Capacity)
                VALUES (%s, %s)
                """
              
            elif table_name == "Staff":
                insert_query = """
                INSERT INTO Staff(StaffID, StaffName, PhoneNo, Position)
                VALUES (%s, %s, %s, %s)
                """
            
            elif table_name == "Item":
                insert_query = """
                INSERT INTO Item(ItemID, ItemName, ItemPrice)
                VALUES (%s, %s, %s)
                """
            
            elif table_name == "Food":
                insert_query = """
                INSERT INTO Food(ItemID, IsVegetarian)
                VALUES (%s, %s)
                """
            
            elif table_name == "Beverage":
                insert_query = """
                INSERT INTO Beverage(ItemID, IsCaffeine)
                VALUES (%s, %s)
                """ 
            
            elif table_name == "Orders":
                insert_query = """
                INSERT INTO Orders(OrderID, StaffID, TableNo, OrderTime, OrderDate, OrderStatus, Subtotal)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
            
            elif table_name == "OrderItem":
                insert_query = """
                INSERT INTO OrderItem(OrderID, ItemID, Quantity)
                VALUES (%s, %s, %s)
                """
            
            #Insert row from CSV into the table
            for row in csv_reader:

                #Validate date format
                if table_name == "Orders":
                    raw_date = row[4] 

                    valid_format = [ 
                        "%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y",
                        "%d-%m-%Y", "%Y/%m/%d"
                    ]

                    parsed_date = None
                    for fmt in valid_format:
                        try:
                            parsed_date = datetime.datetime.strptime(raw_date, fmt).strftime("%Y=%m-%d")
                            break
                        except ValueError:
                            continue

                        if not parsed_date:
                            raise ValueError(f"Invalid date format found in CSV: {raw_date}")#
                        
                        #Replace date with corrected format
                        row[4] = parsed_date 

                cursor.execute(insert_query, row)
            
        connection.commit()
        print(f"Data from '{csv_file_path}' inserted successfully into '{table_name}' table.")
        cursor.close()
        
    except Error as e:
        print(f"Error: '{table_name}' '{e}'")

#Query 1: Show the number of orders per day in October 2025       
def query_orders_per_day(connection):
    cursor = connection.cursor()
    query = """
        SELECT OrderDate, COUNT(OrderID)
        FROM Orders
        WHERE DATE_FORMAT(OrderDate, '%Y-%m') = '2025-10'
        GROUP BY OrderDate
        ORDER BY OrderDate;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    print("Query 1 executed. Orders per day in October 2025 retrieved successfully.")
    return results

#Plot chart for query 1
def plot_orders_per_day(data):
    if not data:
        print("No data to plot.")
        return

    dates = [row[0] for row in data]
    counts = [row[1] for row in data]

    fig = go.Figure(data=[go.Bar(x=dates, y=counts)])
    fig.update_layout(
        title="Orders per Day in October 2025",
        xaxis_title="Date",
        yaxis_title="Number of Orders"
    )
    fig.show()
    print("Chart for orders per day in October 2025 displayed successfully.")
    
#Query 2: Show the total sales per day in October 2025
def query_sales_per_day(connection):
    cursor = connection.cursor()
    query = """
        SELECT OrderDate, SUM(Subtotal)
        FROM Orders
        WHERE DATE_FORMAT(OrderDate, '%Y-%m') = '2025-10'
        GROUP BY OrderDate
        ORDER BY OrderDate;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    print("Query 2 executed. Sales per day in October 2025 retrieved successfully.")
    return results
    
#Plot chart for query 2
def plot_sales_per_day(data):
    if not data:
        print("No data to plot.")
        return

    dates = [row[0] for row in data]
    sales = [float(row[1]) for row in data]

    fig = go.Figure(data=[go.Scatter(x=dates, y=sales, mode='lines+markers')])
    fig.update_layout(
        title="Total Sales per Day in October 2025",
        xaxis_title="Date",
        yaxis_title="Total Sales (£)"
    )
    fig.show()
    print("Chart for sales per day in October 2025 displayed successfully.")

                
#Query 3: Show the number of orders handled by each staff in October 2025  
def query_orders_by_staff(connection):
    cursor = connection.cursor()
    query = """
        SELECT StaffName, COUNT(OrderID) AS OrdersHandled
        FROM Staff s, Orders o
        WHERE s.StaffID = o.StaffID 
        GROUP BY StaffName
        ORDER BY COUNT(OrderID) DESC;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    print("Query 3 executed. Number of orders by staff in October 2025 retrieved successfully.")
    return results
    
#Plot chart for query 3
def plot_orders_by_staff(data):
    if not data:
        print("No data to plot.")
        return

    staff = [row[0] for row in data]
    counts = [row[1] for row in data]

    fig = go.Figure(data=[go.Bar(x=staff, y=counts)])
    fig.update_layout(
        title="Number of Orders Handled by Each Staff",
        xaxis_title="Staff Name",
        yaxis_title="Number of Orders Handled"
    )
    fig.show()
    print("Chart for number of orders by staff in October 2025 displayed successfully.")

#Query 4: Count the number of food and beverage available 
def query_food_vs_beverage(connection):
    cursor = connection.cursor()
    query = """
        SELECT 'Food', COUNT(*) 
        FROM Food
        UNION
        SELECT 'Beverage', COUNT(*) 
        FROM Beverage;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    print("Query 4 executed. Counts of food and beverage retrieved successfully.")
    return results

#Plot chart for query 4
def plot_food_vs_beverage(data):
    if not data:
        print("No data to plot.")
        return

    labels = [row[0] for row in data]
    values = [row[1] for row in data]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_layout(title="Comparison of Food and Beverage")
    fig.show()
    print("Chart to compare food and beverage displayed successfully.")

#Query 5: Count the number of vegetarian food and non-vegetarian food
def query_veg_vs_nonveg(connection):
    cursor = connection.cursor()
    query = """
        SELECT 
        (SELECT COUNT(*) FROM Food 
        WHERE IsVegetarian = 1) AS Vegetarian,
        (SELECT COUNT(*)
        FROM Food
        WHERE IsVegetarian = 0) AS NonVegetarian;
    """
    cursor.execute(query)
    results = cursor.fetchone()
    cursor.close()
    print("Query 5 executed. Count of vegetarian food and non-vegetarian food retrieved successfully.")
    return results
    
#Plot chart for query 5
def plot_veg_vs_nonveg(data):
    if not data or len(data)<2:
        print("No data to plot.")
        return

    # data returns only one row: (veg_count, nonveg_count)
    labels = ["Vegetarian Food", "Non-Vegetarian Food"]
    values = [data[0], data[1]]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_layout(title="Comparison of Vegetarian vs Non-Vegetarian Food")
    fig.show()
    print("Chart to compare vegetarian food and non-vegetarian food displayed successfully.")

#Drop database if exists to prevent data duplication
def drop_database(connection, db_name):
    cursor = connection.cursor()
    cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
    cursor.close()
    print(f"Database '{db_name}' dropped if exists.")

#The main program to run all function
def main():
    #MySQL connection details
    host_name = ""
    user_name = ""
    user_password = ""
    
    #Database name
    db_name = "CafeDB"
    
    #File paths for CSVs
    DiningTableCSV = "DiningTable.csv"
    StaffCSV = "Staff.csv"
    ItemCSV = "Item.csv"
    FoodCSV = "Food.csv"
    BeverageCSV = "Beverage.csv"
    OrdersCSV = "Orders.csv"
    OrderItemCSV = "OrderItem.csv"
            
    #Create MySQL connection
    connection = create_connection(host_name, user_name, user_password)
    
    if connection:
        try:
            #Drop previous database if exists to prevent duplication
            drop_database(connection, db_name)

            #Create the database
            create_database(connection, db_name)

            #Create tables
            create_table(connection, db_name)
            
            #Populate data using CSV files
            import_csv(connection, DiningTableCSV, "DiningTable")
            import_csv(connection, StaffCSV, "Staff")
            import_csv(connection, ItemCSV, "Item")
            import_csv(connection, FoodCSV, "Food")
            import_csv(connection, BeverageCSV, "Beverage")
            import_csv(connection, OrdersCSV, "Orders")
            import_csv(connection, OrderItemCSV, "OrderItem")
            
            #Implement queries and charts
            orders_day = query_orders_per_day(connection)
            plot_orders_per_day(orders_day)

            sales_day = query_sales_per_day(connection)
            plot_sales_per_day(sales_day)

            orders_staff = query_orders_by_staff(connection)
            plot_orders_by_staff(orders_staff)

            food_bev = query_food_vs_beverage(connection)
            plot_food_vs_beverage(food_bev)

            veg_nonveg = query_veg_vs_nonveg(connection)
            plot_veg_vs_nonveg(veg_nonveg)
            
        #Close MySQL connection
        finally:
            connection.close()
            print("MySQL connection closed.")
            
    else:
        print("Failed to connect to MySQL.")
            
#Run the main function
if __name__ == "__main__":
    main()
