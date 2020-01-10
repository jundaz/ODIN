import psycopg2
from datetime import date

def getConnection():

    new_conn = psycopg2.connect(user = 'parktae7', database = 'odin')

    return new_conn

def commitQuery(query, output):
	"""
	Prints out a successful statement if query worked. Else, print a error statement.

	Parameters
	----------
	query: str
		This is a query in the form of the string. Ex. "SELECT * FROM hello"
	output: str
		This string is the expected output that is printed depending on the query.
	"""
	try:
		conn = getConnection()
		cursor = conn.cursor()
		cursor.execute("SELECT version();")
		record = cursor.fetchone()
		print("You are connected to - ", record,"\n")
		cursor.execute(query)
		conn.commit()
		print(output)
	except (Exception, psycopg2.Error) as error:
		print ("Error while connecting to PostgreSQL", error)
	finally:
		if (conn):
			cursor.close()
			conn.close()
			print("PostgreSQL connection is closed")

"""
Alter, add and remove, you don't want to update (change the data)
"""

def createTableJson (json):
	"""
	Creates a new table in the odin database based on json objects.

	Parameters
	----------
	json: dict
		A json blob that contains the input statement that needs to be made.
	Returns
	-------
	Returns a message saying Table successfully created
	or error statement if syntax error.
	"""
	commitQuery(createTableJsonQuery(json), "Table created successfully in PostgreSQL")
def createTable(table_name, attr_dict):
	"""
	Creates a new table in the odin database.

	SHOULD IMPLEMENT: should delete the table if it already exists.

	Parameters
	----------
	table_name: string
		The name of the table that is to be created.
	attr_dict: dict
		A dictionary where the key is the column and value is the type of the column

	Returns
	-------
	Returns a message saying Table successfully created
	or error statement if syntax error.
	"""
	commitQuery(createTableQuery(table_name,attr_dict), "Table created successfully in PostgreSQL")

def insertTableJson(json):
	"""
	Inserts a json blobs that are to be added into the odin database.
	"""
	commitQuery(insertTableJsonQuery(json), "Table inserted successfully in PostgreSQL")

def insertTable(json):
	"""
	Inserts a list of values into the columns in the odin database.

	SHOULD IMPLEMENT: should give error if either the columnlst or valuelst is not inside the table.

	Parameters
	----------
	table_name: string
		The name of the table that information should be inserted into.
	attr_dict: dict
		The dictionary where the keys at the column_name and values are the values of the column_name.
	Returns
	-------
	Returns a message saying Table successfully inserted
	or error statement if syntax error.

	"""
	commitQuery(insertTableQuery(json), "Table inserted successfully in PostgreSQL")

def alterTable (table_name, attr_dict):
	"""
	Adds one single column into the existing table.

	Parameters
	----------
	table_name: string
		The name of the table where the column is to be added.
	attr_dict: dict
		A dictionary where the keys are the column name and value is the type of the column.
		The dictionary cannot have a length greater than 1.

	Returns
	-------
	Returns a message saying Table successfully altered
	or error statement if syntax error.
	"""
	commitQuery(alterTableQuery(table_name,attr_dict), "Table altered successfully in PostgreSQL")

def updateTable (table_name, attr_dict, condition = None):
	"""
	Updates the table_name by the given attr_dict. If the condition is given,
	then updates only at the specific condition.

	Parameters
	----------
	table_name: string
		The name of the table where the information is to be updated.
	attr_dict: dict
		A dictionary where the key is the column name and
							value is the value that is to be updated to.
	*condition: string
		A string that should be in the format "WHERE .....". This condition
		statement is optional, if this is empty, updates all the columns that are given.

	Returns
	-------
	Returns a message saying Table successfully updated
	or error statement if syntax error.
	"""
	commitQuery(updateTableQuery(table_name,attr_dict, *condition), "Table updated successfully in PostgreSQL")

def deleteTable(table_name, condition):
	"""
	Deletes the rows of the specific condition.

	Parameters
	----------
	table_name: string
		The name of the table in the odin database.
	condition: string
		A string in the format "WHERE ...." The specific condition where
		the rows should be deleted.

	Returns
	-------
	Returns a message saying Table successfully deleted
	or error statement if syntax error.
	"""
	commitQuery("DELETE FROM {} {};".format(table_name, condition), "Table deletected successfully in PostgreSQL")

def dropTable (table_name):

	commitQuery("Drop table {};".format(table_name), "Table dropped successfully in PostgreSQL")

