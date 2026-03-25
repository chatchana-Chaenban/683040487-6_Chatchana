"""
Chatchana Chaenban
683040487-6
P2
"""

class BankAccount:

      saving_run = 0 # class attribute
      loaning_run = 0
      branch_number = 5511
      branch_name = "KKU Complex"

      def __init__(self, name, acc_type="saving", balance=0): # constructor
         if not name:
           raise ValueError("Name is required") #if there are no name 
       
         self.name = name # instance
         self.type = acc_type
         self.balance = balance

         if self.type == "saving": # saving type
            BankAccount.saving_run += 1
            #type_code = 1
            self.acc_num = f"{BankAccount.branch_number}-1-{BankAccount.saving_run}"
        
         elif self.type == "loan": # loaning type
            BankAccount.loaning_run += 1
            #type_code = 2
            self.acc_num = f"{BankAccount.branch_number}-2-{BankAccount.loaning_run}"

         else:
            raise ValueError("Invalid account type")
       
      def get_balance(self):
         return self.balance
    
      def deposit(self, amount=0): # deposit money
         self.balance += amount
         return self.balance

      def withdraw(self, amount=0): # withdraw money
         self.balance -= amount
         return self.balance

      def print_customer(self):
         print("----- Customer Record -----")
         print(f"Name: {self.name}")
         print(f"Account number: {self.acc_num}")
         print(f"Account type: {self.type}")
         print(f"Balance: {self.balance}")
         print("----- End Record -----")

    
