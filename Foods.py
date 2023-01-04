from DatabaseConnection import Database
import shortuuid

class Foods :

    FoodID = ''

    def __init__(self, *args) -> None:
        if(len(args)!=0):
            Foods.FoodID = f"/fd_{shortuuid.uuid()}"
            self.Atrr = "(Food_ID,Food_Name,Quantity,Price,Description)"
            self.set_value(args)
      

    def set_value(self,args):
        self.data =[]
        self.data.append(self.FoodID)
        for key in args[0] :
            if(key != "Username" and key !="Password" and key!="method"):
                self.data.append(args[0].get(key))
        self.insert_to_mysql("Foods",self.Atrr,tuple(self.data))

    
    def insert_to_mysql(self,table,attr,value):
        Database.Mysql.Insert(table,attr,value)
    