def selectTable (table_name, variable = None, condition = None):
	"""
	Selects the table to read, if the columnlst is not defined, then reads the entire table,
	otherwise, reads the specific columns given.

	Parameters
	----------
	table_name : string
		The name of the table that is to be read.
	*columnlst : list
		Optional list of columns that is to be read. If the columnlst is not defined, reads the
		entire table.

	Returns
	-------
	Returns a message saying Table successfully read
	or error statement if syntax error.
	"""
	commitQuery(selectTableQuery(table_name, variable, condition), "Table read successfully in PostgreSQL")


def selectTableQuery(table_name, variable = None, condition = None):
	"""
	This is a helper function that returns the SELECT statement
	"""
	if (variable != None and condition == None):
		new_query = "SELECT {} FROM {}".format(variable, table_name)

	elif (variable !=None and condition != None):
		new_query = "SELECT {} FROM {} WHERE {}".format(variable, table_name, condition)
	else:
		new_query = "SELECT * FROM {}".format(table_name)
	return new_query

def createTableJsonQuery(json):
	"""
	This is a helper function that returns the CREATE TABLE statement
	"""
	column_lst = ''
	for column_name in json:
		if ("date" in column_name):
			column_lst = column_lst + column_name + " date, "
		elif (type(json[column_name]) == type({})):
			column_lst = column_lst + "stem_name " + "varchar, "
			column_lst = column_lst + "numstems " + "int, "
	column_lst = column_lst.strip(", ")
	create_sql = "CREATE TABLE {} ({});".format(json["service"],column_lst)
	return create_sql

def createTableQuery(table_name ,attr_dict):
	"""
	This is a helper function that returns the CREATE TABLE statement
	"""
	data_str = ''
	for keys in attr_dict:
		statement = keys + ' ' + attr_dict[keys] + ', '
		data_str = data_str + statement
	data_statement = data_str.strip(', ')
	new_query = "CREATE TABLE {} ({});".format(table_name, data_statement)
	return new_query

def insertTableJsonQuery(json):
	"""
	This is a helper function that returns the INSERT TABLE statement
	"""
	for column_name in json:
		if (type(json[column_name]) == type({})):
			statement = ''
			for stem in json[column_name]:
				statement = statement + '(' + stem + ', '
				statement = statement + str(json[column_name][stem]) + ', '
				statement = statement + json["run_date"] + '),'
			statement = statement.strip(',')
			insert_query = "INSERT INTO {}(stem_name, numstems, run_date) VALUES {}".format(json["service"], statement)
			return insert_query
	return "There is nothing to insert"

def insertTableQuery(json):
	"""
	This is a helper function that returns the INSERT TABLE statement
	"""
    columnNotDict = []
    value=""
    column = ""
    for obj in json:
        valueNotDict = []
        for column_name in obj:
            if (type(obj[column_name]) != type({})):
                if (column_name not in columnNotDict):
                    columnNotDict.append(column_name)
                valueNotDict.append(obj[column_name])
        for column_name in obj:
            if (type(obj[column_name]) == type({})):
                columnDict = ['stemname', 'numstems']
                for stem in obj[column_name]:
                    combinedValue = valueNotDict.copy()
                    combinedValue.append(stem)
                    combinedValue.append(obj[column_name][stem])
                    value = value + str(tuple(combinedValue)) + ', '
    columnNotDict +=columnDict
    column = str(tuple(columnNotDict))
    value = value.strip(", ")
    table_name = json[0]["name"]
    insert_query = "INSERT INTO {} {} VALUES {};".format(table_name, column, value)
    return insert_query



def updateTableQuery(table_name, attr_dict, condition = None):
	"""
	This is a helper function that returns the UPDATE statement
	"""
	statement = ''
	for keys in attr_dict:
		statement = statement + keys + ' = ' + attr_dict[keys] + ', '
	statement = statement.strip(", ")
	if (condition == ()):
		new_query = "UPDATE {} SET {};".format (table_name, statement)
	else:
		new_query = "UPDATE {} SET {} WHERE {};".format(table_name,statement,condition)
	return new_query

def alterTableQuery(table_name, attr_dict):
	"""
	This is a helper function that returns the ALTER statement
	"""
	key_str = ''
	value_str = ''
	for keys in attr_dict:
		key_str = key_str + keys + ", "
		value_str = value_str + attr_dict[keys] + ", "
	key_statement = key_str.strip(", ")
	value_statement = value_str.strip(", ")
	alter_query = "ALTER TABLE {} ADD {} {};".format(table_name,key_statement, value_statement)
	return alter_query
