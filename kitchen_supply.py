# Gaspar Tonnesen | CIS 345 T/Th 12:00 PM | Final Project | Due 04.29.19
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////// KITCHEN SUPPLY ///////////////////////////////////////////////////////////////////////////////
# /////////PRODUCT ORDERING & INVENTORY MANAGEMENT SYSTEM /////////////////////////////////////////////////////////
# //////// IMPORTS: ///////////////////////////////////////////////////////////////////////////////////////////////////
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from product_classes import Product, Attachment
from customer import Customer, Employee
from PIL import Image, ImageFilter, ImageTk
import csv
import json
import time  # time.ctime() returns current time
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////// GLOBALS ///////////////////////////////////////////////////////////////////////////
box_color = 'snow'
white_text = 'white'
list_box_color = box_color
edit_zone_bg = box_color
bttn_bg_color = 'lawn green'
gui_bg_color = 'gray20'
disabled_bg = 'gray60'
lbl_bg_color = gui_bg_color
empty_lbl_color = gui_bg_color
bg_black = 'black'
gold_bg_color = 'gold'
img_filename = 'k_supply_logo.jpg'
graphic_filename = 'kitchen_graphic.jpg'
header_text = ""
# acc_detail_text = 'Welcome to Kitchen Supply. Select your account to place an order'
acc_detail_text = ''

acc_lbl_text = 'Select an account:'
dbl_click_text = '(click for product detail)'
list_lbl_text = 'shopping cart/listbox:'
prod_detail_txt = 'product detail label displays info of the product that was double clicked'
emp_zone_txt = 'add new product section, only visible in edit mode'
header_width = 70  # 76                                                # /////////////////////////////////////
col_0_width = 27                                                        # ///////// WIDTH /////////////////
col_1_width = 30                                                       # /////////////////////////////////////
col_2_width = 10
prod_detail_width = col_0_width + col_1_width + col_2_width + 3
list_bx_width = 25
font = ('Helvetica', 10)
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////
window = Tk()
window.geometry('700x560')
window.title('Kitchen Supply Order Management System')
window.iconbitmap('ks_icon.ico')
window.config(bg=gui_bg_color)
window.resizable(0, 0)


# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////// FUNCTIONS /////////////////////////////////////////////////////////////////////////////////


def open_edit_mode():
    """sets GUI to edit mode"""
    global img_lbl, edit_mode, account_logged_in
    if isinstance(account_logged_in, Employee):
        edit_mode = True
        dbl_click_lbl.config(text='(double click to edit product)')
        header_lbl.config(text='Add a new product in the bottom section,\n'
                               'or edit products by selecting them from the drop down.')
        n = 2
        img_lbl.grid_forget()
        prod_desc_lbl.grid(row=9, column=0, sticky=W, padx=11, pady=n)
        prod_desc_entry.grid(row=9, column=1, pady=n)
        add_prod_id_lbl.grid(row=10, column=0, sticky=W, padx=11, pady=n)
        add_prod_id_entry.grid(row=10, column=1, pady=n)
        add_prod_qty_lbl.grid(row=11, column=0, sticky=W, padx=11, pady=n)
        add_prod_qty_entry.grid(row=11, column=1, pady=n)
        add_prod_price_lbl.grid(row=12, column=0, sticky=W, padx=11, pady=n)
        add_prod_price_entry.grid(row=12, column=1, pady=n)
        prod_type_frame.grid(row=9, column=2, rowspan=4, pady=n)
        att_id_lbl.grid(row=13, column=0, sticky=W, padx=11, pady=n)
        att_id_entry.grid(row=13, column=1, pady=n)
        prod_mat_lbl.grid(row=14, column=0, sticky=W, padx=11, pady=n)
        prod_mat_entry.grid(row=14, column=1, pady=n)
        add_new_prod_butt.grid(row=13, column=2, rowspan=2)
    else:
        messagebox.showinfo('Access Denied', 'You need to be logged in as an employee to access edit mode.')


