#from data_old import warehouse1, warehouse2
from datetime import datetime

import json

with open('/Users/temporaryadmin/projects/warehouse/cli/data.json', 'r') as f:
    stock = json.loads(f.read())

def full_name_of_item(item_info: dict) ->str:
    return f"{item_info['state']} {item_info['category']}"

def items_in_warehouse_lower_case(warehouse_number: int, data:dict = stock ) -> list:
    return [full_name_of_item(item).lower() for item in data if item['warehouse'] == warehouse_number]

def items_in_warehouse(warehouse_number: int, data:dict = stock ) -> list:
    return [full_name_of_item(item) for item in data if item['warehouse'] == warehouse_number]

def category_in_warehouse(data:dict = stock ) -> set:
    return set([item['category'] for item in data])

def is_in_warehouse(item_name: str, warehouse_number: int) -> bool:
        return True if item_name in items_in_warehouse_lower_case(warehouse_number) else False

def amount_in_warehouse(item_name: str, warehouse_number: int) -> int:
    return items_in_warehouse_lower_case(warehouse_number).count(item_name)

def days_in_warehouse(item_name):
        today = datetime.today()
        in_stock_date = datetime.fromisoformat(item_name['date_of_stock'])
        days = (today - in_stock_date).days
        return item_name['warehouse'], days

def total_amount(item_name):
    amount = 0
    for item in stock:
        if item['category'] == item_name:
            amount += 1
    return amount


warehouse1 = items_in_warehouse_lower_case(1)
warehouse2 = items_in_warehouse_lower_case(2)

user_name = ""
while len(user_name) == 0:
    user_name = input("What is your user name? ").capitalize()
print(f"\nHello, {user_name}!\n"
    "What would you like to do?")

operations = ""
while operations == "":
    operations = input(
        "1. List all items\n"
        "2. Search an item and place an order\n"
        "3. Browse by category\n"
        "4. Quit\nType the number of the operation: "
        )

if operations == "1":
    print("\nItems in warehouse:")
    for item in set(items_in_warehouse(1)+items_in_warehouse(2)):
        print(f"\n- {item}\n")
        print(f"Total items in warehouse 1: {amount_in_warehouse(item,1)}")
        print(f"Total items in warehouse 2: {amount_in_warehouse(item,2)}")

elif operations == "2":
    chosen_item = input("\nWhat is the name of the item? ").lower() # Letting user choose the item
    amount_available1 = amount_in_warehouse(chosen_item,1)
    amount_available2 = amount_in_warehouse(chosen_item,2)
    amount_available = int(amount_available1) + int(amount_available2)  # total amount of items in both warehouses
    print(f"\nAmount available: {amount_available}\n")
    if chosen_item in warehouse1 and chosen_item in warehouse2:  # chosen item in both warehouses
        print(f"Location:")
        for item in stock:
            if full_name_of_item(item).lower() == chosen_item:
                warehouse_number, days = days_in_warehouse(item)
                print(f"Warehouse {warehouse_number} in stock for {days} days.")
        if amount_in_warehouse(chosen_item,2) > amount_in_warehouse(chosen_item,1):
            print(f"\nMaximum availability: {amount_available2} in Warehouse 2.")
        elif amount_available2 < amount_available1:
            print(f"\nMaximum availability: {amount_available1} in Warehouse 1.")
        else:
            print(f"Borh warehouses have the same amount of item: {amount_available1}.")
    elif chosen_item in warehouse1:  # chosen item in warehouse 1
        for item in stock:
            if full_name_of_item(item).lower() == chosen_item:
                warehouse_number, days = days_in_warehouse(item)
                print(f"Warehouse {warehouse_number} in stock for {days} days.")
        #print(f"Location: Warehouse 1")
    elif chosen_item in warehouse2:  # chosen item in warehouse 2
        for item in stock:
            if full_name_of_item(item).lower() == chosen_item:
                warehouse_number, days = days_in_warehouse(item)
                print(f"Warehouse {warehouse_number} in stock for {days} days.")
        #print(f"Location: Warehouse 2")
    else:    # chosen item not in stock
        print(f"Location: Not in stock")

    if chosen_item in warehouse1 or chosen_item in warehouse2:  # letting user decide if he wants to order the chosen item
        order_option = input("\nWould you like to order this item?(y/n) ")
        if order_option == "y":
            amount_to_order = int(input("How many would you like? "))
            if amount_to_order > amount_available:  # amount that user wants to order is greater than amount in both stores
                print()
                print(50*"*")
                print(f"There are not this many available. The maximum amount that can be ordered is {amount_available}")
                print(50*"*")
                order_option2 =input("\nWould you like to order the maximum available?(y/n) ")  # letting user decide if he wants to order max amount of the chosen item
                if order_option2 == "y":
                    print(f"{amount_available} {chosen_item} have been ordered.")
                elif order_option2 == "n":
                    pass
                else:
                    print()
                    print(50*"*")
                    print(f"{order_option} is not a valid option.")
                    print(50*"*")
            elif amount_to_order <= amount_available:
                    print(f"{amount_to_order} {chosen_item} have been ordered.")
        elif order_option == "n":
            pass
        else:
            print()
            print(50*"*")
            print(f"{order_option} is not a valid option.")
            print(50*"*")
    else:
        pass
elif operations == "3":
    items = {f"{id}": item for id, item in enumerate(category_in_warehouse(stock), 1)}
    for key, value in items.items():
        print(f"{key}. {value} ({total_amount(value)})")
    chosen_item_number = (input('Type the number of the category to browse: '))
    name = items[chosen_item_number]
    plural_name = name.lower() + 's' if name[-1] != 's' else name.lower()
    print(f"\nList of {plural_name} availabe:\n")
    for item in stock:
        if item['category'] == name:
            print(f"{item['state']} {item['category'].lower()}, Warehouse {item['warehouse']}.")

elif operations == "4":
    pass
else:
    print()
    print(50*"*")
    print(f"{operations} is not a valid operation.")
    print(50*"*")

print(f"\nThank you for your visit, {user_name}!")