import factory
from django.contrib.auth import get_user_model
from website import models

User = get_user_model()

class LanguageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Language

    name = factory.Sequence(lambda n: f"Language {n}")

class LevelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Level

    code = factory.Sequence(lambda n: f"A{n}")
    description = "Lorem ipsum"
    study = factory.Sequence(lambda n: n)
    hierarchy = factory.Sequence(lambda n: n)


class OrganisationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Organisation

    name = factory.Sequence(lambda n: f"Org {n}")
    domain = factory.Sequence(lambda n: f"org{n}.sfl.ai")
    language = factory.SubFactory(LanguageFactory)

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True

    username = factory.Sequence(lambda n: f"user{n}")
    password = factory.PostGenerationMethodCall('set_password', 'password')
    organisation = factory.SubFactory(OrganisationFactory)

class PromptFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Prompt

    title = "Sample Prompt"
    user = factory.SubFactory(UserFactory)
    level = factory.SubFactory(LevelFactory)
    language = factory.SubFactory(LanguageFactory)
