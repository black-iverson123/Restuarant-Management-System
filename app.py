import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import time
from hashlib import md5
import secrets
import datetime



class rmsLogin:
    """_summary_ This class is defined to handle employee login,
        it makes use of the md5 package from hashlib to hash passwords to secure in database,
        if sql query returns none when login attempt is made messagebox displays an error message but shows success if 
        user is found then open the dash app
        registration functionality is active in case new employees need to be registered.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Splash Restaurant")
        self.username = tk.StringVar()
        self.password = tk.StringVar()

        self.create_gui()
        #connecting to database
        self.conn = sqlite3.connect("splash.db")
        self.cursor = self.conn.cursor()

    def login(self):
        # Fetch user login details from database and password hashing
        username = self.username.get()
        password = self.password.get()
        
        hashed_password = md5(password.encode()).hexdigest()

        self.cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
        row = self.cursor.fetchone()

        if row is None:
            messagebox.showerror("Error", "User does not exist or invalid credentials")
        else:
            messagebox.showinfo("Success", f"Welcome {username}")
            time.sleep(2)  # time is applied to imporove visual feedback
            self.dashboard()
            
            
    def dashboard(self):
        dashboard_window = tk.Toplevel(self.root)
        RMS(dashboard_window)

    def signUP(self):
        # Open the SignUp window
        signup_window = tk.Toplevel(self.root)
        rmsSignUP(signup_window)

    def create_gui(self):
        """_summary_ Here tikinter frame packages are used to collect user data, style gui
        """
        login_frame = tk.LabelFrame(self.root, text="Login Details", bg="beige", relief=tk.SUNKEN)
        login_frame.pack(fill="x", padx=20, pady=100)

        name_label = tk.Label(login_frame, text="Username")
        name_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        name_entry = tk.Entry(login_frame, textvariable=self.username)
        name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        password_label = tk.Label(login_frame, text="Password")
        password_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        password_entry = tk.Entry(login_frame, textvariable=self.password, show="*")
        password_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(fill="x", padx=10, pady=10)

        login_btn = tk.Button(btn_frame, text="Login", command=self.login, relief=tk.RIDGE, bg="green", fg="white")
        login_btn.pack(padx=5)

        register_btn = tk.Button(btn_frame, text="Register", command=self.signUP, relief=tk.RIDGE, bg="green", fg="white")
        register_btn.pack(padx=5)

class rmsSignUP:
    """_summary_This class handles the employee registration, employs te use of md5 to hash pasword,
        runs a sql query to create a user table if not exist then inserts the data into created table
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Register - Splash Restaurant")
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.email = tk.StringVar()
        self.address = tk.StringVar()

        self.conn = sqlite3.connect("splash.db")
        self.cursor = self.conn.cursor()

        self.create_table()
        self.create_gui()

    def create_table(self):
        # table is created if non existing
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR NOT NULL,
            password VARCHAR NOT NULL,
            email VARCHAR NOT NULL,
            address VARCHAR NOT NULL
        )''')

    def signUP(self):
        # Adding a new emloyee to the database
        username = self.username.get()
        password = self.password.get()
        email = self.email.get()
        address = self.address.get()
        hashed_password = md5(password.encode()).hexdigest()

        self.cursor.execute("INSERT INTO users (username, password, email, address) VALUES (?, ?, ?, ?)", 
                            (username, hashed_password, email, address))
        self.conn.commit()
        messagebox.showinfo("Success", f"User {username} registered successfully")

    def create_gui(self):
        #same as mentioned before
        register_frame = tk.LabelFrame(self.root, text="Registration Details", bg="beige", relief=tk.SUNKEN)
        register_frame.pack(fill="x", padx=20, pady=100)

        name_label = tk.Label(register_frame, text="Username")
        name_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        name_entry = tk.Entry(register_frame, textvariable=self.username)
        name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        password_label = tk.Label(register_frame, text="Password")
        password_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        password_entry = tk.Entry(register_frame, textvariable=self.password, show="*")
        password_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        email_label = tk.Label(register_frame, text="Email Address")
        email_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        email_entry = tk.Entry(register_frame, textvariable=self.email)
        email_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        address_label = tk.Label(register_frame, text="Contact Address")
        address_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        address_entry = tk.Entry(register_frame, textvariable=self.address)
        address_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(fill="x", padx=10, pady=10)

        register_btn = tk.Button(btn_frame, text="Register", command=self.signUP, relief=tk.RIDGE, bg="green", fg="white")
        register_btn.pack(padx=5)



class RMS:
    """_summary_Class RMS is the main application wher most user interactions occur
        functions with predefined sql query to create spsecifi tables when app is just being launched
        this class serves as the main station of the restuarant from billing to orders
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Splash Dashboard")
        
        self.customer_name = tk.StringVar()
        self.customer_contact = tk.StringVar()
        self.customer_email = tk.StringVar()
        self.customer_address = tk.StringVar()
        
        self.orders = {}
        self.gst_percentage = 10
        
        # Connect to SQLite database (splash.db) and create table if not exists
        self.conn = sqlite3.connect('splash.db')
        self.cursor = self.conn.cursor()
        self.create_table()

        self.items = {}  # Menu items will be fetched from the database

        self.create_gui()

    def create_table(self):
        # Create a table for storing menu items if it doesn't exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS menu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            price REAL NOT NULL
        )''')
        
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            email VARCHAR NOT NULL,
            address VARCHAR NOT NULL,
            transaction_id VARCHAR NOT NULL,
            price REAL NOT NULL,
            date DATE  NOT NULL
        )''')
        
        
        self.conn.commit()

    def fetch_menu_from_db(self):
        # Fetch menu items from the database
        self.cursor.execute("SELECT item_name, price FROM menu")
        rows = self.cursor.fetchall()
        self.items = {row[0]: row[1] for row in rows}

    def add_item_to_db(self, item, price):
        # Add a new item to the database
        self.cursor.execute("INSERT INTO menu (item_name, price) VALUES (?, ?)", (item, price))
        self.conn.commit()
    
    def transaction_id(self):
        # generates random numbers to serve as transaction id
        transaction_id = secrets.randbelow(10**10)
        return transaction_id
    

    def create_gui(self):
        """_summary_This function creates the reatuarant dashboard that serves the app
        """
        #customer details section
        details_frame = tk.LabelFrame(self.root, text="Customer Details", bg="beige", relief=tk.SUNKEN)
        details_frame.pack(fill="x", padx=10, pady=10)
        
        name_label = tk.Label(details_frame, text="Name")
        name_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        name_entry = tk.Entry(details_frame, textvariable=self.customer_name)
        name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        contact_label = tk.Label(details_frame, text="Phone Number")
        contact_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        contact_entry = tk.Entry(details_frame, textvariable=self.customer_contact)
        contact_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        contact_entry.configure(validate='key')
        contact_entry.configure(validatecommand=(contact_entry.register(self.validate_contact), "%P"))
        
        email_label = tk.Label(details_frame, text="Email Address")
        email_label.grid(row=0, column=2, padx=5, pady=5, sticky="e")
        email_entry = tk.Entry(details_frame, textvariable=self.customer_email)
        email_entry.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        
        address_label = tk.Label(details_frame, text="House Address")
        address_label.grid(row=1, column=2, padx=5, pady=5, sticky="e")
        address_entry = tk.Entry(details_frame, textvariable=self.customer_address)
        address_entry.grid(row=1, column=3, padx=5, pady=5, sticky="w")
        
        # Menu input section
        menu_input_frame = tk.LabelFrame(self.root, text="Add Menu Item", bg="lavender", relief=tk.SUNKEN)
        menu_input_frame.pack(fill="x", padx=10, pady=10)

        item_label = tk.Label(menu_input_frame, text="Item Name")
        item_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.item_name_entry = tk.Entry(menu_input_frame)
        self.item_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        price_label = tk.Label(menu_input_frame, text="Price")
        price_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.price_entry = tk.Entry(menu_input_frame)
        self.price_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        add_item_button = tk.Button(menu_input_frame, text="Add Item", command=self.add_menu_item)
        add_item_button.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Display the existing menu from the database
        self.fetch_menu_from_db()

        menu_frame = tk.LabelFrame(self.root, text="Menu", bg="grey", relief=tk.SUNKEN)
        menu_frame.pack(fill="both", expand=True)

        item_header = tk.Label(menu_frame, text="Items")
        item_header.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        qty_header = tk.Label(menu_frame, text="Quantity")
        qty_header.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        row = 1
        
        for item, price in self.items.items():
            item_var = tk.IntVar()
            item_label = tk.Label(menu_frame, text=f"{item} - {self.convert_to_inr(price)}")
            item_label.grid(row=row, column=0, padx=5, pady=5, sticky="w")
            
            qty_entry = tk.Entry(menu_frame, width=5)
            qty_entry.grid(row=row, column=1, padx=5, pady=5, sticky="w")
            
            self.orders[item] = {"var": item_var, "quantity": qty_entry }
            
            row += 1
        
        #action buttons section
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        bill_btn = tk.Button(btn_frame, text="Display Bill", command=self.show_bill, relief=tk.RIDGE, bg="green", fg="white")
        bill_btn.pack(side="left", padx=5)
        
        past_record_button = tk.Button(btn_frame, text="Previous Sales", command=self.past_records, relief=tk.RIDGE, bg="green", fg="white")
        past_record_button.pack(side="left", padx=5)
        
        check_out_button = tk.Button(btn_frame, text="Check Out", command=self.check_out, relief=tk.RIDGE, bg="green", fg="white")
        check_out_button.pack(side="left", padx=5)
        
        btn_clear = tk.Button(btn_frame, text="Clear Selection", command=self.clear_selection, relief=tk.RIDGE, bg="green", fg="white")
        btn_clear.pack(side="left", padx=5)
        

    def add_menu_item(self):
        # Add a new item to the menu 
        item_name = self.item_name_entry.get().strip()
        try:
            price = float(self.price_entry.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Invalid price format!")
            return

        if item_name and price > 0:
            self.add_item_to_db(item_name, price)
            messagebox.showinfo("Success", f"Added {item_name} to the menu.")
            self.item_name_entry.delete(0, tk.END)
            self.price_entry.delete(0, tk.END)
            self.refresh_menu()  # Refresh the menu after adding
        else:
            messagebox.showwarning("Input Error", "Please provide valid item name and price.")

    def refresh_menu(self):
        # Refresh the menu display after adding an item
        for widget in self.root.winfo_children():
            widget.destroy()  # Clear the window
        self.create_gui()  # Recreate the GUI

    def show_bill(self):
        # Check if name of customer exists
        if not self.customer_name.get().strip():
            messagebox.showwarning("Warning", "No customer for this bill!!!")
            return
        
        selected_items = []
        total_price = 0
        
        for item, info in self.orders.items():
            qty = info["quantity"].get()
            if qty:
                selected_items.append((item, int(qty)))
                total_price += self.items[item] * int(qty)
        
        if not selected_items:
            messagebox.showwarning("Warning", "Select at least one item.")
            return
        
        gst_amount = (total_price * self.gst_percentage) / 100
        bill = f"Customer Name: {self.customer_name.get()}\n"
        bill += f"Customer Contact: {self.customer_contact.get()}\n\n"
        bill += "Selected Items:\n"
        for item, quantity in selected_items:
            bill += f"{item} x {quantity} - {self.convert_to_inr(self.items[item] * quantity)}\n"
        bill += f"\nTotal Price: {self.convert_to_inr(total_price)}\n"
        bill += f"GST ({self.gst_percentage}%): {self.convert_to_inr(gst_amount)}\n"
        bill += f"Grand Total: {self.convert_to_inr(total_price - gst_amount)}"

        messagebox.showinfo("Bill", bill)
        
        price = self.convert_to_inr(total_price - gst_amount)
        return price
        
    def past_records(self):
        #this function fetches record of past sales in database
        date = datetime.datetime.utcnow().date()
        self.cursor.execute("SELECT customer_name, transaction_id, price, date FROM SALES WHERE date != ?", (date,))
        rows = self.cursor.fetchall()

        if not rows:
            messagebox.showerror("INFO", "No previous records found.")
        else:
            # Create a new top-level window
            top = tk.Toplevel(self.root)
            top.title("Past Sales Records")
            
            # Set up the canvas and scrollbar
            canvas = tk.Canvas(top, width=400, height=300)
            scrollbar = ttk.Scrollbar(top, orient="vertical", command=canvas.yview)
            canvas.configure(yscrollcommand=scrollbar.set)

            # Create a frame within the canvas to hold the text
            frame = tk.Frame(canvas)
            canvas.create_window((0, 0), window=frame, anchor="nw")

            # Populate data into the frame
            for row in rows:
                data = f"Customer name: {row[0]} \n Transaction ID: {row[1]} \nAmount Paid: {row[2]} \nDate: {row[3]} \n\n"
                label = tk.Label(frame, text=data, anchor="w")
                label.pack(fill="x", padx=10, pady=2)

            # Update the canvas scroll region to include the frame
            frame.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))

            # Pack the widgets
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            # Bind mouse scroll to canvas scroll
            def _on_mousewheel(event):
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

            top.bind_all("<MouseWheel>", _on_mousewheel)
        
    def check_out(self):
        #Entry of successful payment added into database
        transaction_id = self.transaction_id()
        price = self.show_bill()
        self.cursor.execute("INSERT INTO sales (customer_name, email, address, transaction_id, price, date) VALUES (?,?,?,?,?,?)", (self.customer_name.get(), self.customer_email.get(), self.customer_address.get(), transaction_id, price, datetime.datetime.utcnow()))
        self.conn.commit()
        messagebox.showinfo("Success", "Thanks for dining with us!!!")
        
        
    def clear_selection(self):
        #Clearing of selections in menu section
        for item, info in self.orders.items():
            info["var"].set(0)
            info["quantity"].delete(0, tk.END)

   

    def validate_contact(self, value):
        #This confirms if enterd user contact is numeric
        return value.isdigit() or value == ""

    @staticmethod
    def convert_to_inr(amount):
        #handlles the conversion of int values to str and attaches monetary sign for better display
       return "$" + str(amount)
   
   

root = tk.Tk()
restaurant_system = rmsLogin(root)
root.mainloop()
