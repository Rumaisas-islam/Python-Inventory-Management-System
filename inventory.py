import re
import shutil
from datetime import datetime

class InventoryManagement:
  def __init__(self,filename="inventory.txt"):
    self.filename=filename
    
  # -------------------- Backup --------------------
  def create_backup(self):
    backup_file = self.filename.replace(".txt", "_backup.txt")
    shutil.copy(self.filename, backup_file)
    print(f" Backup created as: {backup_file}")

  # -------------------- ID Generator -------------------
  def generate_item_id(self):
        """
        Read file reversed and find the last line that starts with 'Item_ID:'.
        Return last_id + 1, or 1 if none found / file missing.
        """
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except FileNotFoundError:
            return 1

        # iterate reversed to find last Item_ID
        for line in reversed(lines):
            line = line.strip()
            if line.startswith("Item_ID:"):
                try:
                    last_id = int(line.split(":", 1)[1].strip())
                    return last_id + 1
                except ValueError:
                    # malformed line — continue searching earlier lines
                    continue
        return 1

  # -------------------- Add Inventory --------------------     
  def add_inventory(self):
    Item_ID=self.generate_item_id()

    while True:
      Item_Name=input("Enter Item Name: ").strip()
      if Item_Name.replace(" ","").isalpha():
        break
      else:
        print("Invalid input!Item_Name should only contain alphabets")
    while True:
      Category=input("Enter category: ").strip()
      if Category.replace(" ","").isalpha():
        break
      else:
        print("Invalid input!Category should only contain alphabets")
    while True:
      Quantity=input("Enter quantity: ").strip()
      if Quantity.isdigit():
        break
      else:
        print("Invalid input!Quantity should only contain numbers")
    while True:
      Price=input("Enter price: ").strip()
      if Price.isdigit():
        break
      else:
        print("Invalid input!Price should only contain numbers")
    while True:
      Supplier_Name=input("Enter supplier name: ").strip()
      if Supplier_Name.replace(" ","").isalpha():
        break
      else:
        print("Invalid input!Supplier_name should only contain alphabets")

    Added_Date=datetime.now().strftime("%Y-%m-%d")
    try:
      with open(self.filename,"a",encoding="utf-8") as f:
        f.write(f"Item_ID:{Item_ID}\n")
        f.write(f"Item_Name:{Item_Name}\n")
        f.write(f"Category:{Category}\n")
        f.write(f"Quantity:{Quantity}\n")
        f.write(f"Price:{Price}\n")
        f.write(f"Supplier_Name:{Supplier_Name}\n")
        f.write(f"Added_Date:{Added_Date}\n")
        f.write("_____________________________________\n")
    except Exception as e:
      print(f"Error saving inventory:{e}")

  # -------------------- Search Inventory --------------------
  def search_inventory(self,field):
    try:
      with open(self.filename,"r",encoding="utf-8") as f:
        lines=f.readlines()
    except FileNotFoundError:
       print("No file found")
       return
    block=[]
    found=False
    value=input(f"Enter the {field.lower()} to search inventory: ").strip()
    pattern = rf"^{re.escape(field)}:.*{re.escape(value)}.*$"
    for line in lines:
       if line.strip()=="_____________________________________":
          if any(re.match(pattern, l.strip(), re.IGNORECASE) for l in block):
            print("_____Inventory Found_____")
            print("\n".join(block))
            print("_____________________________________")
            found=True
          block=[]
       else:
          block.append(line.strip())
    if block:
       if any(re.match(pattern, l.strip(), re.IGNORECASE) for l in block):
            print("_____Inventory Found_____")
            print("\n".join(block))
            print("_____________________________________")
            found=True
    if not found:
       print(f"No inventory found with that {field.lower()}")

  # -------------------- Delete Inventory --------------------
  def delete_inventory(self,field):
     try:
        with open(self.filename,"r",encoding="utf-8") as f:
           lines=f.readlines()
     except FileNotFoundError:
        print("No file found")
        return
     block,new_lines=[],[]
     value=input(f"Enter the {field.lower()} to delete inventory: ").strip()
     pattern = rf"^{re.escape(field)}:.*{re.escape(value)}.*$"
     found_any=False
     for line in lines:
        if line.strip() == "_____________________________________":
           if any(re.match(pattern, l.strip(), re.IGNORECASE) for l in block):
              print("_____Inventory found_____")
              print("".join(block))
              confirm=input("Are you sure you want to delete this (yes/no): ").strip().lower()
              if confirm == "yes":
                 self.create_backup()
                 found_any=True
              else:
                 new_lines.extend(block+["_____________________________________\n"])
           else:
              new_lines.extend(block+["_____________________________________\n"])
           block=[]
        else:
           block.append(line)
     if found_any:
        with open(self.filename,"w",encoding="utf-8") as f:
          f.writelines(new_lines)
        print("Inventory deleted successfully")
     else:
        print(f"No inventory found with that {field.lower()}")

  # -------------------- Update Inventory --------------------
  def update_inventory(self,field):
    try:
      with open(self.filename,"r",encoding="utf-8") as f:
        lines=f.readlines()
    except FileNotFoundError:
      print("No file found")
      return
    value=input(f"Enter the {field.lower()} to update inventory: ").strip()
    pattern = rf"^{re.escape(field)}:.*{re.escape(value)}.*$"
    new_lines,block=[],[]
    found_any=False
    for line in lines:
      if line.strip()=="_____________________________________":
        if any(re.match(pattern, l.strip(), re.IGNORECASE) for l in block):
          print("_____Inventory Found_____")
          print("".join(block))
          confirm=input("Are you sure you want to update this inventory(yes/no): ").strip().lower()
          if confirm == "yes":
            self.create_backup()
            found_any=True
            Item_ID = next((l.split(":", 1)[1].strip() for l in block if l.startswith("Item_ID:")), None)
            while True:
              Item_Name=input("Enter Item Name: ").strip()
              if Item_Name.replace(" ","").isalpha():
                break
              else:
                print("Invalid input!Item_Name should only contain alphabets")
            while True:
              Category=input("Enter category: ").strip()
              if Category.replace(" ","").isalpha():
                break
              else:
                print("Invalid input!Category should only contain alphabets")
            while True:
              Quantity=input("Enter quantity: ").strip()
              if Quantity.isdigit():
                break
              else:
                print("Invalid input!Quantity should only contain numbers")
            while True:
              Price=input("Enter price: ").strip()
              if Price.isdigit():
                break
              else:
                print("Invalid input!Price should only contain numbers")
            while True:
              Supplier_Name=input("Enter supplier name: ").strip()
              if Supplier_Name.replace(" ","").isalpha():
                break
              else:
                print("Invalid input!Supplier_name should only contain alphabets")

            Added_Date=datetime.now().strftime("%Y-%m-%d")

            new_lines.append(f"Item_ID:{Item_ID}\n")
            new_lines.append(f"Item_Name:{Item_Name}\n")
            new_lines.append(f"Category:{Category}\n")
            new_lines.append(f"Quantity:{Quantity}\n")
            new_lines.append(f"Price:{Price}\n")
            new_lines.append(f"Supplier_Name:{Supplier_Name}\n")
            new_lines.append(f"Added_Date:{Added_Date}\n")
            new_lines.append("_____________________________________\n")

          else:
            new_lines.extend(block+["_____________________________________\n"])
        else:
          new_lines.extend(block+["_____________________________________\n"])
        block=[]
      else:
        block.append(line)
    if found_any:
      with open(self.filename,"w",encoding="utf-8") as f:
        f.writelines(new_lines)
      print("Inventory Updated successfully")
    else:
      print(f"No inventory found with that {field.lower()}")

  # -------------------- View Inventories --------------------
  def view_all_inventory_ID(self):
    try:
      with open(self.filename,"r",encoding="utf-8") as f:
        lines=f.readlines()
    except FileNotFoundError:
      print("No file found")
      return
    IDS = [line.split(":", 1)[1].strip() for line in lines if line.startswith("Item_ID:")]
    if IDS:
      print("_____Item ID_____")
      for idx,ID in enumerate(IDS,1):
        print(f"{idx}.{ID}")
    else:
      print("No ID found")

  def view_all_inventory_names(self):
    try:
      with open(self.filename,"r",encoding="utf-8") as f:
        lines=f.readlines()
    except FileNotFoundError:
      print("No file found")
      return
    names = [line.split(":", 1)[1].strip() for line in lines if line.startswith("Item_Name:")]
    if names:
      print("_____Item Name_____")
      for idx,name in enumerate(names,1):
        print(f"{idx}.{name}")
    else:
      print("No Item Name found")

  def view_all_inventory(self):
    try:
      with open(self.filename,"r",encoding="utf-8") as f:
        lines=f.readlines()
    except FileNotFoundError:
      print("No file found")
      return
    found=False
    block=[]
    task_num=1
    for line in lines:
      if line.strip()=="_____________________________________":
        if block:
          print(f"\nTask{task_num}:")
          print("".join(block).strip())
          found=True
          task_num+=1
        block=[]
      else:
        block.append(line)
    if not found:
      print("No inventory found")
      
