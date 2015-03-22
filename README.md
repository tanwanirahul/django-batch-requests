Django Batch Requests
=========================

[![build-status-image]][travis]
[![pypi-version]][pypi]
[![coverage]][coverage-repo]

Django batch requests allow developers to combine multiple http requests into a single batch request. This is essentially useful to avoid making multiple http requests to save on round trip network latency.

Its built on top of Django and uses relies on Django's URL dispatching, hence it could also be used with any web framework built on top of Django such as [Django Rest Framework].

# Requirements

* Python (2.7)
* Django (1.7)

# Installation

Install using `pip`...

    pip install django-batch-requests

Install from source...

    python setup.py install

Add `'batch_requests'` to your `INSTALLED_APPS` setting.

    INSTALLED_APPS = (
        ...
        'batch_requests',
    )


[build-status-image]: https://secure.travis-ci.org/tanwanirahul/django-batch-requests.svg?branch=master
[travis]: http://travis-ci.org/tanwanirahul/django-batch-requests?branch=master
[pypi-version]: https://pypip.in/version/django-batch-requests/badge.svg
[pypi]: https://pypi.python.org/pypi/django-batch-requests
[Django Rest Framework]: https://github.com/tomchristie/django-rest-framework
[coverage]: https://coveralls.io/repos/tanwanirahul/django-batch-requests/badge.png?branch=master
[coverage-repo]: https://coveralls.io/r/tanwanirahul/django-batch-requests?branch=master
