import factory


class UserFactory(factory.django.DjangoModelFactory):
    
    class Meta:
        model = "users.User"
    
    id = factory.Factory('uuid4')
    email = factory.Faker('email')
    password = factory.Faker('password', length=10, special_chars=True, digits=True,
                             upper_case=True, lower_case=True)
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_active = True
    is_staff = False