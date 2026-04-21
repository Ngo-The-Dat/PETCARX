# 🐾 PETCARX

## 📖 Overview

**PETCARX** is an academic project that builds a management system for a pet care store chain, with a primary focus on researching and implementing **query performance optimization techniques**.

The system is built on the following technologies:

- **Frontend/Backend**: [Streamlit](https://streamlit.io/) — a Python framework for rapidly building web interfaces.
- **Database**: Microsoft SQL Server (local database).
- **Languages**: Python, T-SQL.

The system serves four main user groups: **Customer**, **Doctor**, **Manager**, and **Staff**, each with dedicated features tailored to their role.

---

## ⚙️ Key Features

### 👤 Customer
- Search for products.
- Look up doctor schedules.
- View purchase history.
- View pet examination history.

### 🩺 Doctor
- Look up pet examination history.
- Search for medications.
- Create new medical records.

### 📊 Manager
- View annual revenue of each branch.
- View revenue by doctor.
- View examination counts by branch.
- View product sales revenue.
- View total revenue across all branches.
- View revenue of a specific branch.

### 🧑‍💼 Staff
- Look up pets.
- Search for customers by phone number.
- View account lists by membership tier.
- Create invoices for customers.
- Create new membership accounts.
- Create pet profiles.

---

## 🚀 Query Performance Optimization Techniques

To ensure the system runs smoothly as data grows, we have proposed and implemented **Indexes** and **Partitions** on tables with high query frequency.

### 🔹 Table `TAIKHOANHOIVIEN` (Member Accounts)
- **Proposed Index**:
  - `Non-Clustered Index` on column **SDT** (phone number) — supports the `FIND_KH_THROUGH_SDT` procedure (T1).
  - *Reason*: Phone number is a frequently used attribute for customer lookup.
- **Proposed Partition**:
  - Partition by **MACAPBAC** (membership tier) — splits data into tiers (Basic, Loyal, VIP).
  - *Reason*: Optimizes monthly periodic membership reports.

### 🔹 Table `HOADON` (Invoices)
- **Proposed Index**:
  - `Non-Clustered Index` on column **MATK** (account ID) — supports the `sp_LichSuMuaHang` procedure (T14).
  - *Reason*: Customers frequently look up their purchase history on the website.
- **Proposed Partition**:
  - Partition by **NGAYLAP** (issue date, by year/quarter).
  - *Reason*: The invoice table is very large (~500,000 rows in the sample dataset); time-based partitioning significantly speeds up daily/monthly/yearly revenue reports.

### 🔹 Table `DOANHTHUCHINHANH` (Branch Revenue)
- **Proposed Partition**:
  - Partition by **NGAY** (date, by year).
  - *Reason*: Supports management scenarios for analyzing business performance by year and generating system-wide revenue reports.

### 🔹 Tables `HOSOKHAMBENH` & `HOSOTIEMPHONG` (Medical & Vaccination Records)
- **Proposed Index**:
  - `Non-Clustered Index` on column **MATC** (pet ID) — supports the `sp_TraCuuLichSuKhamThuCung` procedure (T7).
  - *Reason*: Doctors frequently look up examination/vaccination history throughout the day when receiving pets.

### 🔹 Table `SANPHAM` (Products)
- **Proposed Index**:
  - `Non-Clustered Index` on column **TEN** (name) — supports the `search_product_name` procedure (T13).
  - *Reason*: Customers frequently search for products by name on the website using the `LIKE` operator.

---

## 🛠️ Installation & Setup Guide

### Step 1 — Install required dependencies
Open a terminal in the project's root directory and run:
```bash
pip install -r .\web_app\requirements.txt
```

### Step 2 — Initialize the database
Open **SQL Server Management Studio (SSMS)** and execute the following SQL files **in order**:

1. `Database.sql` — creates the database structure (tables, constraints, indexes, partitions).
2. `insert_data.sql` — populates the system with sample data.
3. `proc_trigger.sql` — installs the required Stored Procedures and Triggers.

### Step 3 — Launch the web application
Once setup is complete, run the following command to start the web app:
```bash
streamlit run .\web_app\app.py
```
The browser will automatically open the application at `http://localhost:8501`.

---

## 📌 Notes
- This project focuses on **evaluating and demonstrating the effectiveness** of query optimization techniques (Indexes, Partitions) by comparing execution time before and after applying them.
- The sample dataset was designed at a large scale (~500,000 invoice rows) to clearly showcase performance differences.