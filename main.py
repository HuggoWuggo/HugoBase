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
    def __init__(self, name: str, type: Type, length: int = None, values=None, default_value=None):
        self.name = name
        self.type = type
        self.length = length
        # If default_value is provided, use it as the sole value.
        if default_value is not None:
            self.values = [default_value]
        # Otherwise, use provided values or an empty list.
        else:
            self.values = values if values is not None else []

    def __str__(self):
        type_name = self.type.__name__ if hasattr(self.type, '__name__') else self.type
        # Join values with the nicer separator.
        formatted_values = ",\n\t\t\t\t".join(str(value) for value in self.values)
        return (f"Column-Name: {self.name}, Type: {type_name}, Length: {self.length}, values [\n\t\t\t\t"
                f"{formatted_values}\n\t\t\t], end-values")

    def edit(self, name: str = None, type: Type = None, length: int = None, value=None):
        # Implementation left as needed.
        pass

    def insert_into(self, value, location=None):
        """
        Insert the given value into the column's values.
        If a location is provided (and valid), insert at that position;
        otherwise, append to the end.
        """
        value_str = str(value)
        # If location is invalid or not provided, append.
        if location is None or not isinstance(location, int) or location < 0 or location > len(self.values):
            self.values.append(value_str)
        else:
            self.values.insert(location, value_str)



    def values(self):
        return self.values
    
class Table:
    def __init__(self, name: str, columns: list[Column], author=None, version=1.0):
        self.name = name
        self.columns = columns
        self.author = author
        self.version = version

    def __str__(self):
        columns_str = "\n\t\t\t".join(str(col) for col in self.columns)
        return f"\n\t\tTable-Name: {self.name},\n\t\tColumns: [\n\t\t\t{columns_str}\n\t\t], end-columns\n\t\tAuthor: {self.author},\n\t\tVersion: {self.version}\n"

    def columns(self):
        return self.columns

