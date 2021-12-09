from classes import User, Employee
from loader import PersonnelLoader, WarehouseLoader
import json
import itertools


def read_and_parse_json_file(file_name):
    with open(file_name) as f:
        records = json.loads(f.read())
    return records


class WarehouseManager:
    personnel_records = read_and_parse_json_file("cli/personnel.json")
    item_records = read_and_parse_json_file("cli/stock.json")

    def __init__(
        self, personnel_records=personnel_records, item_records=item_records
    ) -> None:
        self._personnel = list(PersonnelLoader().load_records(personnel_records))
        self._stock = list(WarehouseLoader().load_records(item_records))
        self._warehouses = {warehouse.id: warehouse for warehouse in self._stock}

    def __repr__(self) -> str:
        return f"{type(self).__name__}(number_of_items={len(self._stock)}, id={self._warehouses})"

    def get_employee(self, user_name: str) -> Employee:
        """Returns Employee instance with a given name if in system, otherwise None"""
        return next(
            (employee for employee in self._personnel if employee.is_named(user_name)),
            None,
        )

    def _all_items_in_warehouse_filtered(
        self, source=lambda w: w.stock, filter=lambda _x: True
    ):
        """Returns (warehouse.id, item) pairs from given source (default is the whole warehouse stock) under certain conditions (default is any condition)"""
        return itertools.chain.from_iterable(
            ((warehouse.id, item) for item in source(warehouse) if filter(item))
            for warehouse in self._stock
        )

    # TODO: private
    def _all_items_with_warehouse_id(self):
        """Returns an iterable -> tuple of all items in our warehouses with the id of warehouse
        (warehouse_id, Item), (warehouse_id, Item), ..."""
        return self._all_items_in_warehouse_filtered()

    def _all_named_items_with_warehouse_id(self, item_name):
        """Returns an iterable -> tuple of all items with a given item_name in our warehouses with the id of warehouse
        (warehouse_id, Item), (warehouse_id, Item), ..."""
        return self._all_items_in_warehouse_filtered(
            source=lambda w: w.search(item_name)
        )

    # TODO: private
    # TODO: use _all_items_in_warehouse_filtered
    def _all_items_of_category_with_warehouse_id(self, category):
        """Returns an iterable -> tuple of all items with of a given category in our warehouses with the id of warehouse
        (warehouse_id, Item), (warehouse_id, Item), ..."""
        return self._all_items_in_warehouse_filtered(
            filter=lambda i: i.category == category
        )

    def calculate_total_amount(self) -> int:
        """Returns total amount of all items in all warehouses"""
        return sum(warehouse.occupancy() for warehouse in self._stock)

    def calculate_item_amount_in_warehouse(self, id: int, item_name: str) -> int:
        """Returns the amount of items with a given name in the warehouse with given ID"""
        return len(self._warehouses[id].search(item_name))

    def calculate_item_total_amount(self, item_name: str = None) -> int:
        """Returns total amount of items with a given name in all warehouses combined"""
        return sum(
            self.calculate_item_amount_in_warehouse(warehouse.id, item_name)
            for warehouse in self._stock
        )

    def get_unique_item_names(self) -> set:
        """Returns set of unique item names in all warehouses"""
        return set(item[1].full_name() for item in self._all_items_with_warehouse_id())

    def get_amount_of_item_in_each_warehouse(self, items: set) -> dict:
        """Returns dictionary with item names and amount of items per warehouse in format:
        { item_name1: { warehouse_id_1: amount_of_items, warehouse_id_2: amount_of_items, ... }, { item_name2: {...} }
        """
        return {
            item_name: {
                warehouse.id: self.calculate_item_amount_in_warehouse(
                    warehouse.id, item_name
                )
                for warehouse in self._stock
            }
            for item_name in items
        }

    def get_unique_categories(self) -> set[str]:
        """Returns list of unique categories in all warehouses"""
        return set(item[1].category for item in self._all_items_with_warehouse_id())

    def calculate_amount_of_items_in_category(
        self, categories: set[str]
    ) -> list[tuple]:
        """Returns list of tuples with category and total amount of items of that category"""
        return [
            (
                category,
                sum(
                    1
                    for item in self._all_items_with_warehouse_id()
                    if item[1].category == category
                ),
            )
            for category in categories
        ]

    def get_all_items_of_category(self, category: str) -> list[tuple]:
        """Returns list of tuples with full name of item of given category and ID of warehouse
        [ (item_full_name, warehouse_id), (item_full_name, warehouse_id) ]
        """
        return [
            (item.full_name(), warehouse_id)
            for warehouse_id, item in self._all_items_of_category_with_warehouse_id(
                category
            )
        ]

    def remove_ordered_items(self):
        pass


