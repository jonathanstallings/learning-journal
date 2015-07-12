Feature: Twitter Button
    A twitter button to tweet title of and link to post

Scenario: Using the twitter button
    Given I am an authenticated user
    And I am on an entry detail page
    Then I should have a prepared twitter link
    
Scenario: Non authenticated twitter button absence
    Given I am not authenticated
    When I go to an entry detail page
    Then I should not see a twitter button
