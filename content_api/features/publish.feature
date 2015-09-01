Feature: Publish service

    Scenario: Publish an item
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
            "version": "1"
    	}]
    	"""
        Then we get response code 201

        When we get "/items?start_date=2014-03-16"
        Then we get list with 1 items
        """
        {
        	"_items": [
        		{
		            "type": "picture",
		            "headline": "lorem ipsum",
		            "versioncreated": "2014-03-16T06:49:47+0000",
		            "language": "en",
		            "mimetype": "text/plain",
		            "pubstatus": "usable",
		            "version": "1"
	            }
	        ]
        }
        """

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
