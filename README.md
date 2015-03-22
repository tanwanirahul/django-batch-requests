Django Batch Requests
=========================

[![build-status-image]][travis]
[![pypi-version]][pypi]
[![coverage]][coverage-repo]

Django batch requests allow developers to combine multiple http requests into a single batch request. This is essentially useful to avoid making multiple http requests.

Its built on top of Django and relies on Django's URL dispatching, hence it could also be used with any web framework built on top of Django such as [Django Rest Framework].

# Requirements

* Python (2.7)
* Django (1.7)

# Installation

Install using `pip`...

    pip install django-batch-requests

Install from source...

    python setup.py install


# Usage

Add `'batch_requests'` to your `INSTALLED_APPS` setting.

    INSTALLED_APPS = (
        ...
        'batch_requests',
    )
    
In your `urls.py` add `batch_requests.views.handle_batch_requests` view with one of the endpoints as shown below:


    url(r'^api/v1/batch/', 'batch_requests.views.handle_batch_requests')

This is the only setup required to get it working.



# Making batch requests

Using `batch_requests` is simple. Once we have an endpoint for `batch_requests` working, we can make a `POST` call specifying the list of requests. Each request is a JSON object with 4 keys:

* method: Specifies the http method. Valid values include GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS, CONNECT, and TRACE.

* url: Relative URL for the request.

* body: Serialized / Encoded HTTP body as a String.

* headers: Any additional headers that you would like to pass to this request.
    
At the minimum we need to specify url and method for a request object to be considered valid. Consider for instance we need to batch two http requests. The valid json should look like as shown:

```json
[
  {
    "url" : "/views/",
    "method" : "get"
  },
  {
    "url" : "/views/",
    "method" : "post",
    "body" : "{\"text\": \"some text\"}",
    "headers" : {"Content-Type": "application/json"}
  }
]
```

Here, we are making 2 requests. Get on /views/ and POST to /views/. Please also note that, body of the post request is JSON encoded string (Serialized JSON).

For such a request, batch api replies back with list of HTTP response objects. Each response object consist of status_code, body and response headers. For the above request, the valid response may look like:

```json
[
    {
        "headers": {
            "Content-Type": "text/html; charset=utf-8"
        },
        "status_code": 200,
        "body": "Success!",
        "reason_phrase": "OK"
    },
    {
        "headers": {
            "Content-Type": "text/html; charset=utf-8"
        },
        "status_code": 201,
        "body": "{\"text\": \"some text\"}",
        "reason_phrase": "CREATED"
    }
]
```

Please note that, requests and responses in `batch_requests` are ordered, meaning the first response in the list is for the first request specified.

[build-status-image]: https://secure.travis-ci.org/tanwanirahul/django-batch-requests.svg?branch=master
[travis]: http://travis-ci.org/tanwanirahul/django-batch-requests?branch=master
[pypi-version]: https://pypip.in/version/django-batch-requests/badge.svg
[pypi]: https://pypi.python.org/pypi/django-batch-requests
[Django Rest Framework]: https://github.com/tomchristie/django-rest-framework
[coverage]: https://coveralls.io/repos/tanwanirahul/django-batch-requests/badge.png?branch=master
[coverage-repo]: https://coveralls.io/r/tanwanirahul/django-batch-requests?branch=master
