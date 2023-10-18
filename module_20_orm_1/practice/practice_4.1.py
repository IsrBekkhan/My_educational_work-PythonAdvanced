from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from flask import Flask, jsonify, abort, request
from typing import Dict, Any

app = Flask(__name__)
engine = create_engine('sqlite:///sqlite_python.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    count = Column(Integer, default=0)
    price = Column(Float, default=0)

    def __repr__(self):
        return f"Товар {self.title}, в количестве: {self.count}, цена: " \
               f"{self.price}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}


@app.before_request
def before_request_func():
    Base.metadata.create_all(engine)


@app.route('/products', methods=['GET'])
def get_all_products():
   """Получение списка товаров на складе"""
   products = session.query(Product).all()
   products_list = []
   for product in products:
       product_as_dict = product.to_json()
       products_list.append(product_as_dict)
   return jsonify(products_list=products_list), 200


@app.route('/product/<int:id>', methods=['GET'])
def get_product(id):
   """Получение товара по id"""
   product = session.query(Product).filter(Product.id == id).one_or_none()
   if product is None:
       abort(404)
   return jsonify(product=product.to_json()), 200


@app.route('/products', methods=['POST'])
def add_product():
   """Добавить новый товар на склад"""
   title = request.form.get('title', type=str)
   count = request.form.get('count', type=int)
   price = request.form.get('price', type=float)
   new_product = Product(title=title, count=count, price=price)
   session.add(new_product)
   session.commit()
   return 'Товар успешно создан', 201


app.route('/product/<int:id>', methods=['PATCH'])
def update_product(id):
   """Обновить товар на складе"""
   title = request.form.get('title', type=str)
   count = request.form.get('count', type=int)
   price = request.form.get('price', type=float)
   product = session.query(Product).filter(Product.id == id).one_or_none()
   if title:
       product.title = title
   if count:
       product.count = count
   if price:
       product.price = price
   session.commit()
   # # 2 вариант UPDATE
   # session.query(Product).filter(Product.id == id)\
   #     .update({Product.title:title,
   #              Product.count:count,
   #              Product.price:price})
   ## 3 вариант UPDATE
   # from sqlalchemy import update
   # query = update(Product).where(Product.id == id).values(title=title,
   #                                                        count=count,
   #                                                        price=price)
   # print(query)
   # session.execute(query)
   return 'Товар успешно обновлен', 200


@app.route('/product/<int:id>', methods=['DELETE'])
def delete_product(id):
   """Убрать товар со склада"""
   # с помощью метода объекта Query
   session.query(Product).filter(Product.id == id).delete()
   session.commit()
   # # используя специальную конструкцию delete
   # from sqlalchemy import delete
   # query = delete(Product).where(Product.id == id)
   # session.execute(query)
   return 'Товар успешно удален', 200


if __name__ == '__main__':
    app.run()