class Database:
    def __init__(self):
        self.tables = []
        self.author = ""
        self.version = 1.0

    def create(self, name: str, author=None, version=1.0):
        self.name = name
        self.author = author
        self.version = version

    def add_table(self, table: Table):
        self.tables.append(table)

    def info(self) -> str:
        tables_str = "\n\t\t".join(f"{str(table)}\t\tend_table\n" for table in self.tables)
        return f"Database: {self.name},\n\tTables: [\n\t\t{tables_str}\n\t], end-tables\nAuthor: {self.author},\nVersion: {self.version}\n"
    
    def load(self, file_name: str) -> list[Table]:
        with open(file_name, "r") as file:
            content = file.read()
        
        # Extract database name
        try:
            _, part2 = content.split("Database: ", 1)
            self.name = part2.split(",", 1)[0].strip()
        except ValueError:
            print("Error: 'Database: ' not found in file.")
            return

        # Extract tables section
        try:
            _, part2 = content.split("Tables: [", 1)
            tables_string = part2.split("], end-tables", 1)[0]
        except ValueError:
            print("Error: 'Tables: [' or '], end-tables' not found in file.")
            return

        # Process each table
        while "Table-Name: " in tables_string:
            try:
                # Extract table name
                tables_string = tables_string.split("Table-Name: ", 1)[1]
                table_name = tables_string.split(",", 1)[0].strip()

                # Extract columns section
                _, tables_string = tables_string.split("Columns: [", 1)
                columns_string, tables_string = tables_string.split("], end-columns", 1)

                # Extract columns
                columns = []
                while "Column-Name:" in columns_string:
                    try:
                        _, columns_string = columns_string.split("Column-Name: ", 1)
                        column_name, columns_string = columns_string.split(",", 1)
                        column_name = column_name.strip()

                        _, columns_string = columns_string.split("Type: ", 1)
                        column_type, columns_string = columns_string.split(",", 1)
                        column_type = column_type.strip()

                        _, columns_string = columns_string.split("Length: ", 1)
                        column_length, columns_string = columns_string.split(",", 1)
                        column_length = column_length.strip()

                        _, columns_string = columns_string.split("values [", 1)
                        values_string, columns_string = columns_string.split("], end-values", 1)
                        values = [v.strip() for v in values_string.split(",") if v.strip()]

                        columns.append(Column(name=column_name, type=column_type, length=column_length, values=values))
                    except ValueError as e:
                        print("Error parsing column:", e)
                        break  # Move to next table

                self.tables.append(Table(name=table_name, columns=columns))

                # Move to the next table
                if "end_table" in tables_string:
                    tables_string = tables_string.split("end_table", 1)[1]
                else:
                    break  # No more tables

            except ValueError as e:
                print("Error parsing table:", e)
                break  # Stop processing if an error occurs

        # Print parsed tables and columns for verification

        return self.tables

    def table_wizard(self):
        while True:
            while True:
                table_name = input(f"Enter the{bcolors.OKGREEN} name{bcolors.ENDC} of a {bcolors.YELLOW}table{bcolors.ENDC} you want to make: ")
                if table_name != "":
                    break
                else:
                    print(f"{bcolors.FAIL}Table Name Can't Be Empty!{bcolors.ENDC}")

            if table_name.lower() == "exit":
                break
            else:
                table_author = input(f"Enter the{bcolors.OKGREEN} author{bcolors.ENDC} of the {bcolors.YELLOW}table{bcolors.ENDC}: ")
                if table_author == "":
                    table_author = "Anonymous"
                columns = []
                while True:
                    column_name = input(f"Enter the{bcolors.OKGREEN} name{bcolors.ENDC} of the {bcolors.YELLOW}column{bcolors.ENDC} you want to make: ")
                    if column_name.lower() == "exit":
                        break
                    else:
                        while True:
                            column_type = input(f"Enter the{bcolors.OKGREEN} type{bcolors.ENDC} of the {bcolors.YELLOW}column{bcolors.ENDC} you want to make: ")
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
                        while True:
                            column_length_input = input(f"Enter the{bcolors.OKGREEN} length{bcolors.ENDC} of the {bcolors.YELLOW}column{bcolors.ENDC} you want to make: ")
                            if column_length_input == "":
                                column_length = 255
                                break
                            else:
                                try:
                                    column_length = int(column_length_input)
                                    break
                                except ValueError:
                                    print(f"{bcolors.FAIL}Invalid Length!{bcolors.ENDC}")

                        column_default_value = input(f"Enter the{bcolors.OKGREEN} default value{bcolors.ENDC} of the {bcolors.YELLOW}column{bcolors.ENDC} you want to make: ")

                        columns.append(Column(name=column_name, type=column_type, length=column_length, default_value=column_default_value))
                self.add_table(Table(name=table_name, columns=columns, author=table_author))

def print_table(table: Table, order = None):
    num = -1
    max_values = []

    for column in table.columns:
        num += 1
        max_values.append(5)
        if len(column.name) > max_values[num]:
            max_values[num] = len(column.name)
        
        for value in column.values:
            if len(value) > max_values[num]:
                max_values[num] = len(value)
    
    print("| ", end="")
    num = -1
    while num < len(max_values) - 1:
        num += 1
        print(f"{table.columns[num].name:<{max_values[num]}}", end="")
        print(" | ", end="")
    
    print("")
    print("|", end="")

    for i in range(len(max_values)):
        for y in range(max_values[i] + 2):
            print("-", end="")
        print("|", end="")

    print("")

    # Determine the maximum number of rows among all columns
    max_rows = max(len(column.values) for column in table.columns)

    # For each row index, iterate over each column and print the value if it exists,
    # otherwise print an empty string
    for row in range(max_rows):
        print("| ", end="")
        for col_index, column in enumerate(table.columns):
            # Get the value if available, else use an empty string
            value = column.values[row] if row < len(column.values) else ""
            # Use the corresponding max width for that column
            print(f"{value:<{max_values[col_index]}} | ", end="")
        print("")  # Newline after each row

    
