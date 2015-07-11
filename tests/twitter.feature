Feature: Twitter Button
    A twitter button to tweet title of and link to post

Scenario: Using the twitter button
    Given I am an authenticated user
    And I have an entry
    And I am on an entry detail page
    When I click on the twitter button
    Then I should be see a new page with the prepared tweet
    
Scenario: Non authenticated twitter button absence
    Given I am not authenticated
    When I go to an entry detail page
    Then I should not see a twitter button
