from __future__ import annotations 

from datetime import datetime

class User:
    def __init__(self, user_name: str = None) -> None:
        self._name = user_name if user_name else 'Anonymous'
        self.is_authenticated = False

    def __str__(self):
        return f'User name: {self._name}'

    def __repr__(self):
        return f'User({self.__str__()})'

    def get_user_name():
        return input('Enter name: ')

    def authenticate(self, password: str) -> bool:
        return False

    def is_named(self, name):
        return self._name == name

    def greet(self) -> None:
        print(f"\nHello, {self._name}! \nWelcome to our Warehouse Database. \nIf you don't find what you are looking for, please ask one of our staff members to assist you.")

    def bye(self, actions: list) -> None:
        del actions # don't show actions to just any user
        print(f"\nThank you for your visit, {self._name}!\n")

class Employee(User):
    def __init__(self, user_name: str, password: str = None, head_of: list[Employee] = None) -> None:
        super().__init__(user_name)
        self.__password = password
        self.head_of = head_of if head_of is not None else []

    def __str__(self):
        return f'{super().__str__()} Password: {self.__password} Head of: {self.head_of}'

    def __repr__(self):
        return f'Employee({self.__str__()})'


    def get_user_password(self):
        return input('Enter password: ')

    def authenticate(self, password: str) -> bool:
        """Returns True if the password provided by user is the same as password in system, otherwise True
            If User becomes authenticated parameter self.is_authenticated becomes True
        """
        match = password == self.__password
        if match:
            # NOTE: this is not specified!! (but it makes sense, and the opposite doesn't)
            self.is_authenticated = True
        return match

    def order(self, item: Item, amount: int) -> None:
        print(f'You have ordered {item}. \nOrdered amount: {amount}')

    def greet(self) -> None:
        print(f'\nHello, {self._name} \nIf you experience a problem with the system, please contact technical support.')

    def bye(self, actions: list) -> None:
        super().bye(actions)
        print('\n'.join(f'{id}. {action}' for id, action in enumerate(actions, 1)))
    

class Warehouse:
    def __init__(self, id: int, stock: list = None) -> None:
        self.id = id
        self.stock = stock if stock is not None else []

    def __str__(self) -> str:
        return f'Warehouse ID: {self.id} ({len(self.stock)} items in stock)'

    def __repr__(self) -> str:
        return f'Warehouse({self.__str__()})'

    def occupancy(self) -> int:
        return len(self.stock)

    def add_item(self, item: Item) -> None:
        self.stock.append(item)

    def search(self, search_term: str) -> list[Item]:
        items = [ item for item in self.stock if item.full_name() == search_term ]
        return items

# TODO:
# @dataclass
class Item:
    def __init__(self, state: str, category: str, warehouse: int, date_of_stock: datetime)  -> None:
        del warehouse # we don't care about warehouse param
        self.state = state
        self.category = category
        self.date_of_stock = date_of_stock

    def __str__(self) -> str:
        return f'State: {self.state}, Category: {self.category}, Date of stock: {self.date_of_stock}'

    def __repr__(self) -> str:
        return f'Item({self.__str__()})'

    def full_name(self) -> str:
        return f'{self.state} {self.category}'

    def days_in_warehouse(self) -> str:
        today = datetime.today()
        return (today - self.date_of_stock).days

    def name_warehouse_info(self) -> str:
        return f"{self.name()}, Warehouse {self.warehouse}"