def close_edit_mode():
    """"""
    global img_lbl, edit_mode
    edit_mode = False
    dbl_click_lbl.config(text=dbl_click_text)
    prod_desc_lbl.grid_forget()
    prod_desc_entry.grid_forget()
    add_prod_id_lbl.grid_forget()
    add_prod_id_entry.grid_forget()
    add_prod_qty_lbl.grid_forget()
    add_prod_qty_entry.grid_forget()
    add_prod_price_lbl.grid_forget()
    add_prod_price_entry.grid_forget()
    prod_type_frame.grid_forget()
    att_id_lbl.grid_forget()
    att_id_entry.grid_forget()
    prod_mat_lbl.grid_forget()
    prod_mat_entry.grid_forget()
    add_new_prod_butt.grid_forget()
    img_lbl.grid(row=9, column=0, columnspan=3, rowspan=6)


def exit_program():
    """ends program and closes GUI"""
    print('Quit program - function linked to file-quit..')
    save_data()
    window.destroy()


def save_products():
    """saves product/attachments in json files"""
    reg_prod = []
    attach_prod = []
    for p in regular_products:
        tmp_prod = [p.id, p.description, p.q_on_hand, p.price]
        reg_prod.append(tmp_prod)
    with open('products.json', 'w') as json_file:
        json.dump(reg_prod, json_file)
    for a in attachments:
        tmp_attachment = [a.attach_id, a.material, a.id, a.description, a.q_on_hand, a.price]
        attach_prod.append(tmp_attachment)
    with open('attach_products.json', 'w') as json_file:
        json.dump(attach_prod, json_file)


def save_data():
    """saves all product and customer data"""
    log_transactions(transactions)
    save_products()
    # with open('customers.csv', 'w', newline='') as file:
    #     writer = csv.writer(file)
    #     for c in customers:
    #         writer.writerow(c)
    # with open('employees.csv', 'w', newline='') as file:
    #     writer = csv.writer(file)
    #     for e in employees:
    #         writer.writerow(e)


def add_to_cart():
    """Add product, quantity and price to the order list/listbox. Update labels."""
    global product_index, product_objects, list_box, quantity_selected, order_total, total_lbl, line_item_prices, \
        account_logged_in, account_objects, account_index, line_item_qty, orders
    price = product_objects[product_index.get()].price * int(quantity_selected.get())
    if price > float(account_logged_in.balance):
        messagebox.showinfo('Insufficient Funds', "Item can't be added to order.\nYour balance is too low.")
    elif product_objects[product_index.get()].q_on_hand < int(quantity_selected.get()):
        messagebox.showinfo('Out of Stock', f"We only have {product_objects[product_index.get()].q_on_hand} "
                f"of this product in stock. Please enter a different quantity.")
    else:
        order = f'({quantity_selected.get()}) {product_objects[product_index.get()].description} ${price}'
        orders.append(order)
        list_box.insert(END, order)
        order_total.set(order_total.get() + price)
        line_item_prices.append(price)
        line_item_qty.append(quantity_selected.get())
        total_lbl.config(text=f'Order Total: \t           ${order_total.get(): .2f} ')
        account_logged_in.balance = float(account_logged_in.balance) - price
        # product_objects[product_index].q_on_hand = product_objects[product_index].q_on_hand-quantity_selected.get()
        p = product_objects[product_index.get()]
        p.q_on_hand = p.q_on_hand - int(quantity_selected.get())
        prod_detail_lbl.config(text=f'Product: {p.description}\nPrice Each: ${p.price: .2f}\nQuantity on Hand: {p.q_on_hand}\nProduct ID: {p.id}')
        acc_login()


def activate_add_bttn(event):
    """"""
    global add_button
    add_button['state'] = NORMAL


def submit_list():
    """processes data in list_box after user press button"""
    global account_logged_in, order_total, transactions
    transactions.append([time.ctime(), account_logged_in.name, str(order_total.get())])
    list_box.delete(0, END)
    order_total.set(0)
    total_lbl.config(text=f'Order Total: \t           ${order_total.get(): .2f} ')
    prod_detail_lbl.config(text='Thank you for placing an order!')


def log_transactions(transactions):
    # writes all transactions within the given parameter into a csv file
    with open('order_log.csv', 'w', newline='') as fp:
        writer = csv.writer(fp)
        for t in transactions:
            writer.writerow(t)


