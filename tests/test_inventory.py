import os
import unittest
from inventory import InventoryManagement

class TestInventory(unittest.TestCase):

    def setUp(self):
        self.test_file = "test_inventory.txt"
        self.manager = InventoryManagement(self.test_file)

        # Create a sample file
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write("Item_ID:1\n")
            f.write("Item_Name:Pen\n")
            f.write("Category:Stationery\n")
            f.write("Quantity:10\n")
            f.write("Price:5\n")
            f.write("Supplier_Name:ABC\n")
            f.write("Added_Date:2025-09-21\n")
            f.write("_____________________________________\n")

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_generate_item_id(self):
        self.assertEqual(self.manager.generate_item_id(), 2)

    def test_view_all_inventory_id(self):
        self.manager.view_all_inventory_ID()
        # Just ensures no crash

if __name__ == "__main__":
    unittest.main()
