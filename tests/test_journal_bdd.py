# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pytest
from pytest_bdd import scenario, given, when, then

from test_journal import login_helper


INPUT_BTN = '<input type="submit" value="Share" name="Share"/>'
ADD_ENTRY = '<h3>Add Entry</h3>'


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


@scenario('edit_entry.feature', 'Entering edit view')
def test_enter_edit_mode():
    pass


@given('I am an authenticated user')
def is_authenticated(app, entry):
    username, password = ('admin', 'secret')
    redirect = login_helper(username, password, app)
    assert redirect.status_code == 302
    response = redirect.follow()
    assert response.status_code == 200
    actual = response.body
    assert ADD_ENTRY in actual


@given('I am on an entry detail page')
def entry_detail_page(app, entry):
    response = app.get('/detail/{id}'.format(id=entry.id))
    return dict(response=response, entry=entry)


@when('I click on the edit button')
def click_edit_button(entry_detail_page):
    response = entry_detail_page['response']
    clicked = response.click(linkid='edit-button')
    entry_detail_page['response'] = clicked


@then('I should be shown an edit view')
def edit_view(entry_detail_page):
    response = entry_detail_page['response']
    actual = response.body
    expected = '<h3>Edit Entry</h3>'
    assert expected in actual


@scenario('edit_entry.feature', 'Modifying an entry')
def test_modify_entry():
    pass


@given('I have an edit view')
def edit_mode_view(app, entry):
    response = app.get('/detail/{id}'.format(id=entry.id))
    clicked = response.click(linkid='edit-button')
    return dict(response=clicked)


@when('I modify text in edit view')
def modify_text(edit_mode_view):
    response = edit_mode_view['response']
    form = response.form
    form.fields['text'][0].value += ' some changes'
    edit_mode_view['response'] = response


@when('I click the save button')
def click_save_button(edit_mode_view):
    response = edit_mode_view['response']
    redirected = response.form.submit()
    response = redirected.follow()
    edit_mode_view['response'] = response


@then('I should see my changes to the entry')
def see_changes(edit_mode_view):
    response = edit_mode_view['response']
    actual = response.body
    expected = 'some changes'
    assert expected in actual


@scenario('edit_entry.feature', 'Non authenticated detail view')
def test_non_auth_detail_view():
    pass


@given('I am not authenticated')
def not_auth(app, entry):
    response = app.get('/')
    return dict(response=response, entry=entry)


@when('I go to an entry detail page')
def vist_entry_detail(app, not_auth):
    entry = not_auth['entry']
    response = app.get('/detail/{id}'.format(id=entry.id))
    not_auth['response'] = response


@then('I should not see an edit button')
def no_edit_button(not_auth):
    response = not_auth['response']
    actual = response.body
    edit_button = 'id="edit-button"'
    assert edit_button not in actual


@scenario('edit_entry.feature', 'Non authenticated edit request')
def test_non_auth_edit_request():
    pass


@when('I send an edit request')
def send_edit_request(app, entry, not_auth):
    response = app.post('/edit/{id}'.format(id=entry.id),
        {
            'submit': True,
            'title': 'You got hacked',
            'text': 'Protect from non-AuthN POST requests!'
        }
    )
    not_auth['response'] = response


@then('I should be redirected to login page')
def redirect_login(not_auth):
    redirect = not_auth['response']
    response = redirect.follow()
    actual = response.body
    expected = "<h3>Login</h3>"
    assert expected in actual


@scenario('twitter.feature', 'Using the twitter button')
def test_authn_twitter_button():
    pass


@then('I should have a prepared twitter link')
def view_tweet_page(entry_detail_page):
    """Tesing this way because of lack of Twitter AuthN cookie."""
    response = entry_detail_page['response']
    entry = entry_detail_page['entry']
    soup = response.html
    twitter_button = soup.find('a', {'id': 'twitter-button'})
    href = twitter_button.attrs['href']
    expected = [
        entry.title,
        entry.id,
        'twitter.com'
    ]
    for item in expected:
        assert unicode(item) in href


@scenario('twitter.feature', 'Non authenticated twitter button absence')
def test_non_authn_twitter_button():
    pass


@then('I should not see a twitter button')
def no_twitter_button(not_auth):
    response = not_auth['response']
    soup = response.html
    twitter_button = soup.find('a', {'id': 'twitter-button'})
    assert twitter_button is None