def remove_product():
    """removes product from list box and adjusts the order total"""
    global list_box, total_lbl, order_total, line_item_prices, remove_bttn, product_index, product_objects, orders
    # print(list_box.size())
    # print(list_box.curselection()[0])
    if list_box.size() >= 1:
        remove_index = list_box.curselection()[0]
        list_box.delete(remove_index)
        p = line_item_prices[remove_index]
        line_item_prices.pop(remove_index)
        q = line_item_qty[remove_index]
        line_item_qty.pop(remove_index)
        orders.pop(remove_index)
        prod_selected = product_objects[product_index.get()]
        prod_selected.q_on_hand += int(q)
        prod_detail_lbl.config(text=f'Product: {prod_selected.description}\nPrice Each: ${prod_selected.price: .2f}'
                            f'\nQuantity on Hand: {prod_selected.q_on_hand}\nProduct ID: {prod_selected.id}')
        order_total.set(order_total.get() - p)
        account_logged_in.balance += p
        total_lbl.config(text=f'Order Total: \t           ${order_total.get(): .2f} ')
        acc_login()
    remove_bttn['state'] = DISABLED


def activate_remove_bttn(event):
    """"""
    global remove_bttn
    remove_bttn['state'] = NORMAL


def activate_att():
    """"""
    global prod_mat_entry, att_id_entry
    prod_mat_entry['state'] = NORMAL
    att_id_entry['state'] = NORMAL


def disable_att():
    """"""
    global prod_mat_entry, att_id_entry
    prod_mat_entry['state'] = DISABLED
    att_id_entry['state'] = DISABLED


def add_new_prod():
    """"""
    global product_objects, product_names, edit_index, edit_product_mode, new_prod_id, new_prod_desc, new_prod_qty, new_prod_price
    if edit_product_mode:
        p = Product(new_prod_id.get(), new_prod_desc.get(), new_prod_qty.get(), new_prod_price.get())
        product_objects[edit_index.get()] = p
        product_names[edit_index.get()] = p.description
        clear_edit_widgets()
    else:
        create_new_product()


def clear_edit_widgets():
    global new_prod_id, new_prod_desc, new_prod_qty, new_prod_price
    new_prod_id.set('')
    new_prod_desc.set('')
    new_prod_qty.set('')
    new_prod_price.set('')


def create_new_product():
    """"""
    print('add new product')


def update_header():
    global account_name, header_lbl, account_logged_in
    header_lbl.config(text=f'Welcome to Kitchen Supply!\nChoose products below')


def verify_pin(event):
    """"""
    global account_logged_in, pin_entered
    pin_dialog = Toplevel(window)
    pin_lbl = Label(pin_dialog, text='Enter 4 Digit Pin').pack()
    pin_entry = Entry(pin_dialog, textvariable=pin_entered).pack(padx=5)
    pin_entry_bttn = Button(pin_dialog, text='Enter', command=lambda: record_pin(pin_dialog)).pack(pady=5)


def record_pin(pin_dialog):
    global account_logged_in, pin_entered, is_pin_correct
    index = 0
    for a in account_objects:
        if a.name == account_name.get():
            account_index.set(index)
            account_logged_in = account_objects[index]
            break
        else:
            index += 1
    print(f'pin entered on bttn click: {pin_entered.get()}\naccount logged in pin: {account_logged_in.pin}')
    if pin_entered.get() == account_logged_in.pin:
        is_pin_correct = True
        acc_login()
    else:
        is_pin_correct = False
        acc_detail_lbl.config(text='Incorrect Pin')
        header_lbl.config(text='')
    pin_dialog.destroy()


def acc_login():
    global account_objects, account_name, acc_detail_lbl, account_logged_in, account_index, prod_drop_down
    acc_detail = f'You are logged in as {account_logged_in.name}\nYour balance is: $' \
                f'{float(account_logged_in.balance): .2f}\nID: {account_logged_in.acc_num}'
    acc_detail_lbl.configure(text=acc_detail)
    update_header()
    prod_drop_down['state'] = NORMAL
    prod_qty_entry['state'] = NORMAL


def show_prod_detail(event):
    """"""
    global prod_detail_lbl, product_objects, product_index, product_name, is_pin_correct
    index = 0

    for p in product_objects:
        if p.description == product_name.get():
            product_index.set(index)
            p = product_objects[index]
            prod_detail_lbl.config(
                text=f'Product: {p.description}\nPrice Each: ${float(p.price): .2f}\nQuantity on Hand: {p.q_on_hand}'
                f'\nProduct ID: {p.id}')
            break
        else:
            index += 1


