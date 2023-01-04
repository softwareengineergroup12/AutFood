from MySQL import mysqldb

class Database :
    
    Mysql = mysqldb()

    # def Create_Table(self):

    Mysql.Create_Table("Users","Username VARCHAR(255) PRIMARY KEY, \
    Password VARCHAR(255),Email VARCHAR(45),Student_Number VARCHAR(11),Phone_Number VARCHAR(11),\
    Active_ID Varchar(100)")
    
    Mysql.Create_Table("Foods","Food_ID Varchar(250) PRIMARY KEY,\
    Food_Name Varchar(250),Quantity Varchar(55),Price Varchar(250),Description Varchar(250)")

    Mysql.Create_Table("Sellers","Seller_ID Varchar(250),Food_ID Varchar(250),\
    Account_Username Varchar(250),Account_Password Varchar(250),Submit_Date Varchar(250)")

    Mysql.Create_Table("wallet","ID Varchar(45), Username Varchar(255) , Balance Varchar(200)")
    
    Mysql.Create_Table("ForgetPassword","User_ID Varchar(255), Username Varchar(255) , Auth_Code Varchar(10)")

