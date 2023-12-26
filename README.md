# Financial Management System

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Architecture](#architecture)
4. [Technologies Used](#technologies-used)
5. [Installation](#installation)
6. [Usage Instructions](#usage)
7. [API Reference](#api-reference)
8. [License](#license)
9. [Authors](#authors)
10. [Thanks](#thanks)

---

## Overview

The Financial Management System (FMS) is an advanced web-based application designed to provide individuals with a comprehensive suite of tools for managing their personal finances. It offers a range of features and capabilities to help users track expenses, set budgets, analyze spending patterns, and make informed financial decisions.

---

## Features

- **User Authentication**: FMS incorporates a robust user authentication system to ensure secure access to financial data. It supports multi-factor authentication for added security.

- **Expense Tracking**: Users can easily log and categorize their expenses, including the amount spent, category, and date of the expense. The system provides a user-friendly interface for entering expense data.

- **Budget Management**: FMS includes advanced budgeting tools that help users set and manage budgets for different expense categories. It offers insights into budget performance and provides recommendations for adjustments.

- **Financial Reporting**: Users can generate detailed financial reports and visualizations to gain insights into their spending habits. Reports include charts and graphs for easy analysis.

- **Savings Goals**: FMS allows users to set savings goals, specifying a target amount and deadline. The system tracks progress toward these goals and provides notifications and reminders.

- **Income Tracking**: Users can record their sources of income, including salary, bonuses, and other earnings. Income entries include the source, amount, and date.

- **Expense Insights**: FMS uses AI-driven algorithms to provide insights into spending patterns. It identifies trends and offers suggestions for optimizing expenses.

---

## Architecture

FMS is built on a client-server architecture, with a backend server handling data storage and processing. The frontend provides a user-friendly interface for interacting with the system. The system uses a relational database for data storage.

---

## Technologies Used

- **Backend Development**: Python, Flask
- **Frontend Development**: HTML, CSS, JavaScript
- **Database**: SQLite (for local development), PostgreSQL (for production)
- **Authentication**: Flask-Login
- **Data Visualization**: Chart.js

---
## Installation

### Prerequisites

Before installing FMS, ensure you have the following prerequisites:

- Python 3.8+
- Node.js and npm (for frontend development)
- Docker (optional for containerization)

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/CyberDemon73/Personal-Finance-Tracker-Web-Application.git
   ```
   
2. Install backend dependencies:
   
   ```bash
   pip install -r requirements.txt
   ```
   
4. Set up the frontend (if applicable):
   
   ```bash
   npm install
   npm run build
   ```
   
6. Initialize the database:
   
   ```bash
   flask db upgrade
   ```
   
8. Run the application:
   
   ```bash
   flask run
   ```
###### Then go Run App.py by typing python3 App.py

---

## Usage

### Accessing the Financial Management System (FMS)

1. Start the FMS application by running the following command:

   ```bash
   flask run
   ```
2. Open your web browser and go to the following URL:
   
   ```bash
   http://localhost:5000
   ```
### User Roles and Authentication

The Financial Management System (FMS) has different user roles, each with specific permissions and access levels:

- **Regular User**: Regular users can manage their own financial transactions, budgets, and savings goals. They have limited access compared to admin users.

#### User Authentication

- To log in, follow these steps:
  1. Click on the "Log In" button on the FMS homepage.
  2. Enter your username and password.

- If you don't have an account, you can sign up by clicking on the "Sign Up" button and providing the required information.

#### User Profile

- After logging in, you can access your user profile by clicking on your username at the top right corner of the page. In your user profile, you can:
  - Update your profile information, including your username, email, and profile picture.
  - Change your password to enhance account security.

- Regular users do not have access to user management features, such as creating or modifying other user accounts. These features are exclusive to admin users.

#### Logging Out

- To log out of your FMS account, simply click on the "Log Out" option in the user dropdown menu (accessible by clicking your username at the top right). This will securely end your session and log you out of the system.

User authentication and authorization mechanisms are in place to ensure that each user has the appropriate level of access and security within the Financial Management System.

---

## API Reference

### Integration with Fraud Detection System

The Financial Management System (FMS) will integrate with the [Transaction Fraud Detection System](https://github.com/CyberDemon73/Transaction-Fraud-Detection-System) to enhance security and detect fraudulent transactions in real-time. This integration allows FMS to send transaction data to the Fraud Detection System for analysis. Here's how it works:

1. **Transaction Submission**: When a user makes a financial transaction within FMS, the transaction data is submitted to the Fraud Detection System API.

2. **Real-time Analysis**: The Fraud Detection System performs real-time analysis on the submitted transaction data, using advanced algorithms to assess the risk level of the transaction.

3. **Risk Score**: The Fraud Detection System assigns a risk score to the transaction based on various factors, such as transaction amount, user behavior, and historical data.

4. **Response to FMS**: The Fraud Detection System sends back the risk score and analysis results to FMS.

5. **Transaction Processing**: FMS receives the risk score and analysis results and uses this information to make decisions regarding the transaction. For example, if the risk score is high, FMS may flag the transaction as suspicious and notify the user.

### Financial Management System (FMS) API Endpoints

FMS provides will integrate with  a set of API endpoints for various functionalities. Below are some of the key endpoints:

- **Transaction Submission**:
  - Endpoint: `/api/transactions/submit`
  - Method: POST
  - Description: Submit a financial transaction for analysis by the Fraud Detection System.

- **Transaction Details**:
  - Endpoint: `/api/transactions/{transaction_id}`
  - Method: GET
  - Description: Get details of a specific financial transaction.

- **User Profile**:
  - Endpoint: `/api/users/profile`
  - Method: GET
  - Description: Get the user's profile information.

- **Budget Management**:
  - Endpoint: `/api/budgets`
  - Method: GET
  - Description: Get the user's budget information.

- **Savings Goals**:
  - Endpoint: `/api/goals`
  - Method: GET
  - Description: Get the user's savings goals.

- **Financial Reports**:
  - Endpoint: `/api/reports`
  - Method: GET
  - Description: Generate financial reports and visualizations.

The API Reference provides detailed information about each endpoint, including request and response formats, authentication requirements, and usage examples.

For more information on using the Fraud Detection System API, please refer to the [Transaction Fraud Detection System repository](https://github.com/CyberDemon73/Transaction-Fraud-Detection-System).

---
## License

The Financial Management System (FMS) is licensed under the [MIT License](https://opensource.org/licenses/MIT).

---

### Authors

- Abdelrhman Hatem
- Mohamed Hisham
- Sharook Khaled

---
## Thanks

We would like to express our gratitude to the following individuals and organizations for their support, contributions, and inspiration:

- Our team members: Abdelrhman Hatem, Mohamed Hisham, Sharook Khaled for their dedication and hard work in developing the Financial Management System.

- TLDA inc. for their valuable insights and feedback during the development process.

- The open-source community for their continuous support and contributions to the project.

We appreciate the collaborative spirit and the community's efforts in making the Financial Management System a success.



