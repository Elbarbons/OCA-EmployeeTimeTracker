# OCA-EmployeeTimeTracker
OCA-EmployeeTimeTracker is a Python application designed to manage and track employees' working hours in a company. It allows you to log work hours, generate timesheets, and create reports to ensure efficient time management and payroll processing. It was created for free for an Italian company composed of 50 employees to speed up payroll processing and better manage working hours allocated to projects based on the projects' budget. The application is written in Python using the library *ttkinter* and utilizes an SQL database to store and retrieve all the data.

## Features
- **Login page**
  
![Login page.](Images/Login.png)

- **Worker page:** where workers can log work hours and consult, sort, filter, and delete previously inserted work hours.

![Worker page.](Images/WorkerPage.png)

- **Manager page**: managers can access to a menu in which they can navigate to three different screens:
  + One where they can define new clients and jobs
  + One where they can consult workers' work hours grouped by client, job, and type of job (useful to check the amount of working hours spent on different projects)
  + One where they can consult workers' work hours grouped by worker name, job, and type of job (useful for creating paychecks at the end of the month)

![Manager page.](Images/ManagerPage.png)

- **Admin page**: admins can insert, delete, and edit users.

- **Logs writing**: the application automatically logs all the errors in a .log file.

## Installation
To install and run the application, follow these steps:

1. Clone the repository:
```console
git clone https://github.com/Elbarbons/OCA-EmployeeTimeTracker.git
```

2. Install the required dependencies:
```console
pip install -r requirements.txt
```

3. Create the database and the tables needed for the application to work. These are the required tables:
   
 - **oca.users** :
   + Username  [VARCHAR(100)] PK - Not Nullable
   + Password  [VARCHAR(100)] Not Nullable
   + Ruolo  [VARCHAR(100)] Not Nullable
   + Nome  [VARCHAR(100)] Not Nullable
   + Cognome  [VARCHAR(100)] Not Nullable
   + CostoOrario [INT], firstLogin[INT]

 - **oca.commesse**:
   + Nome [VARCHAR(100)] PK - Not Nullable
   + Tipo [VARCHAR(100)] PK - Not Nullable
   + Cliente  [VARCHAR(100)], Descrizione  [VARCHAR(200)]
   + Budget [INT]
 
 - **oca.storico_commesse** :
   + CognomeLavoratore [VARCHAR(100)] PK - Not Nullable
   + Data [Date] PK - Not Nullable
   + Ore [INT] PK - Not Nullable
   + Commessa [VARCHAR(100)] PK - Not Nullable
   + TipoCommesa [VARCHAR(100)] PK - Not Nullable
   + Cliente [VARCHAR(100)] PK - Not Nullable

4. To connect to your database, set the HOST, USER, PASSWORD, and DB variables in the DBOperations.py file.

5. Run the application:
```console
python main.py
```

## Contributing
Contributions are welcome! 

## License
This project is licensed under the MIT License. See the LICENSE file for details.
