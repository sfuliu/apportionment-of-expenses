from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk
import pyperclip

# create_new = False: if there is old apportionment cost data: read the count of people
# create_new = True: no old data: create variable: count let person can input
def save_count():
    global count

    if create_new:
        database["count"] = []
        count = people_count_entry.get()
        if count.isdigit() == False or count == "0":
            messagebox.showinfo(title="Oops", message="Please input an integer that is > 0")
            people_count_entry.delete(0, END)
            return
        else:
            information = f"The number of people : {count}\n\nIs correct?"
            confirm_count = messagebox.askyesno(title="Number of people", message=information)
            if confirm_count:
                database["count"].append(int(count))
                people_count_entry.delete(0, END)
                people_count_entry.grid_remove()
                count = int(count)

                people_count_confirm_button.grid_remove()
    else:
        count = database["count"][0]
    # show the count of people on the window
    people_count_label.config(text=f"Number of people :  {count}")
    people_count_label.grid(row=0, column=0, columnspan=2)

    create_people_label()


# check create_new = False: has old data: read the all people name from old data
# check create_new = True: no old data: let user input all people name
def create_people_label():
    global name_list, people_name_confirm_button
    name_list = []
    for row in range(1, count + 1):
        globals()['people_name_label_' + str(row)] = Label(text="                       P.%-2d : " % row)
        globals()['people_name_label_' + str(row)].grid(row=row, column=0)


    if create_new:
        for row in range(1, count + 1):
            globals()['people_name_entry_' + str(row)] = Entry(width=10)
            globals()['people_name_entry_' + str(row)].grid(row=row, column=1)
        globals()['people_name_entry_' + '1'].focus()

        people_name_confirm_button = Button(text="Confirm", command=save_name)
        people_name_confirm_button.grid(row=count, column=3)
    else:
        for name in database["name"]:
            name_list.append(name)
        save_name()

# check if all datas have been inputed
# result for new input = True
# result for modify data = False
def check_all_data_input():
    if cost_item_entry.get() == "":
        messagebox.showinfo(title="Oops", message="Please input 'The spending item'")
        return False
    if (pay_money_entry.get().isdigit() == False) or (pay_money_entry.get() == "0"):
        messagebox.showinfo(title="Oops", message="Please input expense that is > 0")
        return False
    if who_pay_box.get() == "":
        messagebox.showinfo(title="Oops", message='Please choose a person from "Who pay money" item')
        return False
    all_apportion_people = ""
    for (name, var) in choice_person.items():
        if var.get() == 1:
            all_apportion_people += name + ", "
    global confirm_input_pay_data
    information = f"The spending item : {cost_item_entry.get()}\nWho pay money : {who_pay_box.get()}\nHow much : $ {pay_money_entry.get()}\nApportion people : {all_apportion_people[:-2]}\n\nIs all data right?"
    confirm_input_pay_data = messagebox.askyesno(title="Input information", message=information)
    if confirm_input_pay_data == False:
        return False

    check_apportion_people = 0
    for (name, var) in choice_person.items():
        check_apportion_people += var.get()
    if check_apportion_people == 0:
        messagebox.showinfo(title="Oops", message='Please choose who need to apportion from "Apportion people" item')
        return False

# clear all input data after confirm add data
# then save into database
def clear_input_and_save():
    if confirm_input_pay_data == True:
        cost_item_entry.delete(0, END)
        who_pay_box.set("")
        pay_money_entry.delete(0, END)
        position = -1
        for (name, var) in choice_person.items():
            position += 1
            if var.get() == 0:
                menu.invoke(position)


    for line in lines:
        if file_name_entry.get() in line["file_name"]:
            lines.remove(line)

    lines.append(database)
    with open("database.txt", mode="w") as data:
        data.write("")
    with open("database.txt", mode="a") as data:
        for line in range(len(lines) - 1, -1, -1):
            data.write(f"{lines[line]}\n")


