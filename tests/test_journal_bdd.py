import pytest
from pytest_bdd import scenario, given, when, then


@given('a learning journal home page')
def home_page_exits(app):
    response = app.get('/')
    assert response.status_code == 200
    return response


@scenario('permalink.feature', 'Viewing an entry by permalink')
def test_view_permalink(app, entry):
    pass


@given('I have an entry')
def entry_exists(app, entry):
    # response = app.get('/')
    # actual = response.body
    # expected = "class='entry-link'"
    # assert expected in actual
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
def test_invalid_permalink(app):
    pass


@given('I do not have an entry')
def entry_not_exists(app):
    pass


@when('I request a permalink')
def request_permalink():
    pass


@then('I should receive a 404 error')
def receive_404():
    pass
