## Project Details
This project is to segment a given user into different groups
based on predefined configuration.

## Requirements
Python with sqlalchemy
sqlite3

## Directory Structure
- db_utils : contains DB utilities, `SessionFactory` being the actual interface.
contains relevant models and relationships.
- segmentation : contains segmentation utils, `Segmentation` being the actual interface.
- main.py : entry point to segment a user
- db.sqlite3 : text db with prepopulated data

## How to use?
##### Not from scratch
- Install python and run `pip install -r requirements.txt`
- Data is prepopulated into db.sqlite3
- Run main.py to get segment classification for pre populated user `python main.py`

##### From scratch
- Install python and run `pip install -r requirements.txt`
- Delete db.sqlite3
- Edit populate_data.py to add users, restaurants, user preferences,
orders, dishes, etc. 
- Run populate_data.py to populate data into database  `python populate_data.py`
- Edit main.py file to query user you want to get segments for
- RUn main.py to get a list of segments this user belongs to `python main.py`

## Code Design and classes
- `db_utils/connection.py/Connection` :: to connect to actual DB
- `db_utils/session_factory.py/SessionFactory` :: handles provisioning a connection, committing, 
rolling back and closing the connection
- `db_utils/models.py` :: database models (User, Dish, Restaurant, Order, UserPreference)
- `segmentation/operators.py/Operator` :: defines different operators that will 
be used in the rule based configuration 
- `segmentation/segmentation.py/Segmentation` :: contains all utility functions for segmentation.
    - `__init__`: initialise session, register operators, get all segments from database
    - `get_user_segments` : get all segments that the user falls into
    - `flatten_details` : flatten user details to ease out the user details to segment config matching
    - `_resolve_seg_pref` : resolve a section in config which is not an operation but an attribute to check for
    - `__resolve_seg_ope` : resolve a section in config which is an operation like or/and
    
## Algorithm
- Store all segments with respective config to database
- To get segments for a user, get the user details and flatten them.
- Next, pass the user details through every segment to check if it satisfies.
- Satisfaction algorithm:
    Recursively,
    - If section is an operation like or/and, pass it through `_resolve_seg_ope`
    - If not, pass it through `resolve_seg_pref`

