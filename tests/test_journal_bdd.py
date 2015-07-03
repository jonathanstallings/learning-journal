import pytest
from pytest_bdd import scenario, given, when, then


@given('a learning journal home page')
def home_page_exits():
    pass


@scenario('permalink.feature', 'Viewing an entry by permalink')
def test_view_permalink():
    pass


@given('I have an entry')
def entry_exists():
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


@scenario('permalink.feature', 'Entering an invalid permalink')
def test_invalid_permalink():
    pass


@given('I do not have an entry')
def entry_not_exists():
    pass


@when('I request a permalink')
def request_permalink():
    pass


@then('I should receive a 404 error')
def receive_404():
    pass
