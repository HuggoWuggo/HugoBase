import argparse
import os
import subprocess

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    YELLOW = "\033[1;33m"

class Type:
    STRING = str
    INT = int
    FLOAT = float
    BOOL = bool
    DATE = str

class Column:
    def __init__(self, name: str, type: Type, length: int = None, default_value = None):
        self.name = name
        self.type = type
        self.length = length
        self.value = default_value

    def __str__(self):
        return f"Name: {self.name}, Type: {self.type.__name__}, Length: {self.length}"

    def edit(self, name: str = None, type: Type = None, length: int = None, value = None):
        pass
    
class Table:
    def __init__(self, name: str, columns: list[Column], author=None, version=1.0):
        self.name = name
        self.columns = columns
        self.author = author
        self.version = version

    def __str__(self):
        columns_str = "\n                ".join(str(col) for col in self.columns)  # Join columns with a comma

        return f"\n        Name: {self.name},\n        Columns: [\n                {columns_str}\n        ],\n        Author: {self.author},\n        Version: {self.version}\n"

class Database:
    def __init__(self):
        self.tables = []

    def create(self, name: str, author=None, version=1.0):
        self.name = name
        self.author = author
        self.version = version

    def add_table(self, table: Table):
        self.tables.append(table)

    def info(self) -> str:
        tables_str = "\n        ".join(str(col) for col in self.tables)
        return f"Database: {self.name},\n    Tables: [{tables_str}    ],\nAuthor: {self.author},\nVersion: {self.version}\n"

parser = argparse.ArgumentParser(description="This is a custom DataBase Maker For Robotics and Coding 2025! Made By Me (Hugo Lewczak)")

parser.add_argument("-cd", "--create_database", help="Create a New Database", action="store_true")
parser.add_argument("-ct", "--create_table", help="Create a New Table", action="store_true")
parser.add_argument("-u", "--use", help="Use an Existing Database", nargs=1)
parser.add_argument("-d", "--delete", help="Delete an Existing Database", action="store_true")

args = parser.parse_args()

db_name = None

if args.use and args.create_database:
    print(f"{bcolors.FAIL}You can't use and create a database at the same time!{bcolors.ENDC}")
    exit()
elif args.create_database:
    db = Database()

    print(f"{bcolors.OKGREEN}Welcome to the Database Maker!{bcolors.ENDC}")
    print(f"{bcolors.OKCYAN}TYPE 'EXIT' (without the quotes) to exit in either table name or column name prompts{bcolors.ENDC}")
    
    db_name = str(input(f"Enter the{bcolors.OKGREEN} name{bcolors.ENDC} of the {bcolors.YELLOW}database{bcolors.ENDC}: "))
    db_author = str(input(f"Enter the{bcolors.OKGREEN} author{bcolors.ENDC} of the {bcolors.YELLOW}database{bcolors.ENDC}: "))
    if db_author == "":
        db_author = "Anonymous"

    db.create(name=db_name, author=db_author)

    while 1:
        table_name = str(input(f"Enter the{bcolors.OKGREEN} name{bcolors.ENDC} of a {bcolors.YELLOW}table{bcolors.ENDC} you want to make: "))
        if table_name == "exit" or table_name == "EXIT":
            break
        else:
            columns = []
            while 1:
                column_name = str(input(f"Enter the{bcolors.OKGREEN} name{bcolors.ENDC} of the {bcolors.YELLOW}column{bcolors.ENDC} you want to make: "))
                if column_name == "exit" or column_name == "EXIT":
                    break
                else:
                    while 1:
                        column_type = str(input(f"Enter the{bcolors.OKGREEN} type{bcolors.ENDC} of the {bcolors.YELLOW}column{bcolors.ENDC} you want to make: "))

                        match column_type:
                            case "str" | "string" | "STRING" | "STR":
                                column_type = Type.STRING
                                break
                            case "int" | "INT":
                                column_type = Type.INT
                                break
                            case "float" | "FLOAT":
                                column_type = Type.FLOAT
                                break
                            case "bool" | "BOOL":
                                column_type = Type.BOOL
                                break
                            case "date" | "DATE":
                                column_type = Type.DATE
                                break
                            case _:
                                print(f"{bcolors.FAIL}Invalid Type!{bcolors.ENDC}")
                                continue

                    column_length = 100

                    column_length = int(input(f"Enter the{bcolors.OKGREEN} length{bcolors.ENDC} of the {bcolors.YELLOW}column{bcolors.ENDC} you want to make: "))
                    column_default_value = str(input(f"Enter the{bcolors.OKGREEN} default value{bcolors.ENDC} of the {bcolors.YELLOW}column{bcolors.ENDC} you want to make: "))

                    columns.append(Column(name=column_name, type=column_type, length=column_length, default_value=column_default_value))

            table_author = str(input(f"Enter the{bcolors.OKGREEN} author{bcolors.ENDC} of the {bcolors.YELLOW}table{bcolors.ENDC}: "))
            if table_author == "":
                table_author = "Anonymous"
                    

            db.add_table(Table(name=table_name, columns=columns, author=table_author))
        
    os.system("cls")
    print("Successfully Created Database!")

    file_name = db_name.replace(" ", "_")
    file_name += ".hdb"

    with open(file_name, "w") as file:
        file.write(f"{db.info()}")

    subprocess.run(["attrib","+H",file_name],check=True)
elif args.use:
    if not os.path.exists(args.use[0]):
        print(f"{bcolors.FAIL}Database Not Found!{bcolors.ENDC}")
    else:
        file = open(args.use[0], "r")
        print(file.read())
        if args.delete:
            os.remove(f"{args.use[0]}")
            print(f"{bcolors.OKGREEN}Successfully Deleted Database!{bcolors.ENDC}")
elif args.delete:
    print(f"{bcolors.FAIL}You need to specify a database to delete!{bcolors.ENDC}")