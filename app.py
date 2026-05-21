from abc import ABC, abstractmethod

class MenuItem(ABC):
    def __init__(self, item_id, name, base_price, is_available=True):
        self._item_id = item_id
        self._name = name
        self._base_price = base_price
        self._is_available = is_available

    @property
    def base_price(self):
        return self._base_price

    @base_price.setter
    def base_price(self, value):
        if value < 0:
            print("[Error] Price cannot be negative!")
            return
        self._base_price = value

    @property
    def is_available(self):
        return self._is_available

    @is_available.setter
    def is_available(self, value):
        if not isinstance(value, bool):
            print("[Error] Availability must be True or False!")
            return
        self._is_available = value

    @abstractmethod
    def calculate_final_price(self):
        pass

    @abstractmethod
    def display_info(self):
        pass


class FoodItem(MenuItem):
    def __init__(self, item_id, name, base_price, allergy_warning="None"):
        super().__init__(item_id, name, base_price)
        self.allergy_warning = allergy_warning

    def calculate_final_price(self):
        service_fee = self.base_price * 0.15
        return self.base_price + service_fee

    def display_info(self):
        return f"[Food] ID: {self._item_id} | {self._name} - Price: {self.base_price} EGP (Warning: {self.allergy_warning})"


class BeverageItem(MenuItem):
    def __init__(self, item_id, name, base_price, size="Medium"):
        super().__init__(item_id, name, base_price)
        self.size = size

    def calculate_final_price(self):
        discounted_price = self.base_price * 0.50
        sugar_tax = 5.0
        return discounted_price + sugar_tax

    def display_info(self):
        return f"[Beverage] ID: {self._item_id} | {self._name} ({self.size}) - Price: {self.base_price} EGP"


class CustomerOrder:
    def __init__(self):
        self.items_list = []

    def add_item(self, menu_item):
        if menu_item.is_available:
            self.items_list.append(menu_item)
            print(f"Added {menu_item._name} to your order.")
        else:
            print("Sorry, this item is currently unavailable!")

    def view_order(self):
        if not self.items_list:
            print("Your order is empty.")
            return
        
        print("\n--- Current Order Items ---")
        for item in self.items_list:
            print(f"- {item._name}: Base Price = {item.base_price} EGP")

    def print_receipt(self):
        if not self.items_list:
            print("No items in order to print a receipt.")
            return
        
        print("\n====================================")
        print("        SMART RESTAURANT POS        ")
        print("====================================")
        
        total_base = 0
        total_final = 0
        
        for item in self.items_list:
            base = item.base_price
            final = item.calculate_final_price()
            total_base += base
            total_final += final
            print(f"{item._name:<18} Base: {base:>5} | Final: {final:>5.2f} EGP")
            
        print("------------------------------------")
        print(f"Total Base Price:  {total_base:.2f} EGP")
        print(f"FINAL TOTAL (Taxes/Discounts): {total_final:.2f} EGP")
        print("====================================\n")


def main():
    menu = {
        "1": FoodItem("1", "Beef Burger", 120.0, "Contains Gluten"),
        "2": FoodItem("2", "Chicken Pizza", 160.0, "None"),
        "3": BeverageItem("3", "Iced Latte", 60.0, "Large"),
        "4": BeverageItem("4", "Orange Juice", 40.0, "Medium")
    }
    
    current_order = CustomerOrder()
    
    while True:
        print("\n--- Cashier System Dashboard ---")
        print("[1] View Restaurant Menu")
        print("[2] Add Item to Customer Order")
        print("[3] View Current Order Status")
        print("[4] Print Final Receipt & Pay")
        print("[5] Exit System Gracefully")
        
        choice = input("Please select an option (1-5): ").strip()
        
        if choice == "1":
            print("\n--- Restaurant Menu ---")
            for item in menu.values():
                print(item.display_info())
                
        elif choice == "2":
            item_id = input("Enter Item ID to add: ").strip()
            if item_id in menu:
                current_order.add_item(menu[item_id])
            else:
                print("[Error] Invalid Item ID! Please check the menu first.")
                
        elif choice == "3":
            current_order.view_order()
            
        elif choice == "4":
            current_order.print_receipt()
            current_order = CustomerOrder() 
            
        elif choice == "5":
            print("Exiting system... Thank you!")
            break
        else:
            print("[Warning] Invalid choice! Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()