import unittest
from classes import Item, User, Employee
from datetime import datetime
from unittest.mock import patch
from io import StringIO
from app import ConsoleUserInterface, Controller, WarehouseManager


class TestWarehouseManager(unittest.TestCase):
    personnel_for_test_get_employee = [
        {
            "user_name": "Tomek",
            "password": "q",
            "head_of": [{"user_name": "Ania", "password": "hunter2", "head_of": []}],
        }
    ]
    warehouse_items_for_test = [
        {
            "state": "Black",
            "category": "Smartwatch",
            "warehouse": 4,
            "date_of_stock": "2021-07-20 03:51:06",
        },
        {
            "state": "High quality",
            "category": "Remote control",
            "warehouse": 2,
            "date_of_stock": "2021-07-29 01:19:44",
        },
        {
            "state": "Exceptional",
            "category": "Remote control",
            "warehouse": 4,
            "date_of_stock": "2019-08-26 23:15:50",
        },
        {
            "state": "Blue",
            "category": "Remote control",
            "warehouse": 3,
            "date_of_stock": "2020-09-02 07:19:05",
        },
        {
            "state": "Brand new",
            "category": "Remote control",
            "warehouse": 3,
            "date_of_stock": "2019-11-16 14:35:51",
        },
        {
            "state": "Blue",
            "category": "Remote control",
            "warehouse": 1,
            "date_of_stock": "2020-06-25 22:45:20",
        },
        {
            "state": "Blue",
            "category": "Remote control",
            "warehouse": 3,
            "date_of_stock": "2020-11-07 00:38:09",
        },
        {
            "state": "Blue",
            "category": "Remote control",
            "warehouse": 2,
            "date_of_stock": "2019-08-19 09:13:20",
        },
    ]

    def setUp(self) -> None:
        self.warehouse_manager = WarehouseManager(
            personnel_records=__class__.personnel_for_test_get_employee,
            item_records=__class__.warehouse_items_for_test,
        )

    def test_get_employee_in_list(self):
        # Do not Repeat Yourself (DRY!)
        tomek = self.warehouse_manager.get_employee("Tomek")
        self.assertIsNotNone(tomek)
        self.assertTrue(tomek.is_named("Tomek"))

    def test_get_employee_in_tree(self):
        ania = self.warehouse_manager.get_employee("Ania")
        self.assertIsNotNone(ania)
        self.assertTrue(ania.is_named("Ania"))

    def test_get_employee_not_found(self):
        krzysiek = self.warehouse_manager.get_employee("Krzysiek")
        self.assertIsNone(krzysiek)

    # def test_all_items(self):
    #     all_items = self.warehouse_manager._all_items()
    #     self.assertEqual(set(list(all_items)), set([Item(state='Black', category='Smartwatch',warehouse= 4, date_of_stock=datetime(2021,7,20,3,51,6)), Item(state='Brand new', category='Remote control', warehouse= 3, date_of_stock=datetime(2019,11,16,14,35,51)), Item(state="High quality", category="Remote control",warehouse=2, date_of_stock=datetime(2021,7,29,1,19,44)), Item(state="Blue", category="Remote control",warehouse=2, date_of_stock=datetime(2019,8,19,9,13,20)), Item(state="Blue", category="Remote control",warehouse=3, date_of_stock=datetime(2020,11,7,0,38,9)), Item(state="Exceptional", category="Remote control",warehouse=4, date_of_stock=datetime(2019,8,26,23,15,50)), Item(state="Blue", category="Remote control",warehouse=1, date_of_stock=datetime(2020,6,25,22,45,20)), Item(state="Blue", category="Remote control",warehouse=3, date_of_stock=datetime(2020,9,2,7,19,5))]))

    def test_all_items_with_warehouse_id(self):
        all_items = self.warehouse_manager._all_items_with_warehouse_id()
        self.assertEqual(
            set(all_items),
            set(
                [
                    (
                        4,
                        Item(
                            state="Black",
                            category="Smartwatch",
                            warehouse=4,
                            date_of_stock=datetime(2021, 7, 20, 3, 51, 6),
                        ),
                    ),
                    (
                        3,
                        Item(
                            state="Brand new",
                            category="Remote control",
                            warehouse=3,
                            date_of_stock=datetime(2019, 11, 16, 14, 35, 51),
                        ),
                    ),
                    (
                        2,
                        Item(
                            state="High quality",
                            category="Remote control",
                            warehouse=2,
                            date_of_stock=datetime(2021, 7, 29, 1, 19, 44),
                        ),
                    ),
                    (
                        2,
                        Item(
                            state="Blue",
                            category="Remote control",
                            warehouse=2,
                            date_of_stock=datetime(2019, 8, 19, 9, 13, 20),
                        ),
                    ),
                    (
                        3,
                        Item(
                            state="Blue",
                            category="Remote control",
                            warehouse=3,
                            date_of_stock=datetime(2020, 11, 7, 0, 38, 9),
                        ),
                    ),
                    (
                        4,
                        Item(
                            state="Exceptional",
                            category="Remote control",
                            warehouse=4,
                            date_of_stock=datetime(2019, 8, 26, 23, 15, 50),
                        ),
                    ),
                    (
                        1,
                        Item(
                            state="Blue",
                            category="Remote control",
                            warehouse=1,
                            date_of_stock=datetime(2020, 6, 25, 22, 45, 20),
                        ),
                    ),
                    (
                        3,
                        Item(
                            state="Blue",
                            category="Remote control",
                            warehouse=3,
                            date_of_stock=datetime(2020, 9, 2, 7, 19, 5),
                        ),
                    ),
                ]
            ),
        )

    def test_all_named_items_with_warehouse_id(self):
        all_items = self.warehouse_manager._all_named_items_with_warehouse_id(
            "Blue Remote control"
        )
        self.assertEqual(
            set(all_items),
            set(
                [
                    (
                        2,
                        Item(
                            state="Blue",
                            category="Remote control",
                            warehouse=2,
                            date_of_stock=datetime(2019, 8, 19, 9, 13, 20),
                        ),
                    ),
                    (
                        3,
                        Item(
                            state="Blue",
                            category="Remote control",
                            warehouse=3,
                            date_of_stock=datetime(2020, 11, 7, 0, 38, 9),
                        ),
                    ),
                    (
                        1,
                        Item(
                            state="Blue",
                            category="Remote control",
                            warehouse=1,
                            date_of_stock=datetime(2020, 6, 25, 22, 45, 20),
                        ),
                    ),
                    (
                        3,
                        Item(
                            state="Blue",
                            category="Remote control",
                            warehouse=3,
                            date_of_stock=datetime(2020, 9, 2, 7, 19, 5),
                        ),
                    ),
                ]
            ),
        )

    def test_all_items_of_category_with_warehouse_id(self):
        all_items = self.warehouse_manager._all_items_of_category_with_warehouse_id(
            "Remote control"
        )
        self.assertEqual(
            set(all_items),
            set(
                [
                    (
                        3,
                        Item(
                            state="Brand new",
                            category="Remote control",
                            warehouse=3,
                            date_of_stock=datetime(2019, 11, 16, 14, 35, 51),
                        ),
                    ),
                    (
                        2,
                        Item(
                            state="High quality",
                            category="Remote control",
                            warehouse=2,
                            date_of_stock=datetime(2021, 7, 29, 1, 19, 44),
                        ),
                    ),
                    (
                        2,
                        Item(
                            state="Blue",
                            category="Remote control",
                            warehouse=2,
                            date_of_stock=datetime(2019, 8, 19, 9, 13, 20),
                        ),
                    ),
                    (
                        3,
                        Item(
                            state="Blue",
                            category="Remote control",
                            warehouse=3,
                            date_of_stock=datetime(2020, 11, 7, 0, 38, 9),
                        ),
                    ),
                    (
                        4,
                        Item(
                            state="Exceptional",
                            category="Remote control",
                            warehouse=4,
                            date_of_stock=datetime(2019, 8, 26, 23, 15, 50),
                        ),
                    ),
                    (
                        1,
                        Item(
                            state="Blue",
                            category="Remote control",
                            warehouse=1,
                            date_of_stock=datetime(2020, 6, 25, 22, 45, 20),
                        ),
                    ),
                    (
                        3,
                        Item(
                            state="Blue",
                            category="Remote control",
                            warehouse=3,
                            date_of_stock=datetime(2020, 9, 2, 7, 19, 5),
                        ),
                    ),
                ]
            ),
        )

    def test_calculate_total_amount(self):
        total_amount = self.warehouse_manager.calculate_total_amount()
        self.assertEqual(total_amount, 8)

    def test_calculate_item_amount_in_warehouse_items_found_in_warehouse_1_2_and_3_asked_for_2(
        self,
    ):
        test1 = self.warehouse_manager.calculate_item_amount_in_warehouse(
            2, "Blue Remote control"
        )
        self.assertEqual(test1, 1)

    def test_calculate_item_amount_in_warehouse_items_found_in_warehouse_1_2_and_3_asked_for_3(
        self,
    ):
        test2 = self.warehouse_manager.calculate_item_amount_in_warehouse(
            3, "Blue Remote control"
        )
        self.assertEqual(test2, 2)

    def test_calculate_item_amount_in_warehouse_items_found_in_warehouse_1_2_and_3_asked_for_4(
        self,
    ):
        test3 = self.warehouse_manager.calculate_item_amount_in_warehouse(
            4, "Blue Remote control"
        )
        self.assertEqual(test3, 0)

    def test_calculate_item_amount_in_warehouse_items_found_in_warehouse_1_2_and_3_asked_for_1_case_insensitive(
        self,
    ):
        test4 = self.warehouse_manager.calculate_item_amount_in_warehouse(
            2, "blue REMOTE Control"
        )
        self.assertEqual(test4, 1)

    def test_calculate_item_total_amount_4_items_in_warehouses_1_2_and_3(self):
        test5 = self.warehouse_manager.calculate_item_total_amount(
            "Blue Remote control"
        )
        self.assertEqual(test5, 4)

    def test_calculate_item_total_amount_item_not_found(self):
        test6 = self.warehouse_manager.calculate_item_total_amount(
            "White Remote control"
        )
        self.assertEqual(test6, 0)

    def test_get_unique_item_names(self):
        unique_names = self.warehouse_manager.get_unique_item_names()
        self.assertEqual(
            unique_names,
            set(
                [
                    "Black Smartwatch",
                    "High quality Remote control",
                    "Exceptional Remote control",
                    "Blue Remote control",
                    "Brand new Remote control",
                ]
            ),
        )

    def test_get_amount_of_item_in_each_warehouse(self):
        items = set(
            [
                "New Smartwatch",
                "Black Smartwatch",
                "High quality Remote control",
                "Exceptional Remote control",
                "Blue Remote control",
                "Brand new Remote control",
            ]
        )
        amount_of_item_in_each_warehouse = (
            self.warehouse_manager.get_amount_of_item_in_each_warehouse(items)
        )
        self.assertDictEqual(
            amount_of_item_in_each_warehouse,
            {
                "Brand new Remote control": {1: 0, 2: 0, 3: 1, 4: 0},
                "Blue Remote control": {1: 1, 2: 1, 3: 2, 4: 0},
                "Black Smartwatch": {1: 0, 2: 0, 3: 0, 4: 1},
                "High quality Remote control": {1: 0, 2: 1, 3: 0, 4: 0},
                "Exceptional Remote control": {1: 0, 2: 0, 3: 0, 4: 1},
                "New Smartwatch": {1: 0, 2: 0, 3: 0, 4: 0},
            },
        )

    def test_get_unique_categories(self):
        unique_categories = self.warehouse_manager.get_unique_categories()
        self.assertSetEqual(unique_categories, set(["Remote control", "Smartwatch"]))

    def test_calculate_amount_of_items_in_category(self):
        unique_categories = set(["Remote control", "Smartwatch", "Book"])
        amount_of_items_in_category = (
            self.warehouse_manager.calculate_amount_of_items_in_category(
                unique_categories
            )
        )
        self.assertListEqual(
            sorted(amount_of_items_in_category),
            sorted([("Remote control", 7), ("Smartwatch", 1), ("Book", 0)]),
        )

    def test_get_all_items_of_category(self):
        all_items_of_category = self.warehouse_manager.get_all_items_of_category(
            "Remote control"
        )
        self.assertListEqual(
            sorted(all_items_of_category),
            sorted(
                [
                    ("Brand new Remote control", 3),
                    ("Blue Remote control", 1),
                    ("Blue Remote control", 2),
                    ("Blue Remote control", 3),
                    ("Blue Remote control", 3),
                    ("High quality Remote control", 2),
                    ("Exceptional Remote control", 4),
                ]
            ),
        )

    def test_get_all_items_of_category_category_not_in_stock(self):
        all_items_of_category2 = self.warehouse_manager.get_all_items_of_category(
            "Book"
        )
        self.assertListEqual(all_items_of_category2, [])


