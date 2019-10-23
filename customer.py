# Gaspar Tonnesen | CIS 345 T/Th 12:00 PM | Final Project | Due 04.26.19

# ///////////////////// CUSTOMER ////////////////////////////////////////////////////////////////////////


class Customer:
    """defines common attributes of customers"""

    def __init__(self, acc_num=0, name='', pin='0000', balance=0.0):
        """initializes a new instance of te customer class"""
        self.acc_num = acc_num
        self.name = name
        self.pin = pin
        self.balance = balance

    @property
    def acc_num(self):
        return self.__acc_num

    @acc_num.setter
    def acc_num(self, new_acc_num):
        self.__acc_num = new_acc_num

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name):
        self.__name = new_name

    @property
    def pin(self):
        return self.__pin

    @pin.setter
    def pin(self, new_pin):
        self.__pin = new_pin

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, new_balance):
        self.__balance = new_balance

    def __str__(self):
        return f'Account# {self.acc_num} | {self.name} | Balance: ${self.balance:.2f}'


class Employee(Customer):

    def __init__(self, emp_id=0, acc_num=0, name='', pin='', balance=0.0):
        super().__init__(acc_num, name, pin, balance)
        self.emp_id = emp_id

    @property
    def emp_id(self):
        return f'{self.__emp_id}'

    @emp_id.setter
    def emp_id(self, new_emp_id):
        self.__emp_id = new_emp_id

    def __str__(self):
        """overrides the string representation of the attachment product"""
        cust_info = super().__str__()
        return f'{cust_info} | employee_id: {self.emp_id}'
