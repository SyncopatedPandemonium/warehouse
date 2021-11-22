from classes import User, Employee
from loader import PersonnelLoader, WarehouseLoader
import json

def read_from_file(file_name, loader_type):
    with open(file_name) as f:
        records = json.loads(f.read())
    return list(loader_type().load_records(records))

class WarehouseManager:
    def __init__(self, actions = None) -> None:
        self.personnel = read_from_file('cli/personnel.json', PersonnelLoader)
        self.stock = read_from_file('cli/stock.json', WarehouseLoader)
        self.actions = actions if actions else []

    def get_employee(self, user_name: str) -> Employee:
        """Returns Employee instance with a given name if in system, otherwise None"""
        return next((employee for employee in self.personnel if employee.is_named(user_name)), None)

    def calculate_amount_of_items_in_warehouse(self, id, item_name: str = None) -> int:
        if item_name == None:
            return len( next(( [item for item in warehouse.stock]  for warehouse in self.stock  if warehouse.id == id), []))
        return len(next( [ item for item in warehouse.stock if item.full_name().lower() == item_name.lower() ] for warehouse in self.stock if warehouse.id == id))

    def calculate_item_total_amount(self, item_name = None):
        total_number_of_items = 0
        for warehouse in self.stock:
            if item_name == None:
                total_number_of_items += self.calculate_amount_of_items_in_warehouse(warehouse.id)
            else:
                total_number_of_items += self.calculate_amount_of_items_in_warehouse(warehouse.id, item_name)
        return total_number_of_items

    def get_list_of_unique_items(self) -> list:
        """Returns list of unique item names in all warehouses"""
        items = []
        for warehouse in self.stock:
            items.extend([ item.full_name() for item in warehouse.stock ])
        return list(set(items))

    def get_amount_of_item_pro_warehouse(self, items: list) -> dict:
        """Returns dictionary with item names and amount of items per warehouse in format:
            { item_name1: { warehouse_id_1: amount_of_items, warehouse_id_2: amount_of_items, ... }, { item_name2: {...} }
        """
        return { item_name: {warehouse.id: self.calculate_amount_of_items_in_warehouse(warehouse.id, item_name) for warehouse in self.stock} for item_name in items }

    def get_all_searched_items(self, item_name: str) -> list[tuple]:
        """Returns list of tuples with ID of Warehouse and amount of days the item with given item_name is on stock
            [ (warehouse_id, days_on_stock), (warehouse_id, days_on_stock), ... ]
        """
        item_list = []
        for warehouse in self.stock: 
            item_list.extend((warehouse.id, item.days_in_warehouse()) for item in warehouse.stock if item.full_name().lower() == item_name.lower())
        return item_list

    def get_unique_categories(self) -> list[str]:
        """Returns list of unique categories in all warehouses"""
        return list(set(next( ( item.category for item in warehouse.stock ) for warehouse in self.stock )))

    def calculate_amount_of_items_in_category(self, categories):
        category_and_amount_of_items_in_category = []
        for category in categories:
            category_and_amount_of_items_in_category.append(
                (category, 
                sum([ len( [ item for item in warehouse.stock if item.category == category ] ) for warehouse in self.stock ])
                ))
        return category_and_amount_of_items_in_category

    def get_all_items_of_category(self, category: str) -> list[tuple]:
        """Returns list of tuples with full name of item of given category and ID of warehouse
            [ (item_full_name, warehouse_id), (item_full_name, warehouse_id) ]
        """
        warehouse_items_of_category = []
        for warehouse in self.stock:
            warehouse_items_of_category.extend([ (item.full_name(), warehouse.id) for item in warehouse.stock if item.category == category ])
        return warehouse_items_of_category

    def remove_ordered_items(self): pass


class ConsoleUserInterface:
    def ask_user_name(self) -> str:
        return input('\nEnter your name: ')

    def greet_user(self, user: User):
        return user.greet()

    def display_options(self):
        print('\nOptions:')
        options = ['List all items', 'Search an item and place an order', 'Browse by category', 'Quit']
        for id, option in enumerate(options, 1):
            print(f'{id}. {option}')
    
    def ask_for_option(self):
        return input("\nType the number of the operation: ")

    def print_no_option_error(self, option):
        print(f'\n\n\t***** No option {option}! *****\n')

    def display_items(self, items):
        for item_name, warehouse_info in items.items():
            print(f'\n{item_name}\n')
            print('\n'.join([f'Total amount of item in Warehouse {id}: {amount}' for id, amount in warehouse_info.items() if amount > 0]))

    def ask_for_item_name(self):
        return input('\nEnter name of the item: ')

    def display_search_result(self, item_name, total_number_of_items, items):
        if total_number_of_items:
            print(f'\n{total_number_of_items} {item_name.capitalize()} in stock')
            for item in items:
                warehouse_id, days_in_warehouse = item
                print(f'   In Warehouse {warehouse_id} for {days_in_warehouse} days')    
        else:
            print("\nNot in stock")

    def display_items_of_category(self, category) -> None:
        print('\n'.join( f'{item.full_name()}, Warehouse {self.id}' for item in self.stock if item.category == category) )

    def ask_if_user_want_to_order(self):
        return input('\nDo you wanat to order? (y/n): ')

    def ask_for_password(self):
        return input('\nPassword or press enter to quit: ')

    def ask_how_much_to_order(self):
        return int(input('\nHow many would you like to order? '))

    def print_not_enough_items_in_stock(self, max_amount, item_name):
        print(f'\nThere are only {max_amount} {item_name}')

    def ask_if_user_want_to_order_max_amount(self, max_amount):
        return input(f'\nDo you want to order maximum amount ({max_amount})? (y/n): ')

    def print_order(self, number_to_order, item_name):
        print(f'\nYou have ordered {number_to_order} {item_name}')

    def print_order_cancelled(self):
        print(f'\nOrder cancelled')

    def display_categories(self, categories_numbered):
        print()
        for id, value in categories_numbered.items():
            category, amount = value
            print(f"{id}. {category} ({amount})")

    def ask_for_number_of_category_to_browse(self):
        return input('\nType the number of category you want to browse: ')

    def display_all_items_of_category(self, category, items_in_category_and_warehouse_id):
        print(f'\n{category}:')
        for item, warehouse_id in items_in_category_and_warehouse_id:
            print(f'{item}, Warehouse {warehouse_id}')
        

