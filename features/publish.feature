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
    Scenario: Publish an item
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
            "_id": "tag:example.com,0000:newsml_BRE9A605",
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