def calculator_add_to_dict():

    # check if all datas have been inputed
    # result = False -> stop process
    check_result = check_all_data_input()
    if check_result == False:
        return
    database["item"].append(cost_item_entry.get())
    database["Who_pay"].append(who_pay_box.get())
    database["money"].append(pay_money_entry.get())
    count_need_to_pay = 0
    for (name, var) in choice_person.items():
        count_need_to_pay += int(var.get())
        database["apportion_yn_"+name].append(var.get())
    for (name, var) in choice_person.items():
        if name != who_pay_box.get():
            if var.get() != 0:
                database["apportion_money_" + name].append(eval(pay_money_entry.get())/count_need_to_pay)
            else:
                database["apportion_money_" + name].append(0)
        else:
            database["apportion_money_" + name].append(0)

    for (name, var) in choice_person.items():
        for name_1 in name_list:
            if name != name_1:
                if who_pay_box.get() == name_1 and var.get() != 0:
                    database[name + " give " + name_1].append(eval(pay_money_entry.get())/count_need_to_pay)
                else:
                    database[name + " give " + name_1].append(0)

    for name in name_list:
        locals()[name + "_pay_money"] = 0
        locals()[name + "_gain_money"] = 0
    for name in name_list:
        for name_1 in name_list:
            if name != name_1:
                for cost in database[name + " give " + name_1]:
                    locals()[name + "_pay_money"] += cost
        database[name + "_pay"] = locals()[name + "_pay_money"]
    for name_1 in name_list:
        for name in name_list:
            if name != name_1:
                for cost in database[name + " give " + name_1]:
                    locals()[name_1 + "_gain_money"] += cost
        database[name_1 + "_gain"] = locals()[name_1 + "_gain_money"]
    summary = []
    for name in name_list:
        database["summary_" + name] = database[name + "_pay"] - database[name + "_gain"]

    # clear all input data after confirm add data
    # then save into database
    clear_input_and_save()



# let the number of people need to apportion show on the menubutton
def check_choice_person_num():
    choice_person_num = 0
    for (key, num) in choice_person.items():
        choice_person_num += num.get()
    apportion_people_menubutton.config(text=f"All member({choice_person_num})")


def input_apportionment_detail():
    global tab_1, add_window
    add_window = Toplevel(window)
    add_window.grab_set()
    add_window.config(padx=20, pady=20, height=200, width=350)
    add_window.title("Add new cost")

    tab_main = ttk.Notebook(add_window)  # create a shift
    tab_main.place(relx=0.02, rely=0.02, relheight=1, relwidth=0.9)

    tab_1 = Frame(tab_main) # first shift
    tab_1.place(x=0, y=30)
    tab_main.add(tab_1, text="Pay")
    tab_1.config(pady=10, padx=10)

    # tab_2 = Frame(tab_main)  # second shift
    # # tab_2.place(x=0, y=30)
    # tab_main.add(tab_2, text="Gain")
    # tab_2.config(pady=10, padx=10)

    global cost_item_entry
    cost_item_label = Label(tab_1, text="The spending item : ")
    cost_item_label.grid(row=0, column=0)

    cost_item_entry = Entry(tab_1, width=16, justify='left')
    cost_item_entry.grid(row=0, column=1)
    cost_item_entry.focus()

    who_pay_label = Label(tab_1, text="Who pay money : ")
    who_pay_label.grid(row=1, column=0)

    global who_pay_box, pay_money_entry
    who_pay_box = ttk.Combobox(tab_1,
                               width=14,
                               values=name_list,
                               state="readonly")
    who_pay_box.grid(row=1, column=1)

    pay_money_label = Label(tab_1, justify='right', text="How much : $")
    pay_money_label.grid(row=2, column=0)
    pay_money_entry = Entry(tab_1, width=16, justify='center')
    pay_money_entry.grid(row=2, column=1)

    # choice who need to apportion

    apportion_people_label = Label(tab_1, text="Apportion people : ")
    apportion_people_label.grid(row=3, column=0)

    global apportion_people_menubutton, menu
    apportion_people_menubutton = Menubutton(tab_1, text=f"All member({len(name_list)})",
                                             indicatoron=True, highlightthickness=1, relief="raised")

    menu = Menu(apportion_people_menubutton, tearoff=False)
    apportion_people_menubutton.configure(menu=menu, padx=10)
    apportion_people_menubutton.grid(row=3, column=1)




