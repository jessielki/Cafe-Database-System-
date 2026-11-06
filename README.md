# Cafe Database System

## 📌 Project Overview

This project provides an automated backend data pipeline for a dining and cafe setup. It handles database creation, foreign key relation building, CSV data ingestion, and business intelligence reporting with interactive Plotly visualizations.

### Key Highlights
* **Automated Data Pipeline:** Programmatically creates database structures, drops old instances to avoid data duplication, and sequentially imports structured CSV data.
* **Relational Schema Design:** Features 7 interconnected tables with primary and foreign key constraints enforcing table-level and category-level relationships (`Item`, `Food`, `Beverage`, `Orders`, `OrderItem`, `Staff`, `DiningTable`).
* **Interactive Business Intelligence:** Integrates SQL query outputs directly with Plotly to output interactive visual charts for revenue tracking, staffing workloads, and inventory composition.

---

## 🗄️ Database Architecture & Entity Relationships

The relational schema organizes cafe transactions, menu taxonomies, staff assignments, and seating capacity:

* **Core Entities:**
  * `DiningTable`: Table capacity records.
  * `Staff`: Employee profiles and positions.
  * `Item`: General menu items and baseline pricing.
  * `Food` & `Beverage`: Categorical child tables inheriting from `Item` via Foreign Keys (tracking properties like `IsVegetarian` and `IsCaffeine`).
  * `Orders` & `OrderItem`: Order transaction headers and itemized line details.

---

## ⚙️ Schema Features & Constraints

* **Primary & Foreign Key Integrity:** Foreign keys tie transactions directly to staff, tables, and menu items with `ON DELETE RESTRICT` safeguards on core dining assets.
* **Specialized Categorization:** Sub-category tables (`Food`, `Beverage`) use binary flags (`BOOLEAN`) to model item attributes clean of sparse columns in the parent table.
* **Transactional Auditing:** Order headers maintain precise `DATE`, `TIME`, and calculated `Subtotal` values for financial reporting.

---

## 💡 Key Analytical Queries & Visualizations Included

The Python script executes embedded SQL queries and plots real-time analytical dashboards:

1. **Daily Order Frequency (Bar Chart):** Aggregates daily order counts for October 2025.
2. **Daily Sales Trends (Line Chart):** Computes total daily revenue across October 2025.
3. **Staff Workload Distribution (Bar Chart):** Tracks and ranks total order volume handled per staff member.
4. **Menu Composition (Pie Chart):** Compares total food inventory offerings against beverage items using `UNION` aggregations.
5. **Dietary Split (Pie Chart):** Analyzes the ratio of vegetarian vs. non-vegetarian menu items.
