# Import necessary modules
import graphene
from graphene_django.types import DjangoObjectType
from .models import BrickCategory, BrickProduct, ProductAttribute, Sale, BrickStock

# Define GraphQL types for each Django model
class BrickCategoryType(DjangoObjectType):
    class Meta:
        model = BrickCategory

class BrickProductType(DjangoObjectType):
    product_img_display = graphene.String()

    class Meta:
        model = BrickProduct

    def resolve_product_img_display(self, info):
        return self.product_img_display()

class ProductAttributeType(DjangoObjectType):
    class Meta:
        model = ProductAttribute

class SaleType(DjangoObjectType):
    class Meta:
        model = Sale

class BrickStockType(DjangoObjectType):
    class Meta:
        model = BrickStock

# Define Query for fetching data
class Query(graphene.ObjectType):
    all_brick_categories = graphene.List(BrickCategoryType)
    all_brick_products = graphene.List(BrickProductType)
    all_product_attributes = graphene.List(ProductAttributeType)
    all_sales = graphene.List(SaleType)
    all_brick_stocks = graphene.List(BrickStockType)

    def resolve_all_brick_categories(self, info):
        return BrickCategory.objects.all()

    def resolve_all_brick_products(self, info):
        return BrickProduct.objects.all()

    def resolve_all_product_attributes(self, info):
        return ProductAttribute.objects.all()

    def resolve_all_sales(self, info):
        return Sale.objects.all()

    def resolve_all_brick_stocks(self, info):
        return BrickStock.objects.all()

# Define mutations for creating new instances
class CreateBrickCategory(graphene.Mutation):
    class Arguments:
        name = graphene.String()

    brick_category = graphene.Field(BrickCategoryType)

    def mutate(self, info, name):
        brick_category = BrickCategory(name=name)
        brick_category.save()
        return CreateBrickCategory(brick_category=brick_category)

class CreateBrickProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        category_id = graphene.ID()
        description = graphene.String()
        product_image = graphene.String()
        product_code = graphene.String()

    brick_product = graphene.Field(BrickProductType)

    def mutate(self, info, name, category_id, description, product_image, product_code):
        category = BrickCategory.objects.get(pk=category_id)
        brick_product = BrickProduct(
            name=name,
            category=category,
            description=description,
            product_image=product_image,
            product_code=product_code
        )
        brick_product.save()
        return CreateBrickProduct(brick_product=brick_product)

# Define Mutation for adding new instances
class Mutation(graphene.ObjectType):
    create_brick_category = CreateBrickCategory.Field()
    create_brick_product = CreateBrickProduct.Field()

# Define schema
schema = graphene.Schema(query=Query)
