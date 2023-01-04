import mysql.connector

class mysqldb :

    MySQL,Cursor = None ,None
   
    def __init__(self) -> None:
    
       try:
        self.MySQL = mysql.connector.connect( 
            host = "185.208.172.174",
            user = "frsher_mysql",
            password = "1$3H7g9h",
            database = "frsher_telebot")

        print("Successfully Connected")
        self.__setCursor__()
       except:
        print("Cannot connect to database")

    def __setCursor__ (self):
        self.Cursor = self.MySQL.cursor()
        
    def Create_Table(self,name,attrs):
        if(self.MySQL):
            try:
                self.Cursor.execute(f"CREATE TABLE {name} ({str(attrs).translate({39:None})})")
            except:
                print("Table is already exist!")

    def Insert (self,table,attrs,value):
        
        if(self.MySQL):
            if(type(value) == list):
                SQL = "INSERT INTO {} {} VALUES (%s,%s)".format(table,str(attrs).translate({39:None}))
                self.Cursor.executemany(SQL,value)
            else:
                SQL = "INSERT INTO {} {} VALUES {}".format(table,str(attrs).translate({39:None}),value)
                self.Cursor.execute(SQL)

            self.MySQL.commit()
    
    def Select (self,table,attrs,value,type):
        
        if(self.MySQL):

            if(attrs and value): # specific users
                self.Cursor.execute(f"SELECT * FROM {table} WHERE {attrs}='{value}'")
                return self.Cursor.fetchall()
            elif(type == "all"): # all users
                    self.Cursor.execute(f"SELECT * FROM {table}")
                    return self.Cursor.fetchall()
            else: #last user has been inserted
                self.Cursor.execute(f"SELECT * FROM {table}")
                return self.Cursor.fetchone()

    def Update (self,table,NewAttrs,NewValue,OldAttrs,OldValue):
        if(self.MySQL):
            self.Cursor.execute(f"UPDATE {table} SET {NewAttrs} = '{NewValue}' WHERE {OldAttrs} = '{OldValue}'")
            self.MySQL.commit()

    def Delete(self,table,attrs,value): #Delete user
        if(self.MySQL):
            self.Cursor.execute(f"DELETE FROM {table} WHERE {attrs}='{value}'")
            self.MySQL.commit()

    def Search(self,table,attrs,value):# search for user
        if(self.MySQL):
            if(len(self.Select(table,attrs,value,None)) == 0):
                return 0
            else:
                return self.Select(table,attrs,value,None)