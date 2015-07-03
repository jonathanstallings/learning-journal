import pytest
from pytest_bdd import scenario, given, when, then


@scenario('permalink.feature', 'Viewing an entry by permalink')
def test_view_permalink():
    pass


@given('I have an entry')
def auth_user():
    pass


@when('I click on an entry title')
def click_on_entry_title():
    pass


@then('I should not see an error message')
def no_error_messages():
    pass


@then('I should should see the entry detail')
def see_entry_detail():
    pass
