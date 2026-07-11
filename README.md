# Banking System

A console-based banking system built with Python using Object-Oriented
Programming (OOP).

This is my first major Python project. I built it to practice OOP
concepts, JSON data storage, inheritance, method overriding, and real
banking operations.

## Features

-   Create Savings and Current accounts
-   Login using account number and PIN
-   Deposit and withdraw money
-   Transfer money between accounts
-   Check balance and change PIN
-   View transaction history
-   Add interest to Savings accounts
-   Current account overdraft support
-   Delete accounts
-   JSON data persistence
-   Admin panel

## Account Types

### Savings Account

-   Balance-based interest rates
-   Add interest feature
-   Withdrawal limit of ₹20,000

### Current Account

-   Minimum opening balance of ₹200,000
-   Overdraft limit of ₹50,000
-   No savings interest

## Admin Panel

The admin can view all accounts, search accounts, check total bank
money, count accounts, and delete accounts.

## 🔐 Admin Access

The project includes an Admin Panel for managing bank accounts.

Default Admin PIN:

`1234`

> Note: This PIN is for demonstration purposes only. In a real banking system, credentials should never be hardcoded in the source code.

## Concepts Used

-   Python
-   Object-Oriented Programming (OOP)
-   Classes and Objects
-   Inheritance
-   Encapsulation
-   Method Overriding
-   `super()`
-   `isinstance()`
-   Exception Handling
-   JSON File Handling
-   Dictionaries and Lists

## Project Structure

``` text
Banking-System/
├── banking_system.py
├── account.json
└── README.md
```

> Rename the main Python file to `banking_system.py` if it still has a
> temporary name such as `new_test.py`.

## How to Run

1.  Make sure Python is installed.
2.  Download or clone the repository.
3.  Open a terminal in the project folder.
4.  Run:

``` bash
python Bank-pro.py
```

## Data Storage

Account information and transaction history are stored in
`account.json`. The file is loaded when the program starts and updated
when account data changes.

## Future Improvements

-   Improve PIN security
-   Add timestamps to transactions
-   Refactor repeated code
-   Add automated tests
-   Replace JSON with a database
-   Build a graphical or web interface

## Author

**Aditya Habib**

BCA student learning Python, DSA, Web Development, and AI/ML.

------------------------------------------------------------------------

Built as a learning project to improve Python and Object-Oriented
Programming skills.
