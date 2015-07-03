Feature: Entry Permalink
    A detail view of a single entry

Background:
    Given a learning journal home page

Scenario: Viewing an entry by permalink
    Given I have an entry
    When I click on an entry title
    Then I should not see an error message
    And I should should be redirected to entry detail

Scenario: Entering an invalid permalink
    Given I do not have an entry
    When I request a permalink
    Then I should receive a 404 error
    
