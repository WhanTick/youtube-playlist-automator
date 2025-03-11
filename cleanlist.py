import os.path

list = open("musiclist.txt")

if not os.path.isfile("cleanedlist.txt"):
    cleaned_list = open("cleanedlist.txt", "x")
else:
    cleaned_list = open("cleanedlist.txt", "w")

new_string = ""
for i, item in enumerate(list):
    index = item.find("[")
    clean = item[:index:]
    if i == 0:
        new_string += f"{clean}"
    else:
        new_string += f"\n{clean}"


cleaned_list.write(new_string)
list.close()
cleaned_list.close()
