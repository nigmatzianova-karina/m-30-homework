from sqlalchemy import Column, Integer, String, ARRAY

from database import Base

class Recipe(Base):
    __tablename__ = "Recipe"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    cook_time = Column(Integer, index=True)
    list_of_ingredients = Column(String, index=True)
    description = Column(String, index=True)
    count_of_view = Column(Integer, index=True, default=0,)


# {
#     "name": "Pancake",
#     "cook_time": 15,
#     "list_of_ingredients": "Milk, eggs, sugar",
#     "description": "Yammy!"
# }