def get_product_list():
    """gets sample products from json file"""
    global product_names, product_objects
    with open('products.json', 'r') as json_file:
        sp = json.load(json_file)  # load sample products (sp)
        for p in sp:
            tmp_product = Product(p[0], p[1], p[2], p[3])
            product_objects.append(tmp_product)
            product_names.append(tmp_product.description)
            regular_products.append(tmp_product)
    with open('attach_products.json', 'r') as json_file:
        sp = json.load(json_file)  # load sample products (sp)
        for p in sp:
            tmp_product = Attachment(p[0], p[1], p[2], p[3], p[4], p[5])
            product_objects.append(tmp_product)
            product_names.append(tmp_product.description)
            attachments.append(tmp_product)


def get_account_list():
    """gets customer/employees list from csv file"""
    global account_names, account_objects
    with open('customers.csv', 'r') as read_file:
        reader = csv.reader(read_file)
        for line in reader:
            id = line[0]
            name = line[1]
            pin = line[2]
            balance = line[3]
            tmp_customer = Customer(id, name, pin, balance)
            account_objects.append(tmp_customer)
            account_names.append(tmp_customer.name)
            customers.append(tmp_customer)
    with open('employees.csv', 'r') as read_file:
        reader = csv.reader(read_file)
        for line in reader:
            id = line[0]
            name = line[1]
            pin = line[2]
            balance = line[3]
            emp_id = line[4]
            tmp_employee = Employee(emp_id, id, name, pin, balance)
            account_objects.append(tmp_employee)
            account_names.append(tmp_employee.name)
            employees.append(tmp_employee)


def add_8_seperators():
    menu_bar.add_separator()
    menu_bar.add_separator()
    menu_bar.add_separator()
    menu_bar.add_separator()
    menu_bar.add_separator()
    menu_bar.add_separator()
    menu_bar.add_separator()
    menu_bar.add_separator()


def product_selected(event):
    global edit_mode, product_name, new_prod_desc, new_prod_id, edit_index, edit_product_mode
    index = 0
    for p in product_objects:
        if p.description == product_name.get():
            product_index.set(index)
            p = product_objects[index]
            edit_index.set(index)
            break
        else:
            index += 1
    if edit_mode:
        prod_detail_lbl.config(text=f'Edit {product_name.get()} below.\nClick Add Product Button to save changes')
        new_prod_desc.set(product_name.get())
        new_prod_id.set(p.id)
        new_prod_qty.set(p.q_on_hand)
        new_prod_price.set(p.price)
        edit_product_mode = True
    else:
        show_prod_detail(1)
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////// //////////////////////////////////////////////////////////////////////////////////////


attachments = []
regular_products = []
customers = []
employees = []
account_objects = []
account_names = []
product_names = []
product_objects = []
get_product_list()
get_account_list()
account_logged_in = Customer()
pin_entered = StringVar()
is_pin_correct = BooleanVar()
is_pin_correct.set(False)
product_index = IntVar()
account_index = IntVar()
line_item_prices = []  # list to contain prices of each line item in list box to adjust total when item is removed
line_item_qty = []  # list to contain quantities of each line item in list box to adjust q_on_hand when item is removed
account_name = StringVar()
product_name = StringVar()
product = StringVar()
active_acc = StringVar()
new_prod_id = StringVar()
new_prod_desc = StringVar()
new_prod_qty = StringVar()
new_prod_price = StringVar()
new_prod_material = StringVar()
attachment_id = StringVar()
order_total = DoubleVar()
order_total.set(0.0)
quantity_selected = StringVar()
quantity_selected.set('1')
edit_index = IntVar()
edit_mode = False
edit_product_mode = False  # specifies whether user is editing a product or adding a new one
# list of line items in the order/list box. This will be the data for order log
orders = []
transactions = [['DateTime', 'Name', 'Total']]
window.grid_columnconfigure(0, minsize=col_0_width)

# menu bar
menu_bar = Menu(window)
window.config(menu=menu_bar)
menu_bar.add_separator()
menu_bar.add_command(label='Turn Edit Mode On', command=open_edit_mode)
add_8_seperators()
menu_bar.add_command(label='Turn Off Edit Mode', command=close_edit_mode)
add_8_seperators()
menu_bar.add_command(label='Save Data', command=save_data)
add_8_seperators()
menu_bar.add_command(label='Quit', command=exit_program)

