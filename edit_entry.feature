Feature: Edit Entry
    A view allowing editing entries

Scenario: Viewing an entry by permalink
    Given I'm an authenticated user
    And I have an entry
    When I go to the home page
    And I click on an entry title
    Then I should not see an error message
    And I should should be redirected to entry detail

Scenario: Editing an entry
    Given I'm an authenticated user
    And I have an entry
    When I go to an entry detail page
    And I click on the edit button
    Then I should be shown an edit view





    As an author I want to have a permalink for each journal entry where I can view it in detail.
    As an author I want to edit my journal entries so I can fix errors.
    As an author I want to use MarkDown to create and edit my entries so that I can format them nicely.
    As an author I want to see colorized code samples in my journal entries so that I can more easily understand them.
