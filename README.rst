==================================
django_tagcapsule
=================

django_tagcapsule is a Django application designed to easily get rid of dynamic content insertion (scripts like Google Analytics, partners tags...) in templates.

Currently in beta (v0.1).

Requirements
============

- Django 1.3+

Installation
============

#. Add the `django_tagcapsule` directory to your Python path.

#. Add `django_tagcapsule` to your `INSTALLED_APPS` setting in `settings.py` file:

	``'django_tagcapsule',``
	
#. Add the following middleware to your project's `settings.py` file:

	``'django_tagcapsule.middleware.TagCapsuleMiddleware',``

#. Let Django create the needed database:

	``python manage.py syncdb``

Configuration
=============

One installed, django_tagcapsule adds a few topics in your admin panel as you can start creating tags.