# manipulate image of KS logo and place it in a label
img = Image.open(img_filename)
# new_img = img.resize((148, 175))
new_img = img.resize((148, 175))

# end_img = new_img.filter(ImageFilter.SMOOTH)
logo = ImageTk.PhotoImage(new_img)
logo_lbl = Label(window, image=logo, width=148)
logo_lbl.grid(row=0, column=3, rowspan=5, columnspan=3)
# image to cover edit mode area:
k_graphic = Image.open(graphic_filename)
ks_graphic = k_graphic.resize((450, 120))
graphic = ImageTk.PhotoImage(ks_graphic)
# select account drop down combobox
acc_drop_down = ttk.Combobox(window, values=account_names, textvariable=account_name, width=col_0_width - 3)
acc_drop_down.grid(row=0, column=1, sticky=W, padx=2)
acc_drop_down.bind("<<ComboboxSelected>>", verify_pin)
acc_lbl = Label(window, text=acc_lbl_text, bg=gui_bg_color, fg=white_text, font=font)
acc_lbl.grid(row=0, column=0, sticky=E)
# account detail section
acc_detail_lbl = Label(window, text=acc_detail_text, width=header_width, bg=gui_bg_color, fg=white_text,
                       font='Helvetica 9 bold')
acc_detail_lbl.grid(row=1, rowspan=2, column=0, columnspan=3, sticky=W)

# header/message to user
header_lbl = Label(window, text=header_text, width=header_width, bg=gui_bg_color, fg=white_text,
                   font='Helvetica 9 bold')
header_lbl.grid(row=3, column=0, rowspan=2, columnspan=3, sticky=N)
# placeholder
empty_lbl_3 = Label(window, bg=empty_lbl_color, width=col_0_width)
empty_lbl_3.grid(row=5, column=0)
# advice/instructions for user
dbl_click_lbl = Label(window, text=dbl_click_text, bg=gui_bg_color, fg=white_text, width=col_1_width - 5)
dbl_click_lbl.grid(row=5, column=1, sticky=SW)
# select product drop down combobox
prod_lbl = Label(window, text='Select Product Here:', bg=lbl_bg_color, fg=white_text, font=font)
prod_lbl.grid(row=6, column=0, sticky=E, padx=1)
prod_drop_down = ttk.Combobox(window, values=product_names, textvariable=product_name, width=col_1_width - 3,
                              justify=CENTER, state=DISABLED)

prod_drop_down.grid(row=6, column=1, sticky=W)
prod_drop_down.bind('<<ComboboxSelected>>', product_selected)
prod_drop_down.bind('<Button-1>', activate_add_bttn)

# product quantity entry
prod_qty_lbl = Label(window, text='Enter Quantity Here:', bg=lbl_bg_color, fg=white_text, font=font)
prod_qty_lbl.grid(row=7, column=0, sticky=E)
prod_qty_entry = Entry(window, width=col_1_width, textvariable=quantity_selected, justify=CENTER, state=DISABLED,
                       disabledbackground=disabled_bg)
prod_qty_entry.grid(row=7, column=1, sticky=W, padx=1)
# product detail section
prod_detail_lbl = Label(window, bg=gui_bg_color, width=prod_detail_width - 20, height=6, fg=white_text, justify=LEFT,
                        font=('Helvetica', 11, 'bold'))
prod_detail_lbl.grid(row=8, column=0, columnspan=3, pady=1, padx=20)
# //////////*********************************************************************************8
# description for new product section
prod_desc_lbl = Label(window, bg=gui_bg_color, fg=white_text, text='Description:', width=col_0_width - 15, font=font,
                      anchor=W)
# prod_desc_lbl.grid(row=9, column=0, sticky=W, padx=11)
prod_desc_entry = Entry(window, textvariable=new_prod_desc, width=col_1_width)
# prod_desc_entry.grid(row=9, column=1)
# new prod id entry
add_prod_id_lbl = Label(window, text='ID:', width=col_0_width - 20, bg=gui_bg_color, fg=white_text, font=font, anchor=W)
# add_prod_id_lbl.grid(row=10, column=0, sticky=W, padx=11)
add_prod_id_entry = Entry(window, textvariable=new_prod_id, width=col_1_width)
# add_prod_id_entry.grid(row=10, column=1)
# new product quantity
add_prod_qty_lbl = Label(window, text='Quantity:', width=col_0_width - 15, bg=gui_bg_color, fg=white_text, font=font,
                         anchor=W)
