import tkinter as tk
from tkinter import ttk
import re  # Regular expression module
import backend

class BitcoinAddressTrackerApp:

    def __init__(self, root):
        """Initialize the Bitcoin Address Tracker App."""
        self.root = root
        self.root.title("Bitcoin Address Tracker")
        
        # Variables to store the entered Bitcoin address and validation result
        self.address_var = tk.StringVar()
        self.validation_var = tk.StringVar()
        
        # Create UI widgets
        self.create_widgets()

    def create_widgets(self):
        """Create UI widgets for the Bitcoin Address Tracker App."""
        
        # Label and Entry for entering Bitcoin address
        address_label = ttk.Label(self.root, text="Bitcoin Address:")
        address_label.pack()
        self.address_entry = ttk.Entry(self.root, textvariable=self.address_var)
        self.address_entry.pack()
        
        # Label to display validation result
        self.validation_label = ttk.Label(self.root, textvariable=self.validation_var)
        self.validation_label.pack()

        # Button to add Bitcoin address
        add_button = ttk.Button(self.root, text="Add Address", command=self.add_address)
        add_button.pack()
        
        # Button to remove Bitcoin address
        remove_button = ttk.Button(self.root, text="Remove Address", command=self.remove_address)
        remove_button.pack()
        
        # Button to synchronize transactions
        sync_button = ttk.Button(self.root, text="Synchronize Transactions", command=self.sync_transactions)
        sync_button.pack()
        
        # Listbox to display added Bitcoin addresses
        self.address_list = tk.Listbox(self.root, height=10, width=50)
        self.address_list.pack()
        
        # Treeview to display transactions info in table format
        self.transaction_tree = ttk.Treeview(self.root, columns=("Address", "Balance (BTC)", "Transactions"), show="headings", height=10)
        self.transaction_tree.heading("Address", text="Address")
        self.transaction_tree.heading("Balance (BTC)", text="Balance (BTC)")
        self.transaction_tree.heading("Transactions", text="Transactions")
        self.transaction_tree.pack()

    def add_address(self):
        """Add Bitcoin address to the backend and update the UI."""
        address = self.address_var.get()
        
        # Validate Bitcoin address
        if self.validate_address(address):
            backend.add_address(address)
            self.display_addresses()
            self.validation_var.set("Valid Bitcoin Address")
        else:
            self.validation_var.set("Invalid Bitcoin Address")

    def remove_address(self):
        """Remove Bitcoin address from the backend and update the UI."""
        address = self.address_var.get()
        backend.remove_address(address)
        self.display_addresses()

    def sync_transactions(self):
        """Synchronize transactions for added Bitcoin addresses and update the UI."""
        transactions_info = backend.sync_transactions()
        self.display_transactions(transactions_info)

    def display_addresses(self):
        """Display added Bitcoin addresses in the UI."""
        self.address_list.delete(0, tk.END)
        for address in backend.bitcoin_addresses:
            self.address_list.insert(tk.END, address)

    def display_transactions(self, transactions_info):
        """Display transactions info in the UI."""
        # Clear existing items in the Treeview
        for item in self.transaction_tree.get_children():
            self.transaction_tree.delete(item)
        
        # Insert new items in the Treeview
        for address, info in transactions_info.items():
            self.transaction_tree.insert("", tk.END, values=(address, info['balance'], info['transactions']))

    def validate_address(self, address):
        """Validate Bitcoin address using regular expression."""
        # Bitcoin address regex pattern
        pattern = r"^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$|^bc1[ac-hj-np-z02-9]{5,87}$"
        
        if re.match(pattern, address):
            return True
        else:
            return False

def main():
    """Main function to initialize and run the Bitcoin Address Tracker App."""
    root = tk.Tk()
    app = BitcoinAddressTrackerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

