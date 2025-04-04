import pytest
from website.tests.factories import OrganisationFactory, UserFactory, PromptFactory, LanguageFactory

@pytest.mark.django_db
def test_create_user_with_organisation():
    user = UserFactory()
    org = user.organisation

    assert user.organisation == org
    assert user.username.startswith("user")
    assert user.check_password("password") is True

@pytest.mark.django_db
def test_prompt_creation_sets_user():
    prompt = PromptFactory(title="Bonjour!")

    assert prompt.user.username.startswith("user")
    assert prompt.language.name.startswith("Language")
    assert prompt.title == "Bonjour!"
