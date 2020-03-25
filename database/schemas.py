from database.db import ma


class CategorySchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')


class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'comment', 'price', 'category_id')
