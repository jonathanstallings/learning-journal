import pytest
from pytest_bdd import scenario, given, when, then


@given('a learning journal home page')
def homepage_exists(homepage):
    pass


@scenario('permalink.feature', 'Viewing an entry by permalink')
def test_view_permalink():
    pass


@given('I have an entry')
def entry_exists(app, entry):
    response = app.get('/')
    actual = response.body
    expected = 'class="entry-link"'
    assert expected in actual
    return dict(entry=entry, response=response)


@when('I click on an entry title')
def click_on_entry_title(app, entry_exists):
    entry = entry_exists['entry']
    response = app.get('/detail/{id}'.format(id=entry.id))
    assert response.status_code == 200
    entry_exists['response'] == response


@then('I should should see the entry detail')
def see_entry_detail(entry_exists):
    response = entry_exists['response']
    entry = entry_exists['entry']
    actual = response.body
    expected = entry.title
    assert expected in actual


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
