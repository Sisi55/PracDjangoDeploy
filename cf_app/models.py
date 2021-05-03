# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AllViewUserNumber(models.Model):
    all_view_user_number_id = models.BigIntegerField(primary_key=True)
    user_number = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'all_view_user_number'


class Category(models.Model):
    category_id = models.BigIntegerField(primary_key=True)
    created_date = models.DateTimeField(blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True)
    kurly_id = models.BigIntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'category'


class Coupon(models.Model):
    dtype = models.CharField(max_length=31)
    coupon_id = models.BigIntegerField(primary_key=True)
    created_date = models.DateTimeField(blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True)
    coupon_type = models.CharField(max_length=255, blank=True, null=True)
    discount_rate = models.IntegerField()
    name = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    category_coupon_type = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    category = models.ForeignKey(Category, models.DO_NOTHING, blank=True, null=True)
    product = models.ForeignKey('Product', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'coupon'


class CouponUseUserNumber(models.Model):
    coupon_use_user_number_id = models.BigIntegerField(primary_key=True)
    coupon_type = models.CharField(max_length=255, blank=True, null=True)
    user_number = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'coupon_use_user_number'


class HibernateSequence(models.Model):
    next_val = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hibernate_sequence'


class OrderProduct(models.Model):
    order_product_id = models.BigIntegerField(primary_key=True)
    created_date = models.DateTimeField(blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True)
    count = models.BigIntegerField()
    order_price = models.BigIntegerField()
    order = models.ForeignKey('Orders', models.DO_NOTHING, blank=True, null=True)
    product = models.ForeignKey('Product', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_product'


class Orders(models.Model):
    order_id = models.BigIntegerField(primary_key=True)
    created_date = models.DateTimeField(blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    total_price = models.BigIntegerField()
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orders'


class Payment(models.Model):
    payment_id = models.BigIntegerField(primary_key=True)
    created_date = models.DateTimeField(blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True)
    count = models.BigIntegerField()
    product = models.ForeignKey('Product', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'payment'


class Product(models.Model):
    product_id = models.BigIntegerField(primary_key=True)
    created_date = models.DateTimeField(blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    img_url = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    price = models.IntegerField()
    stock_quantity = models.BigIntegerField()
    category = models.ForeignKey(Category, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product'


class ProductOrderUserNumber(models.Model):
    product_order_user_number_id = models.BigIntegerField(primary_key=True)
    product_id = models.BigIntegerField()
    user_number = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'product_order_user_number'


class ProductTag(models.Model):
    product_tag_id = models.BigIntegerField(primary_key=True)
    created_date = models.DateTimeField(blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True)
    product = models.ForeignKey(Product, models.DO_NOTHING, blank=True, null=True)
    tag = models.ForeignKey('Tag', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_tag'


class ProductViewUserNumber(models.Model):
    product_view_user_number_id = models.BigIntegerField(primary_key=True)
    product_id = models.BigIntegerField()
    user_number = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'product_view_user_number'


class ShopList(models.Model):
    shop_list_id = models.BigIntegerField(primary_key=True)
    created_date = models.DateTimeField(blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True)
    count = models.BigIntegerField()
    product = models.ForeignKey(Product, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shop_list'


class ShopListProduct(models.Model):
    shop_list_product_id = models.BigIntegerField(primary_key=True)
    created_date = models.DateTimeField(blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True)
    count = models.IntegerField()
    shop_list_price = models.IntegerField()
    product = models.ForeignKey(Product, models.DO_NOTHING, blank=True, null=True)
    shop_list = models.ForeignKey(ShopList, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shop_list_product'


class Tag(models.Model):
    tag_id = models.BigIntegerField(primary_key=True)
    created_date = models.DateTimeField(blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tag'


class User(models.Model):
    user_id = models.BigIntegerField(primary_key=True)
    created_date = models.DateTimeField(blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    picture = models.CharField(max_length=255, blank=True, null=True)
    role = models.IntegerField(blank=True, null=True)
    last_activated_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'