# add_prod_qty_lbl.grid(row=11, column=0, padx=11, sticky=W)
add_prod_qty_entry = Entry(window, width=col_1_width, textvariable=new_prod_qty)
# add_prod_qty_entry.grid(row=11, column=1)
# new product price
add_prod_price_lbl = Label(window, text='Price:', width=col_0_width - 15, bg=gui_bg_color, fg=white_text, font=font,
                           anchor=W)
# add_prod_price_lbl.grid(row=12, column=0, padx=11, sticky=W)
add_prod_price_entry = Entry(window, width=col_1_width, textvariable=new_prod_price)
# add_prod_price_entry.grid(row=12, column=1)
# frame containing radio buttons to select product type, attachment or regular
prod_type_frame = Frame(window, width=col_2_width, bg='yellow')
# prod_type_frame.grid(row=9, rowspan=4, column=2)
att_radio_bttn = Radiobutton(prod_type_frame, text='Attachment', value='A', command=activate_att)  # variable=prod_type?
att_radio_bttn.pack()
reg_radio_bttn = Radiobutton(prod_type_frame, text='Regular', value='R', command=disable_att)  # variable=prod_type?
reg_radio_bttn.pack(fill=X)
# attachment product id
att_id_lbl = Label(window, text='ID of attachment:', width=col_0_width - 10, bg=gui_bg_color, fg=white_text, font=font,
                   anchor=W)
# att_id_lbl.grid(row=13, column=0, padx=11, sticky=W)
att_id_entry = Entry(window, width=col_1_width, textvariable=attachment_id, state=DISABLED, disabledbackground='gray60')
# att_id_entry.grid(row=13, column=1)
# product material
prod_mat_lbl = Label(window, text='Material:', width=col_0_width - 15, bg=gui_bg_color, fg=white_text, font=font,
                     anchor=W)
prod_mat_entry = Entry(window, textvariable=new_prod_material, width=col_1_width, state=DISABLED,
                       disabledbackground='gray60')
# add new product button
add_new_prod_butt = Button(window, width=col_2_width, height=2, bg=bttn_bg_color, text='ADD\nPRODUCT',
                           command=add_new_prod)

# image covering edit zone when edit mode is off
img_lbl = Label(window, image=graphic, width=494, height=150, bg='white')
img_lbl.grid(row=9, rowspan=6, column=0, columnspan=3)
# add to listbox button
add_button = Button(window, width=col_2_width, text='>>', bg=bttn_bg_color, command=add_to_cart, relief=RAISED,
                    state=DISABLED)
add_button.grid(row=6, column=2, sticky=W, pady=2)
# remove from listbox button
remove_bttn = Button(window, width=col_2_width, text='<<', bg='red', command=remove_product, relief=RAISED,
                     state=DISABLED)
remove_bttn.grid(row=7, column=2, sticky=W)
# list box
list_lbl = Label(window, text=list_lbl_text, width=list_bx_width, bg=lbl_bg_color, fg=white_text)
list_lbl.grid(row=5, column=3, columnspan=3)
list_box = Listbox(window, width=list_bx_width, relief=SUNKEN, bg=list_box_color, height=15)
list_box.grid(row=6, column=3, columnspan=3, rowspan=6, ipadx=10, padx=5, sticky=NW)
list_box.bind('<Button-1>', activate_remove_bttn)

total_lbl = Label(window, width=list_bx_width, text=f'Order Total:\t\t${order_total.get(): .2f} ', bg=gui_bg_color,
                  fg=white_text)
total_lbl.grid(row=12, column=3, columnspan=3)

order_bttn = Button(window, text='PLACE ORDER', width=list_bx_width, height=2, bg=bttn_bg_color, command=submit_list)
order_bttn.grid(row=13, rowspan=2, column=3, columnspan=3, sticky=S, padx=5)
# close edit mode to start
# low_bar = Label(window, bg='sky blue', width=header_width-10, text='nee').grid(row=15, column=0, columnspan=2)

close_edit_mode()

print(window.grid_size())
window.mainloop()