def add_cost_window():
    input_apportionment_detail()

    global choice_person
    choice_person = {}
    for person in name_list:
        choice_person[person] = IntVar(value=1)
        menu.add_checkbutton(label=person, variable=choice_person[person],
                             onvalue=1, offvalue=0,
                             command=check_choice_person_num)


    all_pay_data_confirm_button = Button(tab_1, text="Add", command=calculator_add_to_dict)
    all_pay_data_confirm_button.grid(row=5, column=1)


def modify_list_detail():
    check_result = check_all_data_input()
    if check_result == False:
        return

    position = database["item"].index(modify_item)
    database["item"][position] = cost_item_entry.get()
    database["Who_pay"][position] = who_pay_box.get()
    database["money"][position] = pay_money_entry.get()

    count_need_to_pay = 0
    for (name, var) in choice_person.items():
        count_need_to_pay += int(var.get())
        database["apportion_yn_" + name][position] = var.get()
    for (name, var) in choice_person.items():
        if name != who_pay_box.get():
            if var.get() != 0:
                database["apportion_money_" + name][position] = eval(pay_money_entry.get()) / count_need_to_pay
            else:
                database["apportion_money_" + name][position] = 0
        else:
            database["apportion_money_" + name][position] = 0

    for (name, var) in choice_person.items():
        for name_1 in name_list:
            if name != name_1:
                if who_pay_box.get() == name_1 and var.get() != 0:
                    database[name + " give " + name_1][position] = eval(pay_money_entry.get()) / count_need_to_pay
                else:
                    database[name + " give " + name_1][position] = 0

    for name in name_list:
        locals()[name + "_pay_money"] = 0
        locals()[name + "_gain_money"] = 0
    for name in name_list:
        for name_1 in name_list:
            if name != name_1:
                for cost in database[name + " give " + name_1]:
                    locals()[name + "_pay_money"] += cost
        database[name + "_pay"] = locals()[name + "_pay_money"]
    for name_1 in name_list:
        for name in name_list:
            if name != name_1:
                for cost in database[name + " give " + name_1]:
                    locals()[name_1 + "_gain_money"] += cost
        database[name_1 + "_gain"] = locals()[name_1 + "_gain_money"]
    summary = []
    for name in name_list:
        database["summary_" + name] = database[name + "_pay"] - database[name + "_gain"]

    # clear all input data after confirm add data
    # then save into database
    clear_input_and_save()
    add_window.destroy()
    list_window.destroy()
    cost_list_window()


def list_modify_window():
    listbox_used()

    position = database["item"].index(modify_item)
    input_apportionment_detail()
    add_window.title("Modify this cost")

    cost_item_entry.insert(0, modify_item)
    who_pay_box.set(database["Who_pay"][position])
    pay_money_entry.insert(0, database["money"][position])

    global choice_person
    choice_person = {}
    for person in name_list:
        choice_person[person] = IntVar(value=0)
        menu.add_checkbutton(label=person, variable=choice_person[person],
                             onvalue=1, offvalue=0,
                             command=check_choice_person_num)
    posi = -1
    for name in database["name"]:
        posi += 1
        if database["apportion_yn_" + name][position] == 1:
            menu.invoke(posi)

    all_pay_data_confirm_button = Button(tab_1, text="Modify", command=modify_list_detail)
    all_pay_data_confirm_button.grid(row=5, column=1)

# def listbox_used(event):
def listbox_used():
    global modify_item
    # Gets current selection from listbox
    # the listbox.curselection() get type of turple, ex: (n,)
    n, = listbox.curselection()
    choise_item = listbox.get(n)
    choise_item_separate = choise_item.split("  $")
    modify_item = choise_item_separate[0]


