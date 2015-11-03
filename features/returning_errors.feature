Feature: Returning error on invalid request parameters

	@auth
    Scenario: Sending an unknown parameter when retrieving items
        When we get "/items?parameter_x=foo"
        Then we get error 422
        """
        {
            "internal_error": 10001,
            "_message": "Unexpected parameter.",
            "_status": "ERR",
            "_issues": "Unexpected parameter (parameter_x)"
        }
        """

	@auth
    Scenario: Sending an unknown parameter when retrieving packages
        When we get "/packages?parameter_x=foo"
        Then we get error 422
        """
        {
            "internal_error": 10001,
            "_message": "Unexpected parameter.",
            "_status": "ERR",
            "_issues": "Unexpected parameter (parameter_x)"
        }
        """

	@auth
    Scenario: Trying to apply filters when fetching a single item
        When we get "/items/someItemId?q={\"language\": \"en\"}"
        Then we get error 422
        """
        {
            "internal_error": 10001,
            "_issues": "Filtering is not supported when retrieving a single object (the \"q\" parameter)",
            "_status": "ERR",
            "_message": "Unexpected parameter."
        }
        """

	@auth
    Scenario: Trying to apply filters when fetching a single package
        When we get "/packages/somePackageId?q={\"language\": \"en\"}"
        Then we get error 422
        """
        {
            "internal_error": 10001,
            "_issues": "Filtering is not supported when retrieving a single object (the \"q\" parameter)",
            "_status": "ERR",
            "_message": "Unexpected parameter."
        }
        """
