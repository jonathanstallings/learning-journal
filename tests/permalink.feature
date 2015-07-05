Feature: Entry Permalink
    A detail view of a single entry

Background:
    Given a learning journal home page

Scenario: Viewing an entry by permalink
    Given I have an entry
    When I click on an entry title
    Then I should should see the entry detail

    
