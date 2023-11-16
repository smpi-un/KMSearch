# TBD
import argparse
import json
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class YourTable(Base): # Here replace with your actual model
    __tablename__ = 'your_table'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)
    age = sa.Column(sa.Integer)
    city = sa.Column(sa.String)

# Connect to the database
engine = sa.create_engine('sqlite:///your_database.db') 
Session = sessionmaker(bind=engine)
session = Session()

# Define command line arguments parser
parser = argparse.ArgumentParser()
parser.add_argument("table")
parser.add_argument("conditions", type=json.loads)

args = parser.parse_args()

# Get the relevant model based on the table name
Model = getattr("your_module_containing_the_model", args.table)

# Create a query
query = session.query(Model)

# Apply the conditions from the argument
for field, condition in args.conditions.items():
    if condition.startswith(">"):
        query = query.filter(getattr(Model, field) > condition[1:])
    elif condition.startswith("<"):
        query = query.filter(getattr(Model, field) < condition[1:])
    elif condition.startswith("LIKE"):
        query = query.filter(getattr(Model, field).like(condition[4:]))
    else:
        query = query.filter(getattr(Model, field) == condition)

# Run the query and print the results
results = query.all()
for result in results:
    print(result)
# ... (前述と同様の部分は省略します) ...

# Define command line arguments parser
parser = argparse.ArgumentParser()
parser.add_argument("table")
parser.add_argument("and_conditions", type=json.loads)
parser.add_argument("or_conditions", type=json.loads)

args = parser.parse_args()

# Get the relevant model based on the table name
Model = getattr(your_module_containing_the_model, args.table)

# Create a query
query = session.query(Model)

# Apply the And conditions
for clause in args.and_conditions:
    for field, condition in clause.items():
        if condition.startswith(">"):
            query = query.filter(getattr(Model, field) > condition[1:])
        elif condition.startswith("<"):
            query = query.filter(getattr(Model, field) < condition[1:])
        elif condition.startswith("LIKE"):
            query = query.filter(getattr(Model, field).like(condition[4:]))
        else:
            query = query.filter(getattr(Model, field) == condition)

# Apply the Or conditions in a single filter
or_conditions = []
for clause in args.or_conditions:
    for field, condition in clause.items():
        if condition.startswith(">"):
            or_conditions.append(getattr(Model, field) > condition[1:])
        elif condition.startswith("<"):
            or_conditions.append(getattr(Model, field) < condition[1:])
        elif condition.startswith("LIKE"):
            or_conditions.append(getattr(Model, field).like(condition[4:]))
        else:
            or_conditions.append(getattr(Model, field) == condition)

query = query.filter(sa.or_(*or_conditions))

# Run the query and print the results
results = query.all()
for result in results:
    print(result)