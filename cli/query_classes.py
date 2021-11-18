from datetime import datetime

import json

with open('/Users/temporaryadmin/projects/warehouse/cli/data.json', 'r') as f:
    stock = json.loads(f.read())


# everything to do with just one item (dictionary) goes here
class Item:
    """Almost a dataclass which represents an item in a warehouse"""
    def __init__(self, item) -> None:
        self.state = item['state']
        self.category = item['category']
        self.warehouse = item['warehouse']
        self.date_of_stock = item['date_of_stock']

    def name(self) -> str:
        return f"{self.state} {self.category}"

    def name_warehouse_info(self) -> str:
        return f"{self.name()}, Warehouse {self.warehouse}"

    def days_in_warehouse(self) -> str:
        today = datetime.today()
        in_stock_date = datetime.fromisoformat(self.date_of_stock)
        days = (today - in_stock_date).days
        return f"Warehouse {self.warehouse} in stock for {days} days."

    def __str__(self) -> str:
        return self.name()
    
    def __repr__(self) -> str:
        return f"Item({self.__str__()})"
    
# everything to do with items (plural!) goes here
class Storage:
    """Manages our warehouses"""
    def __init__(self, items: list[Item]) -> None:
        self.items = items
    
    def count_named(self, item_name: str) -> int:
        count = 0
        for item in self.items:
            if item_name == item.category:
                count +=1
        return count
    
    def unique_item_names(self) -> set[str]:
        return set(item.name() for item in self.items)

    def unique_category(self) -> set[str]:
        return set(item.category for item in self.items)

    def count_in_warehouse(self, warehouse_id: int, item_name: str) -> int:
        count = 0
        for item in self.items:
            if item_name.lower() == item.name().lower() and item.warehouse == warehouse_id:
                count += 1
        return count

    def category_amount(self):
        #for id, unique_category in enumerate(storage.unique_category(), 1):
        return {id: [unique_category, self.count_named(unique_category)] for id, unique_category in enumerate(storage.unique_category(), 1)} 

    def items_in_category(self, category_name) -> list[Item]:
        return [ item for item in self.items if item.category == category_name ]

    def items_by_full_name(self, full_name) -> list[Item]:
        return [ item for item in self.items if item.name().lower() == full_name.lower() ]

    def matching_item_name(self, input_name):
        for item in self.items:
            if item.name().lower() == input_name:
                return item.name()

    def plural_name(self, name: str) -> str:
        print(name)
        return name + 's' if name[-1].lower() != 's' else name

# every input and print goes here
class WarehouseOperator:
    """Runs the operations"""
    def __init__(self, storage: Storage) -> None:
        self.storage = storage

    def do_your_job(self):
        name = input("What is your user name? ").capitalize()
        print(f"\nHallo, {name}!\n")
        instruction = input(
            "1. List all items\n"
            "2. Search an item and place an order\n"
            "3. Browse by category\n"
            "4. Quit\n"
            "Type the number of the operation: "
        )
        if instruction == "1":
            self.operation1()
        elif instruction == "2":
            self.operation2()
        elif instruction == "3":
            self.operation3()
        elif instruction == "4":
            self.operation4()
        else:
            self._print_error(f"{instruction} is not a valid option.")
        print(f"\nThank you for a visit, {name}!")

    def operation1(self):
        for unique_item_name in self.storage.unique_item_names():
            print(f"\n- {unique_item_name}:\n")
            print(f"  Total items in warehouse 1: {storage.count_in_warehouse(1, unique_item_name)}")
            print(f"  Total items in warehouse 2: {storage.count_in_warehouse(2, unique_item_name)}")

    def operation2(self):
        choice = input("\nWhat is the name of the item?: ")
        amount_in_warehouse1 = self.storage.count_in_warehouse(1, choice)
        amount_in_warehouse2 = self.storage.count_in_warehouse(2, choice)
        total_amount = amount_in_warehouse1 + amount_in_warehouse2
        print(f"\nAmount available: {total_amount}\n")
        for item in self.storage.items_by_full_name(choice):
            print(item.days_in_warehouse())

        if amount_in_warehouse1 > 0 and amount_in_warehouse2 > 0:
            if amount_in_warehouse1 > amount_in_warehouse2:
                print(f"\nMaximum availability: {amount_in_warehouse1} in Warehouse 1.")
            elif amount_in_warehouse2 > amount_in_warehouse1:
                print(f"\nMaximum availability: {amount_in_warehouse2} in Warehouse 2.")
            else:
                print(f"\nBorh warehouses have the same amount of item: {amount_in_warehouse1}.")
        
        if total_amount > 0:
            self._order_operation(choice, total_amount)
            

    def operation3(self):
        self._category_menu()
        category = self._choose_category()
        print(f"\nList of {self.storage.plural_name(category.lower())} availabe:\n")
        for item in self.storage.items_in_category(category):
            print(item.name_warehouse_info())
        print()

    def operation4(self):
        return

    def _category_menu(self):
        print()
        for key, value in self.storage.category_amount().items():
            print(f"{key}. {value[0]} ({value[1]})")

    def _choose_category(self):
        choice = int(input("\nChoose the item: "))
        return self.storage.category_amount()[choice][0]

    def _order_operation(self, item, total_amount):
        operation = input("\nWould you like to order this item?(y/n) ")

        if operation not in {"y", "n"}:
            self._print_error(f"{operation} is not a valid option.")
            return
        if operation == "n":
            return

        amount_to_order = int(input("\nHow many would you like? "))

        if amount_to_order <= total_amount:
            if amount_to_order == 1:
                print(f"\n{amount_to_order} {self.storage.matching_item_name(item.lower())} has been ordered")
            else:
                print(f"\n{amount_to_order} {self.storage.plural_name(self.storage.matching_item_name(item.lower()))} have been ordered.")
            return

        message = f"There are not this many available. The maximum amount that can be ordered is {total_amount}"
        self._print_error(message)

        order_option2 =input("\nWould you like to order the maximum available?(y/n) ") 
        if order_option2 not in {"y", "n"}:
            self._print_error(f"{order_option2} is not a valid option.")
            return
        if order_option2 == "n":
            return
        if total_amount == 1:
            print(f"\n{total_amount} {self.storage.matching_item_name(item.lower())} have been ordered.")
        else:
            print(f"\n{total_amount} {self.storage.plural_name(self.storage.matching_item_name(item.lower()))} have been ordered.")               

    def _print_error(self, message) -> str:
        print()
        print(50*"*")
        print(message)
        print(50*"*")

storage = Storage([Item(item) for item in stock])
operator = WarehouseOperator(storage)

operator.do_your_job()