class Controller:
    def __init__(self) -> None:
        self.user = None
        self.manager = WarehouseManager()
        self.console = ConsoleUserInterface()
        self._actions = []

    def log_in(self):
        """Returns True if user has succesfully logged in, otherwise False"""
        while not self.user.is_authenticated: # and not quit
            password = self.console.ask_for_password()
            self.user.authenticate(password)
            if password == "":
                return False
        return True

    def do_you_want_to_order(self):
        """Returns True if user wants to order and is succesfully logged in"""
        order_or_not = self.console.ask_if_user_want_to_order()
        if order_or_not == 'y':
            return self.log_in() 
        return False

    def order(self, item_name, max_amount):
        order_amount = self.console.ask_how_much_to_order()
        if order_amount > max_amount:
            self.console.print_not_enough_items_in_stock(max_amount, item_name)
            order_option_max_amount = self.console.ask_if_user_want_to_order_max_amount(max_amount)
            if order_option_max_amount == 'y':
                return max_amount
        elif order_amount <= max_amount:
            return order_amount
        return 0

    def _welcome_user(self):
        user_name = self.console.ask_user_name()
        self.user = self.manager.get_employee(user_name) or User(user_name)
        self.console.greet_user(self.user) # this function will just do: user.greet()

    def _main_menu(self):
        self.console.display_options()
        operation_number = self.console.ask_for_option()
        if operation_number in ('1234'):
            return operation_number
        else:
            self.console.print_no_option_error(operation_number)
            self._main_menu()

    def operation_list_items_by_warehouse(self):
        items = self.manager.get_list_of_unique_items()
        dict_of_items_with_amount_pro_warehouse = self.manager.get_amount_of_item_pro_warehouse(items)
        self.console.display_items(dict_of_items_with_amount_pro_warehouse)
        self._actions.append(f'You have listed all items')

    def operation_search_an_item_and_place_an_order(self):
        item_name = self.console.ask_for_item_name()
        total_number_of_items = self.manager.calculate_item_total_amount(item_name)   
        items_list = self.manager.get_all_searched_items(item_name) if total_number_of_items > 0 else []
        self.console.display_search_result(item_name, total_number_of_items, items_list)
        self._actions.append(f'You have searched for {item_name}')
        if not total_number_of_items:
            return
        if not self.do_you_want_to_order():
            self.console.print_order_cancelled()
            return
        if not self.user.is_authenticated:
            return
        ordered_number = self.order(item_name, total_number_of_items)
        if ordered_number:
            self.manager.remove_ordered_items() # TODO
            self.console.print_order(ordered_number, item_name)
            self._actions.append(f'You have ordered {ordered_number} {item_name}')
        else:
            self.console.print_order_cancelled()

    def operation_browse_by_category(self):
        categories = self.manager.get_unique_categories()
        category_and_amount_of_items = self.manager.calculate_amount_of_items_in_category(categories)
        categories_numbered = {f"{id}": item for id, item in enumerate(category_and_amount_of_items, 1)}
        self.console.display_categories(categories_numbered)
        number = self.console.ask_for_number_of_category_to_browse()
        category_and_amount = categories_numbered.get(number)
        if category_and_amount:
            category , _ = category_and_amount
            items_of_category_and_warehouse_id = self.manager.get_all_items_of_category(category)
            self.console.display_all_items_of_category(category, items_of_category_and_warehouse_id)
            self._actions.append(f'You have searched for category: {category}')

    def operation_quit(self):
        self.user.bye(self._actions)

    def main(self):
        self._welcome_user()
        end_of_session = False
        while not end_of_session:
            operation_number = self._main_menu() # display options, ask which one to pick
            if operation_number == '1':
                self.operation_list_items_by_warehouse()
            elif operation_number == '2':
                self.operation_search_an_item_and_place_an_order()
            elif operation_number == '3':
                self.operation_browse_by_category()
            elif operation_number == '4':
                end_of_session = True
                self.operation_quit()
                

if __name__ == '__main__':
    app = Controller()
    app.main()