# Cafe Database System

**📌Overview**

A Python-based MySQL database solution designed to automate schema creation, import relational data from CSV files, execute relational analytical queries, and generate interactive visual dashboards using Plotly

🛠️ **Tech Stack**

Language: Python

Database: MySQL

Libraries & Packages:
  - mysql-connector-python (MySQL Database Connection)
  - plotly (Data Visualization)
  - csv (Built-in data parsing)

 📊 **Features**
 
Auto Schema Generation: Drops existing instances of CafeDB to prevent duplicate entries, recreates the database, and constructs foreign-key constrained tables (DiningTable, Staff, Item, Food, Beverage, Orders, OrderItem).

Relational Data Import: Parses and imports CSV data files into their corresponding SQL tables in sequence.

Interactive Data Visualization:

Daily Order Counts: October 2025 daily transaction frequency (Bar Chart).

Daily Revenue Trends: October 2025 daily sales performance in RM (Line Chart).

Staff Workload Distribution: Total orders handled per staff member (Bar Chart).

Menu Composition Analysis: Food vs. Beverage menu share (Pie Chart).

Dietary Option Split: Vegetarian vs. Non-Vegetarian food item ratio (Pie Chart).
