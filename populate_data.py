from db_utils.models import User, Dish, Restaurant, Order, Segment, UserPreference
from db_utils.session_factory import SessionFactory

session_fact = SessionFactory()

with session_fact.session_scope() as session:
    user = User(name="Piyush", gender="male")
    session.add(user)
    session.flush()

    dish = Dish(name="red-meat", is_veg=False)
    session.add(dish)

    restaurant = Restaurant(name="Restaurant1")
    restaurant.dishes.append(dish)
    session.add(restaurant)

    order = Order(user_id=user.id, restaurant_id=restaurant.id)
    session.add(order)

    user_pref = UserPreference(user_id=user.id, rest=restaurant.name, food=dish.name)
    session.add(user_pref)

    # segment 1
    config = {
        "gender": {
            "operator": "neq",
            "value": "female"
        }
    }
    segment = Segment(name="segment1", config=config)
    session.add(segment)

    # segment 2
    config = {
        "gender": {
            "operator": "neq",
            "value": "female"
        },
        "or": [
            {"preference.food": {
                "operator": "eq",
                "value": "red-meat"
            }},
            {"order_count": {
                "operator": "gt",
                "value": 1
            }}
        ]
    }
    segment = Segment(name="segment2", config=config)
    session.add(segment)

    # segment 3
    config = {
        "gender": {
            "operator": "neq",
            "value": "female"
        },
        "and": [
            {"preference.food": {
                "operator": "eq",
                "value": "red-meat"
            }},
            {"order_count": {
                "operator": "gte",
                "value": 1
            }}
        ]
    }
    segment = Segment(name="segment3", config=config)
    session.add(segment)

    # segment 4
    config = {
        "gender": {
            "operator": "neq",
            "value": "female"
        },
        "and": [
            {"preference.food": {
                "operator": "eq",
                "value": "red-meat"
            }},
            {"order_count": {
                "operator": "gt",
                "value": 1
            }}
        ]
    }
    segment = Segment(name="segment4", config=config)
    session.add(segment)



