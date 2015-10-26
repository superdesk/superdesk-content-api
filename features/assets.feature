Feature: Assets service

    Scenario: Upload a binary file
        When we upload a file "flower.jpg" to "assets" with "562a9f2746e6da5929ca3bae"
        Then we get response code 201

    Scenario: Upload a binary file twice
        When we upload a file "flower.jpg" to "assets" with "562a9f2746e6da5929ca3bae"
        Then we get response code 201
        When we upload a file "flower.jpg" to "assets" with "562a9f2746e6da5929ca3bae"
        Then we get response code 201
