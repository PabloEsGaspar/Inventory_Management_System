# Gaspar Tonnesen | CIS 345 T/Th 12:00 PM | Final Project | Due 04.26.19

# ///////////////////// PRODUCT CLASS ////////////////////////////////////////////////////////////////////////


class Product:
    """product class defines common info for all products"""

    def __init__(self, id=0, description='', q_on_hand=0, price=0.0):
        """initializes a new Product instance"""
        self.id = id
        self.description = description
        self.q_on_hand = q_on_hand
        self.price = price

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
            self.__id = id

    @property
    def description(self):
        return f'{self.__description}'

    @description.setter
    def description(self, new_desc):
        self.__description = new_desc

    @property
    def q_on_hand(self):
        return self.__q_on_hand

    @q_on_hand.setter
    def q_on_hand(self, new_q):
        self.__q_on_hand = new_q

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, new_price):
        self.__price = new_price

    def __str__(self):
        """overrides the string representation of the product"""
        return f'ID#{self.id} | {self.description} | {self.q_on_hand} in stock | Price: ${self.price:.2f}'


class Attachment(Product):
    """Attachment inherits from Product and defines common info for attachment products"""

    def __init__(self, attach_id=0, material='', id=0, description='', q_on_hand=0, price=0.0):
        """initializes new Attachment Product instance"""
        super().__init__(id, description, q_on_hand, price)
        self.attach_id = attach_id
        self.material = material

    @property
    def attach_id(self):
        return self.__attach_id

    @attach_id.setter
    def attach_id(self, new_attach_id):
        self.__attach_id = new_attach_id

    @property
    def material(self):
        return f'{self.__material}'

    @material.setter
    def material(self, new_material):
        self.__material = new_material

    def __str__(self):
        """overrides the string representation of the attachment product"""
        product_info = super().__str__()
        return f'{product_info} | a_id: {self.attach_id} | material: {self.material}'

