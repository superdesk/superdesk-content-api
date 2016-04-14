Feature: Publish service

    Scenario: Publish an item without authentication
    	When we post to "/publish"
    	"""
    	[{
            "guid": "tag:example.com,0000:newsml_BRE9A605",
            "type": "picture",
            "headline": "lorem ipsum",
            "versioncreated": "2014-03-16T06:49:47+0000",
            "language": "en",
            "mimetype": "text/plain",
            "pubstatus": "usable",
            "version": "1"
    	}]
    	"""
        Then we get response code 201

    Scenario: Create a client and a user without authentication
    	When we post to "/clients"
    	"""
    	[{
            "name": "client1",
            "client_type": "subscriber"
    	}]
    	"""
        Then we get response code 201
    	When we post to "/users"
    	"""
    	[{
            "username": "username1",
            "password": "password1",
            "client": "#clients._id#"
    	}]
    	"""
        Then we get response code 201

	@auth
    Scenario: Publish an item with success
    	When we post to "/publish"
    	"""
    	[{
            "guid": "tag:example.com,0000:newsml_BRE9A605",
            "type": "picture",
            "headline": "lorem ipsum",
            "versioncreated": "2014-03-16T06:49:47+0000",
            "language": "en",
            "mimetype": "text/plain",
            "pubstatus": "usable",
            "version": "1"
    	}]
    	"""
        Then we get response code 201

        When we get "/items?start_date=2014-03-16"
        Then we get list with 1 items

    Scenario: Publish an item with error
    	When we post to "/publish"
    	"""
    	[{
            "guid": "tag:example.com,0000:newsml_BRE9A605",
            "type": "picture",
            "headline": "lorem ipsum",
            "versioncreated": "2014-03-16T06:49:47+0000",
            "language": "en",
            "mimetype": "text/plain",
            "pubstatus": "usable",
            "versions": "1"
    	}]
    	"""
        Then we get error 422
        """
        {
        	"_issues": { "versions": "unknown field" },
        	"_error": {"code": 422, "message": "Insertion failure: 1 document(s) contain(s) error(s)"},
        	"_status": "ERR"
        }
        """

	@auth
	Scenario: Publish a package containing items
		Given empty "items"
		When we post to "publish"
		"""
		[{
            "language": "en",
            "byline": "first name last name",
            "guid": "urn:newsml:localhost:2016-03-17T17:07:01.639259:5dd14b97-a15d-41b6-aee7-ae9b3948345a",
            "pubstatus": "usable",
            "version": "2",
            "versioncreated": "2016-03-17T15:07:02+0000",
            "urgency": 2,
            "priority": 1,
            "slugline": "PACKAGE2 SLUGLINE",
            "headline": "package2",
            "type": "composite",
            "associations": {
                "main": [
                    {
                    	"guid": "item5",
                        "headline": "item5",
                        "urgency": 1,
                        "guid": "urn:newsml:localhost:2016-03-17T17:07:00.093304:8089015f-a7d7-494f-9b68-13829ab34366",
                        "body_html": "<p>item5 text</p>",
                        "language": "en",
                        "byline": "Billy The Fish",
                        "pubstatus": "usable",
                        "version": "2",
                        "versioncreated": "2016-03-17T15:07:00+0000",
                        "slugline": "item5 slugline one/two",
                        "priority": 6,
                        "type": "composite"
                    }
                ],
                "story": [
                    {
                    	"guid": "item9",
                        "headline": "item9",
                        "urgency": 1,
                        "guid": "urn:newsml:localhost:2016-03-17T17:07:01.639259:5dd14b97-a15d-41b6-aee7-ae9b3948792f",
                        "body_html": "<p>item9 text</p>",
                        "language": "en",
                        "byline": "first name last name",
                        "pubstatus": "usable",
                        "version": "2",
                        "versioncreated": "2016-03-17T15:07:02+0000",
                        "slugline": "item9 slugline",
                        "priority": 6,
                        "type": "composite"
                    }
                ]
            }
		}]
		"""
        Then we get response code 201
        When we get "/packages?start_date=2016-03-17"
        Then we get list with 3 items