class TestConsoleUserInterface(unittest.TestCase):
    def setUp(self):
        self.cui = ConsoleUserInterface()

    @patch("builtins.input", return_value="USER_TYPED_THIS")
    def test_ask_user_name(self, _input):
        self.assertEqual(self.cui.ask_user_name(), "USER_TYPED_THIS")

    @patch("sys.stdout", new_callable=StringIO)
    def test_greet_user_user(self, output):
        user = User(user_name="Tomek")
        self.cui.greet_user(user)
        self.assertEqual(
            output.getvalue(),
            "\nHello, Tomek!\nWelcome to our Warehouse Database.\nIf you don't find what you are looking for, please ask one of our staff members to assist you.\n",
        )

    @patch("sys.stdout", new_callable=StringIO)
    def test_print_greet_user_employee(self, output):
        user = Employee(user_name="Marc", password="janis")
        self.cui.greet_user(user)
        self.assertEqual(
            output.getvalue(),
            "\nHello, Marc!\nIf you experience a problem with the system, please contact technical support.\n",
        )

    @patch("sys.stdout", new_callable=StringIO)
    def test_print_greet_user_anonymous(self, output):
        user = User(user_name="")
        self.cui.greet_user(user)
        self.assertEqual(
            output.getvalue(),
            "\nHello, Anonymous!\nWelcome to our Warehouse Database.\nIf you don't find what you are looking for, please ask one of our staff members to assist you.\n",
        )

    @patch("builtins.input", return_value="3")
    def test_ask_for_operation(self, _input):
        self.assertEqual(self.cui.ask_for_operation(), "3")

    # NOTE: patch input AND output (order matters for parameter order in the method)
    @patch("sys.stdout", new_callable=StringIO)
    @patch("builtins.input", side_effect=["INVALID", "3"])
    def test_ask_for_operation_invalid_input(self, _input, output):
        self.assertEqual(self.cui.ask_for_operation(), "3")
        # NOTE: LOOK AT THIS! You can just match a little bit of print-ed output :-)
        self.assertRegex(output.getvalue(), r"No operation INVALID")
        self.assertNotRegex(output.getvalue(), r"No operation 3")

    @patch("sys.stdout", new_callable=StringIO)
    def test_print_no_operation_error(self, output):
        self.cui.print_no_operation_error("INVALID")
        self.assertEqual(
            output.getvalue(), "\n\n\t***** No operation INVALID! *****\n\n"
        )

    @patch("sys.stdout", new_callable=StringIO)
    def test_display_operations(self, output):
        self.cui.display_operations()
        self.assertEqual(
            output.getvalue(),
            "\nOptions:\n1. List all items\n2. Search an item and place an order\n3. Browse by category\n4. Quit\n",
        )

    @patch("sys.stdout", new_callable=StringIO)
    def test_display_items(self, output):
        items = {
            "Red Laptop": {1: 2, 2: 3, 4: 1},
            "Blue Headphones": {1: 4, 2: 1, 3: 5, 4: 7},
        }
        self.cui.display_items(items)
        self.assertEqual(
            output.getvalue(),
            "\nRed Laptop\n\nTotal amount of item in Warehouse 1: 2\nTotal amount of item in Warehouse 2: 3\nTotal amount of item in Warehouse 4: 1\n\nBlue Headphones\n\nTotal amount of item in Warehouse 1: 4\nTotal amount of item in Warehouse 2: 1\nTotal amount of item in Warehouse 3: 5\nTotal amount of item in Warehouse 4: 7\n",
        )

    @patch("builtins.input", return_value="Red Laptop")
    def test_ask_for_item_name(self, _input):
        self.assertEqual(self.cui.ask_for_item_name(), "Red Laptop")

    @patch("sys.stdout", new_callable=StringIO)
    def test_display_search_result(self, output):
        today = datetime.now()
        items = [
            (
                2,
                Item(
                    state="Blue",
                    category="Remote control",
                    warehouse=2,
                    date_of_stock=datetime(2019, 8, 19, 9, 13, 20),
                ),
            ),
            (
                3,
                Item(
                    state="Blue",
                    category="Remote control",
                    warehouse=3,
                    date_of_stock=datetime(2020, 11, 7, 0, 38, 9),
                ),
            ),
            (
                1,
                Item(
                    state="Blue",
                    category="Remote control",
                    warehouse=1,
                    date_of_stock=datetime(2020, 6, 25, 22, 45, 20),
                ),
            ),
            (
                3,
                Item(
                    state="Blue",
                    category="Remote control",
                    warehouse=3,
                    date_of_stock=datetime(2020, 9, 2, 7, 19, 5),
                ),
            ),
        ]
        self.cui.display_search_result(items)
        self.assertEqual(
            output.getvalue(),
            f"\n4 Blue Remote control in stock\n\tIn Warehouse 2 for {(today - datetime(2019, 8, 19, 9, 13, 20)).days} days\n\tIn Warehouse 3 for {(today - datetime(2020, 11, 7, 0, 38, 9)).days} days\n\tIn Warehouse 1 for {(today - datetime(2020, 6, 25, 22, 45, 20)).days} days\n\tIn Warehouse 3 for {(today - datetime(2020, 9, 2, 7, 19, 5)).days} days\n",
        )

    @patch("sys.stdout", new_callable=StringIO)
    def test_display_all_items_of_category(self, output):
        category = "Laptop"
        items = [
            ("Red Laptop", 1),
            ("Almost new Laptop", 1),
            ("White Laptop", 2),
            ("Second hand Laptop", 3),
            ("New Laptop", 4),
            ("Black Laptop", 4),
        ]
        self.cui.display_all_items_of_category(category, items)
        self.assertEqual(
            output.getvalue(),
            "\nLaptop:\nRed Laptop, Warehouse 1\nAlmost new Laptop, Warehouse 1\nWhite Laptop, Warehouse 2\nSecond hand Laptop, Warehouse 3\nNew Laptop, Warehouse 4\nBlack Laptop, Warehouse 4\n",
        )

    @patch("builtins.input", return_value="y")
    def test_ask_if_user_want_to_order_yes(self, _input):
        self.assertTrue(self.cui.ask_if_user_want_to_order())

    @patch("builtins.input", return_value="n")
    def test_ask_if_user_want_to_order_no(self, _input):
        self.assertFalse(self.cui.ask_if_user_want_to_order())

    @patch("sys.stdout", new_callable=StringIO)
    @patch("builtins.input", side_effect=["INVALID", "y"])
    def test_ask_if_user_want_to_order_first_not_valid(self, _input, output):
        self.assertTrue(self.cui.ask_if_user_want_to_order())
        self.assertRegex(output.getvalue(), r"No operation INVALID")

    @patch("sys.stdout", new_callable=StringIO)
    @patch("builtins.input", side_effect=["INVALID", "y"])
    def test_ask_if_user_want_to_order_max_amount_first_not_valid(self, _input, output):
        self.assertTrue(self.cui.ask_if_user_want_to_order_max_amount(10))
        self.assertRegex(output.getvalue(), r"No operation INVALID")

    @patch("builtins.input", return_value="y")
    def test_ask_if_user_want_to_order_max_amount_yes(self, _input):
        self.assertTrue(self.cui.ask_if_user_want_to_order_max_amount(10))

    @patch("builtins.input", return_value="n")
    def test_ask_if_user_want_to_order_max_amount_no(self, _input):
        self.assertFalse(self.cui.ask_if_user_want_to_order_max_amount(10))

    @patch("sys.stdout", new_callable=StringIO)
    def test_print_not_enough_items_in_stock(self, output):
        self.cui.print_not_enough_items_in_stock(8, "Red Laptop")
        self.assertEqual(output.getvalue(), "\nThere are only 8 Red Laptop\n")

    @patch("sys.stdout", new_callable=StringIO)
    def test_print_order(self, output):
        self.cui.print_order(8, "Red Laptop")
        self.assertEqual(output.getvalue(), "\nYou have ordered 8 Red Laptop\n")

    @patch("sys.stdout", new_callable=StringIO)
    def test_print_order_cancelled(self, output):
        self.cui.print_order_cancelled()
        self.assertEqual(output.getvalue(), "\nOrder cancelled\n")

    @patch("sys.stdout", new_callable=StringIO)
    def test_display_categories(self, output):
        categories_numbered = {
            "1": ("Laptop", 4),
            "2": ("Headphones", 15),
            "3": ("Monitor", 10),
        }
        self.cui.display_categories(categories_numbered)
        self.assertEqual(
            output.getvalue(), "\n1. Laptop (4)\n2. Headphones (15)\n3. Monitor (10)\n"
        )

    @patch("builtins.input", return_value="5")
    def test_ask_for_number_of_category_to_browse(self, _input):
        self.assertEqual(self.cui.ask_for_number_of_category_to_browse(), "5")

    @patch("sys.stdout", new_callable=StringIO)
    @patch("builtins.input", side_effect=["not_a_number", "10"])
    def test_ask_how_much_to_order(self, _input, output):
        self.assertTrue(self.cui.ask_how_much_to_order())
        self.assertRegex(output.getvalue(), r"Input not valid!")

    @patch("builtins.input", return_value="qwe321")
    def test_ask_for_password(self, _input):
        self.assertEqual(self.cui.ask_for_password(), "qwe321")


class ControllerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.app = Controller()
        self.user = User("Anna")
        self.employee = Employee("Tomek", "qwe321")
        self.cui = ConsoleUserInterface()

    # TODO more tests
    # @patch("app.ConsoleUserInterface.ask_for_password", return_value="qwe321")
    # def test_log_in(self, _input):
    #     self.user = Employee("Tomek", "qwe321")
    #     print(self.user.is_authenticated)
    #     self.assertTrue(self.app.log_in())

    @patch("app.Controller.log_in")
    @patch("app.ConsoleUserInterface.ask_if_user_want_to_order", return_value="y")
    def test_do_you_want_to_order(self, _input, log_in_mock):
        self.app.do_you_want_to_order
        log_in_mock.log_in.assert_called


if __name__ == "__main__":
    unittest.main()