# TODO: write unit tests :-)
class ConsoleUserInterface:
    def ask_user_name(self) -> str:
        return input("\nEnter your name: ")

    def greet_user(self, user: User):
        return user.greet()

    def display_operations(self) -> None:
        """Prints list of operation in main menu"""
        print("\nOptions:")
        options = [
            "List all items",
            "Search an item and place an order",
            "Browse by category",
            "Quit",
        ]
        for id, option in enumerate(options, 1):
            print(f"{id}. {option}")

    def ask_for_operation(self) -> str:
        valid_operations = ["1", "2", "3", "4"]
        operation = input("\nType the number of the operation: ")
        while operation not in valid_operations:
            self.print_no_operation_error(operation)
            self.display_operations()
            operation = input("\nType the number of the operation: ")
        return operation

    def print_no_operation_error(self, operation: str) -> None:
        print(f"\n\n\t***** No operation {operation}! *****\n")

    def display_items(self, items: dict) -> None:
        """'Input: { Item1': {id1: amount, id2: amount, id3: amount, ...}, 'Item2': {id1: amount, id2: amount, ...}}
        Output print:

        Item1 Full Name

        Total amount of item in Warehouse 1: 4
        Total amount of item in Warehouse 2: 1
        Total amount of item in Warehouse 3: 2
        Total amount of item in Warehouse 4: 1

        """
        for item_name, warehouse_info in items.items():
            print(f"\n{item_name}\n")
            print(
                "\n".join(
                    [
                        f"Total amount of item in Warehouse {id}: {amount}"
                        for id, amount in warehouse_info.items()
                        if amount > 0
                    ]
                )
            )

    def ask_for_item_name(self) -> str:
        return input("\nEnter name of the item: ")

    def display_search_result(self, items: list[tuple]) -> None:
        if not items:
            print("\nNot in stock")
            return
        total_number_of_items = len(items)
        item_name = items[0][1].full_name()
        print(f"\n{total_number_of_items} {item_name} in stock")
        for item in items:
            id, days = item
            print(f"\tIn Warehouse {id} for {days.days_in_warehouse()} days")

    def display_all_items_of_category(
        self, category: str, items_in_category_and_warehouse_id: list[tuple]
    ) -> None:
        print(f"\n{category}:")
        for item, warehouse_id in items_in_category_and_warehouse_id:
            print(f"{item}, Warehouse {warehouse_id}")

    def ask_if_user_want_to_order(self) -> str:
        action = input("\nDo you wanat to order? (y/n): ")
        while action not in ("y", "n"):
            self.print_no_operation_error(action)
            action = input("\nDo you wanat to order? (y/n): ")
        return action == "y"

    def ask_for_password(self) -> str:
        return input("\nPassword or press enter to quit: ")

    def ask_how_much_to_order(self) -> int:
        amount_to_order = input("\nHow many would you like to order? ")
        while not amount_to_order.isnumeric():
            print("\n***** Input not valid! *****")
            amount_to_order = input("\nHow many would you like to order? ")
        return int(amount_to_order)

    def print_not_enough_items_in_stock(self, max_amount: int, item_name: str) -> None:
        print(f"\nThere are only {max_amount} {item_name}")

    def ask_if_user_want_to_order_max_amount(self, max_amount: int) -> str:
        action = input(f"\nDo you want to order maximum amount ({max_amount})? (y/n): ")
        while action not in ("y", "n"):
            self.print_no_operation_error(action)
            action = input(
                f"\nDo you want to order maximum amount ({max_amount})? (y/n): "
            )
        return action == "y"

    def print_order(self, number_to_order: int, item_name: str) -> None:
        print(f"\nYou have ordered {number_to_order} {item_name}")

    def print_order_cancelled(self) -> None:
        print("\nOrder cancelled")

    def display_categories(self, categories_numbered: dict) -> None:
        print()
        for id, value in categories_numbered.items():
            category, amount = value
            print(f"{id}. {category} ({amount})")

    def ask_for_number_of_category_to_browse(self) -> str:
        return input("\nType the number of category you want to browse: ")


# When writing unit tests for Controller...
# ... you will need to sometimes patch input
# ... sometimes need to patch "print"
#
# ... BUT THERE IS A BETTER WAY!
#
# will create a controller like this:

# personnel = [ { "user_name": "Tomek", "password": "q", "head_of": [ { "user_name": "Ania", "password": "hunter2", "head_of": [] } ] } ]
# items = [ ... ]
# warehouse_manager = WarehouseManager(personnel_records = personnel, item_records = items)
#
# controller = Controller(manager = warehouse_manager)
#
# now you test some methods on controller :-)


