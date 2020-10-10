from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, types, Boolean, Table
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    """Model for a Base User"""

    __tablename__ = 'users'
    __table_args__ = {'sqlite_autoincrement': True}
    # __user_attributes__ = ["gender"]

    id = Column(Integer, primary_key=True)
    name = Column(String)
    gender = Column(String)

    # relationships
    order = relationship('Order', back_populates='user')
    preference = relationship('UserPreference', back_populates='user', uselist=False)


class UserPreference(Base):
    """Model for user preferences"""

    __tablename__ = 'user_preference'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    rest = Column(Integer, ForeignKey("restaurants.name"))
    food = Column(Integer, ForeignKey("dishes.name"))

    # relationship
    user = relationship('User', back_populates='preference')


association_table = Table(
    'association',
    Base.metadata,
    Column('dishes_id', Integer, ForeignKey('dishes.id')),
    Column('restaurants_id', Integer, ForeignKey('restaurants.id')),
)


class Dish(Base):
    """Model for Dish"""

    __tablename__ = "dishes"
    __table_args__ = {'sqlite_autoincrement': True}

    id = Column(Integer, primary_key=True)
    name = Column(String)
    is_veg = Column(Boolean)

    # relationship
    restaurants = relationship('Restaurant', secondary=association_table, back_populates='dishes')


class Restaurant(Base):
    """Model for Restaurant"""

    __tablename__ = "restaurants"
    __table_args__ = {'sqlite_autoincrement': True}

    id = Column(Integer, primary_key=True)
    name = Column(String)

    # relationships
    orders = relationship('Order', back_populates='restaurant')
    dishes = relationship('Dish', secondary=association_table, back_populates='restaurants')


class Order(Base):
    """Model for Order"""

    __tablename__ = "orders"
    __table_args__ = {'sqlite_autoincrement': True}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))

    # relationships
    user = relationship('User', back_populates='order')
    restaurant = relationship('Restaurant', back_populates='orders')


class Segment(Base):
    """Model for Segment"""

    __tablename__ = "segments"
    __table_args__ = {'sqlite_autoincrement': True}

    id = Column(Integer, primary_key=True)
    name = Column(String)
    config = Column(types.JSON())
