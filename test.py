from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models.food import Food
from models.category import Category

Base = declarative_base()

engine = create_engine('sqlite:///database')

Base.metadata.create_all(engine)

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
db = DBSession()


new_food = Food(name='Pizza Paperos', description='My food', price=29, image='asdasd', category_id=2)
new_category = Category(name='Bif Burger')
new_category1 = Category(name='Sup')
new_category2 = Category(name='Pizaa')

#db.add(new_category)
#db.add(new_category1)
#db.add(new_category2)

#db.commit()

#.filter_by(category_id=1)

Base.metadata.drop_all(engine)

foods = db.query(Food).filter_by(category_id=2).all()
categorys_pizza = db.query(Category).all()

print(foods)
print(categorys_pizza)