# TODO: write tests
class Controller:
    def __init__(self, manager=None, console=None, user=None) -> None:
        self.user = user
        self.manager = manager if manager else WarehouseManager()
        self.console = console if console else ConsoleUserInterface()
        self._actions = []
        # TODO:
        # self._list_controller = ListController(manager=self.manager, console=self.console)
        # self._search_and_order_controller = SearchOrderController(manager=self.manager, console=self.console)
        # self._search_category_controller = SearchCategoryController(manager=self.manager, console=self.console)

    def log_in(self):
        """Returns True if user has succesfully logged in, otherwise False"""
        while not self.user.is_authenticated:
            password = self.console.ask_for_password()
            if password == "":
                return False
            self.user.authenticate(password)
        return True

        # better (but requires the code below):
        # try:
        #     while not self.user.is_authenticated:
        #         self.user.authenticate(self.console.ask_for_password())
        #     return True
        # except ConsoleUserInterface.PasswordInputAbortedError:
        #     return False

        # requires these changes to ConsoleUserInterface

        # class ConsoleUserInterface:
        #     class PasswordInputAbortedError(BaseException): pass

        #     def ask_for_password(self):
        #         password = input("GIMME PASSWORD (or empty to quit):")
        #         if password == "":
        #             raise __class__.PasswordInputAbortedError
        #         return password

    def do_you_want_to_order(self):
        """Returns True if user wants to order and is succesfully logged in"""
        order_or_not = self.console.ask_if_user_want_to_order()
        if not order_or_not:
            return False
        return self.log_in()

    def order(self, item_name, max_amount):
        order_amount = self.console.ask_how_much_to_order()
        if order_amount > max_amount:
            self.console.print_not_enough_items_in_stock(max_amount, item_name)
            order_or_not_max_amount = self.console.ask_if_user_want_to_order_max_amount(
                max_amount
            )
            if order_or_not_max_amount:
                return max_amount
        elif order_amount <= max_amount:
            return order_amount

    def _welcome_user(self):
        user_name = self.console.ask_user_name()
        self.user = self.manager.get_employee(user_name) or User(user_name)
        self.console.greet_user(self.user)  # this function will just do: user.greet()

    def _main_menu(self):
        self.console.display_operations()
        operation_number = self.console.ask_for_operation()
        return operation_number

    def operation_list_items_by_warehouse(self):
        items = self.manager.get_unique_item_names()
        dict_of_items_with_amount_pro_warehouse = (
            self.manager.get_amount_of_item_in_each_warehouse(items)
        )
        self.console.display_items(dict_of_items_with_amount_pro_warehouse)
        amount_of_all_items = self.manager.calculate_total_amount()
        self._actions.append(f"You have listed all {amount_of_all_items} items")

    def operation_search_an_item_and_place_an_order(self):
        item_name = self.console.ask_for_item_name()
        total_number_of_items = self.manager.calculate_item_total_amount(item_name)
        items_list = (
            list(self.manager._all_named_items_with_warehouse_id(item_name))
            if total_number_of_items > 0
            else []
        )
        if items_list:
            item_name = items_list[0][1].full_name()
        self.console.display_search_result(items_list)
        self._actions.append(f"You have searched for {item_name}")
        if not total_number_of_items:
            return
        if not self.do_you_want_to_order():
            self.console.print_order_cancelled()
            return
        if not self.user.is_authenticated:
            return
        ordered_number = self.order(item_name, total_number_of_items)
        if ordered_number:
            self.manager.remove_ordered_items()  # TODO
            self.console.print_order(ordered_number, item_name)
            self._actions.append(f"You have ordered {ordered_number} {item_name}")
        else:
            self.console.print_order_cancelled()

    def operation_browse_by_category(self):
        categories = self.manager.get_unique_categories()
        category_and_amount_of_items = (
            self.manager.calculate_amount_of_items_in_category(categories)
        )
        categories_numbered = {
            f"{id}": item for id, item in enumerate(category_and_amount_of_items, 1)
        }
        self.console.display_categories(categories_numbered)
        number = self.console.ask_for_number_of_category_to_browse()
        category_and_amount = categories_numbered.get(number)
        if category_and_amount:
            category, _ = category_and_amount
            items_of_category_and_warehouse_id = self.manager.get_all_items_of_category(
                category
            )
            self.console.display_all_items_of_category(
                category, items_of_category_and_warehouse_id
            )
            self._actions.append(f"You have searched for category: {category}")

    def operation_quit(self):
        self.user.bye(self._actions)

    def main(self):
        self._welcome_user()
        end_of_session = False
        while not end_of_session:
            operation_number = (
                self._main_menu()
            )  # display options, ask which one to pick
            # TODO: make separate controllers for these cases
            if operation_number == "1":
                # TODO:
                self.operation_list_items_by_warehouse()
            elif operation_number == "2":
                self.operation_search_an_item_and_place_an_order()
            elif operation_number == "3":
                self.operation_browse_by_category()
            elif operation_number == "4":
                end_of_session = True
                self.operation_quit()


if __name__ == "__main__":
    app = Controller()
    app.main()
