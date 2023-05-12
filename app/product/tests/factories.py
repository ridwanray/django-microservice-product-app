import factory
from faker import Faker
from product.models import Product

fake = Faker()


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = fake.first_name()
    description = fake.text()
