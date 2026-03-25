"""
Chatchana Chaenban
683040487-6
P2
"""

from bank_acc import BankAccount


john = BankAccount("John", "saving", 500)
tim  = BankAccount("Tim", "loan", -1000000)
sarah = BankAccount("Sarah", "saving")   


john.deposit(3000)
print(f"John Balance: {john.get_balance():,}\n")

print(f"Tim loan: {tim.get_balance():,}")
tim.withdraw((tim.get_balance()) / 2)
print(f"After payment: {tim.get_balance():,}\n")


sarah.deposit(50000000)
sarah_loan = BankAccount("Sarah", "loan", -100000000)

john.print_customer()
print()
tim.print_customer()
print()
sarah.print_customer()
print()