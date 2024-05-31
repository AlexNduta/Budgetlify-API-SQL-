#!/usr/bin/python3

from fastapi import FastAPI, HTTPException, status
import json
from pydantic import BaseModel, ValidationError
from random import randrange
from typing import List
import uuid
import psycopg2 # for working with postgresql
from psycopg2.extras import RealDictCursor # for giving columnname and value
#from schemas import Post 
import schemas
from typing import Any
import utils

app = FastAPI()


# as long as we are not able to connect to the DB, loop endlesly
while True:
    try:
        # connecting to the Database using psycopg2
        # pass requirements
        conn = psycopg2.connect(host='localhost',
                                database='Budgelify', 
                                user='was', 
                                password='123', 
                                cursor_factory=RealDictCursor)
        # We use the cursor to execute SQL commands
        # example: cursor.Execute('SQL commands go here')
        cursor= conn.cursor()
        print("succesfully connected to the DB")
        break # break from the loop when we are able to connect to the DB
    except Exception as error:

        print("Unable to connect to the db")



        print('Error:', error)


@app.get("/Budgetlify/expenses")
def get_expenses():
    """ get a list of all our expenses saved somewhere in the file/DB"""
   # expenses = expense_file_reader(filename)
   # execute SQL statements in our code
    cursor.execute("""SELECT * FROM Expenses""")
    expenses = cursor.fetchall() # get all items from the database
    return expenses 


@app.post("/Budgetlify/expenses", status_code=status.HTTP_201_CREATED)
def post_expense(new_expense: schemas.PostCreate): 
    """ Creates a post and sends data to the URL provided 
        - new_post:
                category: food
                date: Auto provisioned by DB
                amount: 
                Description:
                id: auto provided by DB
    """

    try:
        # use cursor object to execute SQL statements   
        cursor.execute("""INSERT INTO expenses(category, amount, Description) VALUES(%s, %s, %s) RETURNING *""", (new_expense.category, new_expense.amount, new_expense.description))
        new_expense_posted = cursor.fetchone() # get the values posted in the SQL statement above
        conn.commit() # save the data to the database

        # Create a response object that will return the items we want 
        # we ue this because we are not using ORM
        response = schemas.PostResponse(
            category= new_expense_posted['category'],
            amount=new_expense_posted['amount'],
            description= new_expense_posted['description']
        )
        return response.dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occured : {}".format(e))


@app.get("/Budgetlify/expenses/{id}")
def get_single_item(id:int):
    """ gets a single item from the list of expenses
        with the specified ID"""
    cursor.execute("""SELECT * FROM expenses WHERE id = %s""", (str(id),)) # make sure to covert the passed ID to astring
    fetched_item = cursor.fetchone() # get that one item from the list
    # confirm if we were able to get the item else, raise an error
    if fetched_item:
        return fetched_item
    else:
        raise HTTPException(status_code=404, detail="The item with the ID {} is not found".format(id) )


def index_finder(id:int):
    """ returns an index of the item from the list. 
        used by the delete HTTP method
    """
    # call the function that returns a list
    list_of_expenses = expense_file_reader(filename)
    for index, element in enumerate(list_of_expenses):
        if element['id'] == id:
            return index


@app.delete("/Budgetlify/expenses/{id}")
def delete_a_single_item(id:int):
    """
    deletes an item specified by ID from the list
    """
    # use cursor to execute SQL statements
    cursor.execute("""DELETE FROM expenses WHERE id = %s returning *""", (str(id),))
    deleted_post = cursor.fetchone() # delete the specified item
    conn.commit() # make changes to the database

    # confirm if the item exists
    if deleted_post is None:
        raise HTTPException(status_code=404, detail="Expense with ID {} not found".format(id))

    return {"message":"Item deleted successfully"}


@app.put("/Budgetlify/expenses/{id}")
def update_expense(id:int, post: schemas.PostCreate):
    """ updates existing items with user changes in the list maintaining the id"""


    #  use the cursor to execute the SQL statements
    cursor.execute("""UPDATE expenses SET category=%s, amount=%s, description=%s WHERE id=%s returning *""", (post.category, post.amount, post.description, str(id)))
    updated_expense = cursor.fetchone()
    conn.commit()
    if updated_expense:
        return {"message": "expense updated successfuly"}

    else:
        raise HTTPException(status_code=404, detail="expense with ID: {} does not exist")

@app.post("/Budgetlify/users", status_code=status.HTTP_201_CREATED)
def create_user(new_user: schemas.CreateUser):
    """ used to create users to out table of users

    - Our new user willl have a name, email and password
    """
    # hash the password - new_user.password
    hashed_password = utils.hash(new_user.password)
    try:
        # we will use the cursor object to execute our SQL code
        cursor.execute("""INSERT INTO users(name, email, password) VALUES(%s, %s, %s) RETURNING *""", (new_user.name, new_user.email, hashed_password))
        new_user = cursor.fetchone() # get the values we just posted
        conn.commit()# save our values to the database
        # specify what to return  to the user, make sure that we do not return the password
        response = schemas.UserResponse(
                name = new_user['name'],
                email = new_user['email'],
        )
        return response.dict()
        #return new_user
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occured : {}".format(e))

@app.get("Budgetlify/users")
def get_user():
    #cursor.execute("""SELECT * FROM users WHERE id = %s """, (str(id),)) 
    cursor.execute("""SELECT * FROM users""") 
    fetched_user = cursor.fetchall()
    return fetched_user
"""
    if fetched_user:
        return fetched_user
    else:
        raise HTTPException(status_code=404, detail="The user  with the ID {} is not found".format(id)) """
