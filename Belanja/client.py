import tkinter as tk
from tkinter import messagebox
from customtkinter import CTk, CTkLabel, CTkEntry, CTkButton
import shopping_pb2
import shopping_pb2_grpc
import grpc

class ShoppingClient:
    def __init__(self):
        self.channel = grpc.insecure_channel('localhost:50051')
        self.stub = shopping_pb2_grpc.ShoppingServiceStub(self.channel)

    def create_item(self, item_name, price):
        request = shopping_pb2.CreateItemRequest(item_name=item_name, price=price)
        response = self.stub.CreateItem(request)
        return response

    def read_item(self, item_id):
        request = shopping_pb2.ReadItemRequest(id=item_id)
        response = self.stub.ReadItem(request)
        return response

    def update_item(self, item_id, item_name, price):
        request = shopping_pb2.UpdateItemRequest(id=item_id, item_name=item_name, price=price)
        response = self.stub.UpdateItem(request)
        return response

    def delete_item(self, item_id):
        request = shopping_pb2.DeleteItemRequest(id=item_id)
        response = self.stub.DeleteItem(request)
        return response

def create_item_clicked():
    try:
        item_name = item_name_entry.get()
        price = float(price_entry.get())
        response = client.create_item(item_name, price)
        messagebox.showinfo("Info", response.message)
    except ValueError:
        messagebox.showerror("Error", "Price must be a valid number")

def read_item_clicked():
    try:
        item_id = int(item_id_entry.get())
        response = client.read_item(item_id)
        if response.item.id != 0:
            item_info = f"Item Name: {response.item.item_name}\nPrice: {response.item.price}"
            messagebox.showinfo("Item Information", item_info)
        else:
            clear_labels()
            messagebox.showinfo("Info", "Item not found")
    except ValueError:
        messagebox.showerror("Error", "Item ID must be an integer")

def clear_labels():
    item_name_display_label.configure(text="")
    price_display_label.configure(text="")

def update_item_clicked():
    try:
        item_id = int(item_id_entry.get())
        item_name = item_name_entry.get()
        price = float(price_entry.get())
        response = client.update_item(item_id, item_name, price)
        if response.success:
            messagebox.showinfo("Info", response.message)
        else:
            messagebox.showerror("Error", response.message)
    except ValueError:
        messagebox.showerror("Error", "Item ID must be an integer and price must be a valid number")

def delete_item_clicked():
    try:
        item_id = int(item_id_entry.get())
        response = client.delete_item(item_id)
        if response.success:
            clear_labels()
            messagebox.showinfo("Info", response.message)
        else:
            messagebox.showerror("Error", response.message)
    except ValueError:
        messagebox.showerror("Error", "Item ID must be an integer")

    read_item_clicked()

client = ShoppingClient()

app = CTk()
app.geometry("500x400")
app.title("Shopping Notes")

item_id_label = CTkLabel(master=app, text="Item ID:")
item_id_label.grid(row=0, column=0)

item_id_entry = CTkEntry(master=app)
item_id_entry.grid(row=0, column=1)

item_name_display_label = CTkLabel(master=app, text="")
item_name_display_label.grid(row=1, column=0, columnspan=2)

price_display_label = CTkLabel(master=app, text="")
price_display_label.grid(row=2, column=0, columnspan=2)

item_name_label = CTkLabel(master=app, text="Item Name:")
item_name_label.grid(row=3, column=0)

item_name_entry = CTkEntry(master=app)
item_name_entry.grid(row=3, column=1)

price_label = CTkLabel(master=app, text="Price:")
price_label.grid(row=4, column=0)

price_entry = CTkEntry(master=app)
price_entry.grid(row=4, column=1)

create_button = CTkButton(master=app, text="Create Item", command=create_item_clicked)
create_button.grid(row=5, column=0, columnspan=2)

read_button = CTkButton(master=app, text="Read Item", command=read_item_clicked)
read_button.grid(row=6, column=0, columnspan=2)

update_button = CTkButton(master=app, text="Update Item", command=update_item_clicked)
update_button.grid(row=7, column=0, columnspan=2)

delete_button = CTkButton(master=app, text="Delete Item", command=delete_item_clicked)
delete_button.grid(row=8, column=0, columnspan=2)

app.mainloop()