def cost_list_window():
    global list_window
    list_window = Toplevel(window)
    list_window.grab_set()
    list_window.config(padx=20, pady=20)
    list_window.title("Cost list")

    frame = Frame(list_window, width=15)
    frame.grid(row=0, column=0, columnspan=2)

    scrollbar = Scrollbar(frame)
    scrollbar.pack(side='right', fill='y')
    # scrollbar.grid(row=0, column=0)

    global listbox
    listbox = Listbox(frame, height=5, width=30, yscrollcommand = scrollbar.set)
    for item in database["item"]:
        position = database["item"].index(item)
        listbox.insert(position, item+"  $"+database["money"][position])
    listbox.pack(side='left', fill='y')
    scrollbar.config(command=listbox.yview)


    listbox.selection_set(0)

    if database["item"] != []:
        list_modify_button = Button(list_window, text="Modify", command=list_modify_window)
        list_modify_button.grid(row=1, column=0, pady=10)

    list_modify_cancel_button = Button(list_window, text="Cancel", command=list_window.destroy)
    list_modify_cancel_button.grid(row=1, column=1, pady=10)

def summary_window():
    # if create_new and (database["item"] == []):
    if database["item"] == []:
        messagebox.showerror(title="Oops!", message="You never input any data,\nwe can do anything for you.")
        return

    database["total_summary"] = []

    summ_window = Toplevel(window)
    summ_window.grab_set()
    summ_window.config(padx=20, pady=20, height=350, width=400)
    summ_window.title("Summary")

    money = []
    for name in name_list:
        money.append(database["summary_" + name])

    text = Text(summ_window, height=10, width=30)
    if max(money) == min(money):
        money = []
        for i in database["money"]:
            money.append(eval(i))
        database["total_summary"].append(f"Your total cost is {sum(money)}")
        text.insert(END, f"Your total cost is {sum(money)}")
        print(f"Your total cost is {sum(money)}")
    else:
        while (max(money) > 0) and (max(money) != min(money)):
            if (max(money) + min(money)) >= 0:
                database["total_summary"].append(name_list[money.index(max(money))] + " give " + name_list[
                    money.index(min(money))] + f" : $ {-round(min(money), 1)}")
                money[money.index(max(money))] = max(money) + min(money)
                money[money.index(min(money))] = 0
            else:
                database["total_summary"].append(name_list[money.index(max(money))] + " give " + name_list[
                    money.index(min(money))] + f" : $ {round(max(money), 1)}")
                money[money.index(max(money))] = 0
                money[money.index(min(money))] = max(money) + min(money)
        for summ in database["total_summary"]:
            text.insert(END, f"{summ}\n")

    text.config(state="disabled")
    # print(text.get("1.0", END))
    text.grid(row=0, column=0)
    paste_message_label = Label(summ_window, text="You can directly use keyboard ctrl+v to paste!")
    paste_message_label.grid(row=1, column=0)

    for line in lines:
        if file_name_entry.get() in line["file_name"]:
            lines.remove(line)

    lines.append(database)
    with open("database.txt", mode="w") as data:
        data.write("")
    with open("database.txt", mode="a") as data:
        for line in range(len(lines) - 1, -1, -1):
            data.write(f"{lines[line]}\n")

    text.focus()
    # have copied, it can paste directly by ctrl+v
    pyperclip.copy(text.get("1.0", END))