def main():
    parser = argparse.ArgumentParser(description="This is a custom DataBase Maker For Robotics and Coding 2025! Made By Me (Hugo Lewczak)")

    parser.add_argument("-cd", "--create_database", help="Create a New Database", action="store_true")
    parser.add_argument("-ct", "--create_table", help="Create a New Table", action="store_true")
    parser.add_argument("-u", "--use", help="Use an Existing Database", nargs=1, metavar="DATABASE")
    parser.add_argument("-d", "--delete", help="Delete an Existing Database", action="store_true")
    parser.add_argument("-t", "--table", help="Use a Table From an Existing Database", nargs=1, metavar="TABLE_NAME")
    parser.add_argument("-i", "--insert", help="Insert data into table", nargs=2, metavar=("DATA", "COLUMN_NAME"))
    parser.add_argument("-ld", "--list_databases", help="List any databases in the current directory", action="store_true")
    parser.add_argument("-lt", "--list_tables", help="List any tables in a specified database", action="store_true")


    args = parser.parse_args()

    db_name = None

    if args.use and args.create_database:
        print(f"{bcolors.FAIL}You can't use and create a database at the same time!{bcolors.ENDC}")
        exit()
    elif args.list_databases:
        files = [file for file in os.listdir('.') if file.endswith('.hdb')]
        for file in files:
            print(file)
    elif args.list_tables:
        db = Database()
        tables = db.load(args.use[0])
        for i, table in enumerate(tables):
            print(f"Table {i} : {table.name}")
    elif args.create_database:
        db = Database()

        print(f"{bcolors.OKGREEN}Welcome to the Database Maker!{bcolors.ENDC}")
        print(f"{bcolors.OKCYAN}TYPE 'EXIT' (without the quotes) to exit in either table name or column name prompts{bcolors.ENDC}")
        
        db_name = input(f"Enter the{bcolors.OKGREEN} name{bcolors.ENDC} of the {bcolors.YELLOW}database{bcolors.ENDC}: ")
        db_author = input(f"Enter the{bcolors.OKGREEN} author{bcolors.ENDC} of the {bcolors.YELLOW}database{bcolors.ENDC}: ")
        if db_author == "":
            db_author = "Anonymous"

        db.create(name=db_name, author=db_author)
        db.table_wizard()
            
        os.system("cls")
        print("Successfully Created Database!")
        
        file_name = db_name.replace(" ", "_") + ".hdb"
        
        # Delete the file if it already exists
        if os.path.exists(file_name):
            os.remove(file_name)
        
        # Open the file in write mode so that it's newly created
        with open(file_name, "w") as file:
            file.write(db.info())

        subprocess.run(["attrib", "+H", file_name], check=True)
    elif args.use:
        if not os.path.exists(args.use[0]):
            print(f"{bcolors.FAIL}Database Not Found!{bcolors.ENDC}")
        else:
            with open(args.use[0], "r") as file:
                content = file.read()
                #print(content)

            db = Database()
            tables = db.load(args.use[0])

            if args.delete:
                os.remove(args.use[0])
                print(f"{bcolors.OKGREEN}Successfully Deleted Database!{bcolors.ENDC}")
            elif args.create_table:
                db.table_wizard()
            elif args.table:
                # table_index = int(args.table[0])
                # col_index = int(args.insert[1])

                table_index = -1
                column_index = -1
                index = -1
                index_c = -1

                c_name = ""

                for table in tables:
                    index += 1
                    if table.name == args.table[0]:
                        table_index = index
                        if args.insert:
                            for column in table.columns:
                                if column.name == args.insert[1]:
                                    index_c += 1
                                    column_index = index_c
                                    c_name = column.name
                                    break
                        break
                
                if args.insert:
                    if table_index != -1 and column_index != -1:
                        for column in tables[table_index].columns:
                            if column.name == args.insert[1]:
                                column.insert_into(f"{args.insert[0]}", 0)
                            else:
                                column.insert_into(f"NULL", 0)
                        os.remove(args.use[0])
                        with open(args.use[0], "w") as file:
                            file.write(db.info())
                    else:
                        print(f"{bcolors.FAIL}Incorrect column name or table name{bcolors.ENDC}")
                        exit()

                print_table(tables[table_index])
            else:
                print(f"{bcolors.FAIL}The use action needs to do something!{bcolors.ENDC}")
            
            # for table in tables:
            #     print(f"Table: {table.name}")
            #     for column in table.columns:
            #         print(f"  Column: {column.name}, Type: {column.type}, Length: {column.length}, Values: {column.values}")

    elif args.delete or args.create_table or args.table:
        print(f"{bcolors.FAIL}You need to specify a database to edit it!{bcolors.ENDC}")
    elif args.insert:
        print(f"{bcolors.FAIL}You need to specify a table to edit it!{bcolors.ENDC}")

if __name__ == "__main__":
    main()
