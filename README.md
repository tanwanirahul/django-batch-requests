Django Batch Requests
=========================

[![build-status-image]][travis]
[![pypi-version]][pypi]
[![coverage]][coverage-repo]
[![Downloads](https://pepy.tech/badge/django-batch-requests)](https://pepy.tech/project/django-batch-requests)

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

It is also important to note that all the requests by default execute sequentially one after another. Yes, you can change this behavior by configuring the concurrency settings.


# Executing requests in parallel (Concurrency)

Before we jump to concurrency, lets first examine the execution time required to run all requests sequentially. Assume we have an API `/sleep/?seconds=3` which mimics the time consuming APIs by putting the thread to sleep for the specified duration. Let us now make 2 requests in batch for the above sleep API.

```json
[
  {
    "method": "get",
    "url": "/sleep/?seconds=3"
  },
  {
    "method": "get",
    "url": "/sleep/?seconds=3"
  }
]
```
Here is the response we get.

```json
[
    {
        "headers": {
            "Content-Type": "text/html; charset=utf-8",
            "batch_requests.duration": 3
        },
        "status_code": 200,
        "body": "Success!",
        "reason_phrase": "OK"
    },
    {
        "headers": {
            "Content-Type": "text/html; charset=utf-8",
            "batch_requests.duration": 3
        },
        "status_code": 200,
        "body": "Success!",
        "reason_phrase": "OK"
    }
]
```
Each request took about 3 seconds as is evident with the header `"batch_requests.duration": 3`. 

Batch api response header also include:
`
batch_requests.duration 6
`
This shows the total batch request took 6 seconds - sum of the individual requests. Let us now turn ON the concurrency.

## Configuring Parallelism / Concurrency:

Parallelism / Concurrency can be turned ON by specifying the appropriate settings:

`"EXECUTE_PARALLEL": True`

`batch_requests` will now execute the individual requests in parallel. Let us check how it impacts the performance. We will make the same request once again after enabling the parallelism.

```json
[
  {
    "method": "get",
    "url": "/sleep/?seconds=3"
  },
  {
    "method": "get",
    "url": "/sleep/?seconds=3"
  }
]
```

This request yields the following response:

```json
[
    {
        "headers": {
            "Content-Type": "text/html; charset=utf-8",
            "batch_requests.duration": 3
        },
        "status_code": 200,
        "body": "Success!",
        "reason_phrase": "OK"
    },
    {
        "headers": {
            "Content-Type": "text/html; charset=utf-8",
            "batch_requests.duration": 3
        },
        "status_code": 200,
        "body": "Success!",
        "reason_phrase": "OK"
    }
]
```
with the batch response header:

`batch_requests.duration:  3`.

Though each request still took 3 seconds, total time that batch request took is only 3 seconds. This is an evident that requests were executed concurrently.

`batch_requests` add duration header for all the individual requests and also the main batch request. If it is too verbose for you, you can turn this feature off by setting:

`"ADD_DURATION_HEADER": True`

You can also change the duration header name to whatever suites you better, by setting:

`"DURATION_HEADER_NAME": "batch_requests.duration"`

## More Parallelism / Concurrency settings:

There are two widely used approached to achieve concurrency. One through launching multiple threads and another through launching multiple processes. `batch_requests` support both these approaches. There are two settings you can configure in this regard:

```
"CONCURRENT_EXECUTOR": "batch_requests.concurrent.executor.ThreadBasedExecutor"
"NUM_WORKERS": 10
```

`CONCURRENT_EXECUTOR` value must be one of the following two:
1. batch_requests.concurrent.executor.ThreadBasedExecutor
2. batch_requests.concurrent.executor.ProcessBasedExecutor

to achive thread and process based concurrency respectively. `NUM_WORKERS` determines how may threads / processes to pool to execute the requests. Configure this number wisely based on the hardware resources you have. By default, if you turn ON the parallelism, `ThreadBasedExecutor` with `number_of_cpu * 4` workers is configured on the pool.


## Choosing between threads vs processes for concurrency:

There is no abvious answer to this, and it depends on various settings - the resources you have, the amount of web workers you are running, whether the application is blocking or non blocking, if the application is cpu or io bound etc. However, the good way to start off with is:

*  Choose ThreadBasedExecutor if your application is doing too much IO and the code is blocking.
*  Choose ProcessBasedExecutor if your application is CPU bound.



[build-status-image]: https://secure.travis-ci.org/tanwanirahul/django-batch-requests.svg?branch=master
[travis]: http://travis-ci.org/tanwanirahul/django-batch-requests?branch=master
[pypi-version]: https://badge.fury.io/py/django-batch-requests.svg
[pypi]: https://pypi.python.org/pypi/django-batch-requests
[Django Rest Framework]: https://github.com/tomchristie/django-rest-framework
[coverage]: https://coveralls.io/repos/tanwanirahul/django-batch-requests/badge.png?branch=master
[coverage-repo]: https://coveralls.io/r/tanwanirahul/django-batch-requests?branch=master