# save all people name into variable: name_list
# both has/no old data need to do
# then do the initial setting about variable: database
def save_name():
    global name_list
    if create_new:
        name_list = []
        for row in range(1, count + 1):
            people_name = globals()['people_name_entry_' + str(row)].get()
            name_list.append(people_name)
        name_double = False
        for i in range(len(name_list)):
            for j in range(len(name_list)):
                if i != j and name_list[i] == name_list[j]:
                    name_double = True
        if '' in name_list:
            messagebox.showinfo(title="Oops", message="Please don't leave any name empty!")
            return
        elif name_double:
            messagebox.showinfo(title="Oops", message="Please don't input the same name.")
            return
        else:
            database["name"] = []
            for name in name_list:
                database["name"].append(name)

        people_name_confirm_button.grid_remove()
        for row in range(1, count + 1):
            globals()['people_name_entry_' + str(row)].grid_remove()

        database["item"] = []
        database["Who_pay"] = []
        database["money"] = []
        for name in name_list:
            database["apportion_yn_" + name] = []
        for name in name_list:
            database["apportion_money_" + name] = []
        for name in name_list:
            for name_1 in name_list:
                if name != name_1:
                    database[name + " give " + name_1] = []
        for name in name_list:
            database[name + "_pay"] = []
            database[name + "_gain"] = []
        for name in name_list:
            database["summary_" + name] = []

    for row in range(1, count + 1):
        globals()['people_name_label_' + str(row)].grid_remove()

    add_cost_button = Button(window, text="Add new cost", width=25, pady=10, command=add_cost_window)
    add_cost_button.grid(row=1, column=0, columnspan=2, pady=5, padx=15)

    cost_list_button = Button(window, text="Cost list", command=cost_list_window)
    cost_list_button.grid(row=2, column=0, padx=30)

    cost_summary_button = Button(window, text="Summary", command=summary_window)
    cost_summary_button.grid(row=2, column=1, padx=30)


# check: there is the old apportionment cost file exist or not
# then decide what the next step need to do
def read_and_check_file_name():
    global people_count_label, lines, database, create_new, people_count_entry, people_count_confirm_button, file_name_label, file_name_entry, file_name_entry_button
    
    if file_name_entry.get() == "":
        messagebox.showinfo(title="Oops", message="Please input the activity name!")
        return


    # after entry file name, disappear all things about entry file name(Label, Entry, Button)
    file_name_label.grid_remove()
    file_name_entry.grid_remove()
    file_name_entry_button.grid_remove()

    people_count_label = Label(text=f"How many people : ")
    people_count_label.grid(row=0, column=0)

    # read information from file
    with open("database.txt", mode="r") as file:
        database = file.readline()
        lines = []
        if database == "":
            database = {}
            database["file_name"] = []
            create_new_yn = 1
        else:
            file.seek(0)
            for line in file.readlines():
                if line != "\n":
                    lines.append(eval(line))

            create_new_yn = 1
            for line in lines:
                if file_name_entry.get() in line["file_name"]:
                    create_new_yn *= -1
                    datas = line
                else:
                    create_new_yn *= 1

    if create_new_yn == -1:
        create_new = False
        database = datas
        lines.remove(datas)
        save_count()
    else:
        create_new = True
        database = {}
        database["file_name"] = []

        database["file_name"].append(file_name_entry.get())


        # the code about count of people (Entry, Button)
        people_count_entry = Entry(width=4, justify='center')
        people_count_entry.focus()
        people_count_entry.grid(row=0, column=1)

        people_count_confirm_button = Button(text="Confirm", command=save_count)
        people_count_confirm_button.grid(row=0, column=3)

    window.title(f"{file_name_entry.get()}")



window = Tk()
window.title("Apportionment of expenses")
window.config(padx=20, pady=20)


file_name_label = Label(text="The name of this activity :")
file_name_label.grid(row=0, column=0)


# just open file_name_list.txt.
# If this file not exist, it can create one.
with open("database.txt", mode="a") as file:
    file.write("")

with open("database.txt", mode="r") as file:
    old_file = []
    for line in file.readlines():
        if line != "" and line != "\n":
            old_file.append(eval(line)["file_name"])

file_name_entry = ttk.Combobox(width=14, values=old_file)
file_name_entry.focus()
file_name_entry.grid(row=1, column=0, pady=5)

file_name_entry_button = Button(text="Enter", command=read_and_check_file_name)
file_name_entry_button.grid(row=2, column=0)


window.mainloop()