if __name__ == "__main__":
  obj = InventoryManagement()

  while True:
    print("\n--- Inventory Management ---")
    print("1.Add Inventory")
    print("2.Search Inventory")
    print("3.Delete Inventory")
    print("4.Update Inventory")
    print("5.View all inventory id")
    print("6.View all inventory names")
    print("7.View all inventories")
    print("8.Exit\n")

    choice=input("Enter your choice(1-8): ").strip()

    if choice == "1":
      obj.add_inventory()

    elif choice == "2":
      field=input("Search by(Item_ID/Item_Name/Category/Supplier_Name): ").strip()
      if field in ["Item_ID","Item_Name","Category","Supplier_Name"]:
        obj.search_inventory(field)
      else:
        print("Invalid choice!Enter choice from(Item_ID/Item_Name/Category/ Supplier_Name).")

    elif choice == "3":
      field=input("Delete by(Item_ID/Item_Name/Category/Supplier_Name): ").strip()
      if field in ["Item_ID","Item_Name","Category", "Supplier_Name"]:
        obj.delete_inventory(field)
      else:
        print("Invalid choice!Enter choice from(Item_ID/Item_Name/Category/ Supplier_Name).")

    elif choice == "4":
      field=input("Update by(Item_ID/Item_Name/Category/Supplier_Name): ").strip()
      if field in ["Item_ID","Item_Name","Category", "Supplier_Name"]:
        obj.update_inventory(field)
      else:
        print("Invalid choice!Enter choice from(Item_ID/Item_Name/Category/ Supplier_Name).")

    elif choice == "5":
      obj. view_all_inventory_ID()

    elif choice == "6":
      obj.view_all_inventory_names()

    elif choice == "7":
      obj.view_all_inventory()
      
    elif choice == "8":
      break

    else:
      print("Invalid input!Enter right choice(1-8)")