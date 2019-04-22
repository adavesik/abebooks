# abebooks

How To Use

Inputed CSV file should be located in the same directory as script. In this example this the "albert.csv" file.

``
build_link("albert.csv") # input CVS file
``

In generate_csv() function


``
def generate_csv():
    with open('albert.csv') as csvfile:
        reader = csv.DictReader(csvfile)
with open('albert_final.csv', 'a', newline='') as csvfinal:
``

albert_final.csv - generated file. Script will create that if there is no
