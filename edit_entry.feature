Feature: Edit Entry
    A view allowing editing entries

Background:
    Given a learning journal home page
    And I have an entry

Scenario: Entering edit view
    Given I am an authenticated user
    When I go to an entry detail page
    And I click on the edit button
    And I modify the text
    And I click on the save button
    Then I should be shown an edit view

Scenario: Modifying an entry
    Given I am an authenticated user
    And I modify text in edit view
    When I click the save button
    Then I should see my changes to the entry

Scenario: Non authenticated detail view
    Given I am not authenticated
    When I go to an entry detail page
    Then I should not see an edit button

Scenario: Non authenticated edit request
    Given I am not authenticated
    When I send an edit request
    Then I should be redirected to login page
