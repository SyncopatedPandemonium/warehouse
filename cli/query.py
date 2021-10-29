from data import warehouse1, warehouse2

user_name = ""
while len(user_name) == 0:
    user_name = input("What is your user name? ")
print(f"\nHello, {user_name}!\n"
    "What would you like to do?")

operations = input(
    "1. List items by warehouse\n"
    "2. Search an item and place an order\n"
    "3. Quit\nType the number of the operation: "
    )

if operations == "1":
    print("\nItems in warehouse 1:")
    for item in set(warehouse1):
        print(f"- {item}")
    print("\nItems in warehouse 2:")
    for item in set(warehouse2):
        print(f"- {item}")
elif operations == "2":
    chosen_item = input("\nWhat is the name of the item? ")  # Letting user choose the item
    amount_available1 = warehouse1.count(chosen_item)
    amount_available2 = warehouse2.count(chosen_item)
    amount_available = int(amount_available1) + int(amount_available2)  # total amount of items in both warehouses
    print(f"Amount available: {amount_available}")
    if chosen_item in warehouse1 and chosen_item in warehouse2:  # chosen item in both warehouses
        print(f"Location: Both warehouses")
        if amount_available2 > amount_available1:
            print(f"Maximum availability: {amount_available2} in Warehouse 2.")
        elif amount_available2 < amount_available1:
            print(f"Maximum availability: {amount_available1} in Warehouse 1.")
        else:
            print(f"Borh warehouses have the same amount of item: {amount_available1}.")
    elif chosen_item in warehouse1:  # chosen item in warehouse 1
        print(f"Location: Warehouse 1")
    elif chosen_item in warehouse2:  # chosen item in warehouse 2
        print(f"Location: Warehouse 2")
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
    pass
else:
    print()
    print(50*"*")
    print(f"{operations} is not a valid operation.")
    print(50*"*")

print(f"\nThank you for your visit, {user_name}!")