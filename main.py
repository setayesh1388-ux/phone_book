import json
import tkinter as tk
from tkinter import ttk, filedialog


# ساخت پنجره
window = tk.Tk()
window.title("Phone Book")
window.geometry("800x600")


# لیست مخاطبین
contacts = []

tk.Label(window, text="name").pack()

name_entry = tk.Entry(window)
name_entry.pack()

tk.Label(window, text="last name").pack()

family_entry = tk.Entry(window)
family_entry.pack()


tk.Label(window, text="phone number").pack()

phone_entry = tk.Entry(window)
phone_entry.pack()

tk.Label(window, text="email").pack()

email_entry = tk.Entry(window)
email_entry.pack()

tk.Label(window, text="relation").pack()

relation = ttk.Combobox(
    window,
    values=["family", "co_work", "others"])

relation.pack()

favorite = tk.BooleanVar()

tk.Checkbutton(
    window,
    text="Favorite",
    variable=favorite
).pack()


tk.Label(window, text="note").pack()

note_text = tk.Text(
    window,
    height=5,
    width=40)

note_text.pack()


tree = ttk.Treeview(
    window,
    columns=(
        "name",
        "last_name",
        "phone",
        "email",
        "relation",
        "favorite",
        "note"),
    show="headings")


tree.heading("name", text="Name")
tree.heading("last_name", text="Last Name")
tree.heading("phone", text="Phone")
tree.heading("email", text="Email")
tree.heading("relation", text="Relation")
tree.heading("favorite", text="Favorite")
tree.heading("note", text="Note")

tree.pack(fill="both", expand=True)


def add_contact():

    name = name_entry.get()
    last_name = family_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    relation_value = relation.get()
    favorite_value = favorite.get()
    note = note_text.get("1.0", tk.END).strip()

    contact = {
        "name": name,
        "last_name": last_name,
        "phone": phone,
        "email": email,
        "relation": relation_value,
        "favorite": favorite_value,
        "note": note}

    contacts.append(contact)

    tree.insert(
        "",
        tk.END,
        values=(
            name,
            last_name,
            phone,
            email,
            relation_value,
            "*" if favorite_value else "",
            note))

    # خالی کردن فیلدها
    name_entry.delete(0, tk.END)
    family_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)

    relation.set("")
    favorite.set(False)
    note_text.delete("1.0", tk.END)


# دکمه Add Contact
tk.Button(
    window,
    text="Add contact",
    command=add_contact
).pack()

def delete_contact():

    selected = tree.selection()

    for item in selected:
        tree.delete(item)


tk.Button(
    window,
    text="Delete contact",
    command=delete_contact
).pack()


tk.Label(window, text="Search").pack()

search_entry = tk.Entry(window)
search_entry.pack()


def search_contact():

    search_text = search_entry.get().lower()

    # پاک کردن Treeview
    for item in tree.get_children():
        tree.delete(item)

    # جستجو
    for contact in contacts:

        if (
            search_text in contact["name"].lower()
            or search_text in contact["last_name"].lower()
            or search_text in contact["phone"].lower()
        ):

            tree.insert(
                "",
                tk.END,
                values=(
                    contact["name"],
                    contact["last_name"],
                    contact["phone"],
                    contact["email"],
                    contact["relation"],
                    "*" if contact["favorite"] else "",
                    contact["note"]))


tk.Button(
    window,
    text="Search",
    command=search_contact).pack()




def choose_image():

    image_path = filedialog.askopenfilename()

    if image_path:
        print(image_path)


tk.Button(
    window,
    text="Choose image",
    command=choose_image
).pack()


def save_contacts():

    with open(
        "contacts.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            contacts,
            file,
            ensure_ascii=False,
            indent=4
        )

    print("Contacts saved!")


tk.Button(
    window,
    text="Save contacts",
    command=save_contacts
).pack()


def load_contacts():

    global contacts

    try:

        with open(
            "contacts.json",
            "r",
            encoding="utf-8"
        ) as file:

            contacts = json.load(file)

        for contact in contacts:

            tree.insert(
                "",
                tk.END,
                values=(
                    contact["name"],
                    contact["last_name"],
                    contact["phone"],
                    contact["email"],
                    contact["relation"],
                    "*" if contact["favorite"] else "",
                    contact["note"]))

    except FileNotFoundError:

        contacts = []


# خواندن مخاطبین ذخیره شده
load_contacts()

window.mainloop()