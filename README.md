# S.O.L.I.D.-Backend

<p align="center">
<a href="https://codecov.io/gh/zentrumnawi/solid-backend">
  <img src="https://codecov.io/gh/zentrumnawi/solid-backend/branch/master/graph/badge.svg" /> 
</a>
<a href="https://travis-ci.com/zentrumnawi/solid-backend"> 
  <img src="https://travis-ci.com/zentrumnawi/solid-backend.svg?branch=master">
</a>
<a href="https://github.com/ambv/black">
  <img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">
</a>
</p>

## What is S.O.L.I.D.?
The project's name is an acronym for **S**ystematic **O**bject-**L**earning and **I**dentification, 
which is the purpose of this pluggable django app. It is here to provide a solid (hehe - :D) foundation for future eLearning apps.
During the creation of two eLearning apps at Goethe University Frankfurt we figured out that a lot of disciplines require students to learn how to systematically analyse and classify certain objects. Those objects might be hand-samples of minerals, stones, stuffed animals, paintings or plants, mostly stored in archives with limited access - or none at all. To prevent us from repeating all steps in the creation of a back- and frontend, we focused on the question "Which components will all these apps have in common?" and this package is what we came up with.
In order to tackle the problem of limited access to hand-samples, we need to store and process high-definition images with the capability of a zoom feature to deliver HD images on any kind of device. Furthermore, we need a way to arrange the hand-samples in a structured way to provide the core feature. But that's not it. eLearning does not solely consist of content distribution. So we also thought of a glossary which the students have at hand without the need to refer to the lecture notes. Another module to display miscellaneous content is the slideshow feature which dombines text and image on separate pages.
Beyond that, we implemented a quiz in order to give students the opportunity to evaluate their current level of understanding. To top it off, we figured it might be useful to display messages to communicate with our users. Messages can inform about updates, events in the context of a lecture, provide fun facts or make up an advent calender with daily tasks or puzzles. A contact form implementation provides a communication in the other direction.

So what does S.O.L.I.D provide in short:

- A generic way to set up database models which can be structured in a hierarchical tree.
- A simple way to store high-definition images which provides automatic creation of DZI-files for the usage of [OpenSeadragon](https://openseadragon.github.io/)
- A Quiz-system with a variety of Question types.
- A Glossary to provide subject-specific terminology.
- A Message system which can be utilized in various ways.
- A Slideshow system to provide content in a presentation style.
- A Feedback form to facilitate bug reports and questions.
So if you are looking to build the backend of an eLearning app, you came to the right place.
For inspiration or just to see what it looks like to use `solid-backend` in the end have a look at [geomat-backend]()and/or [dive-backend]().
If you are also interested in the Frontend: We also have an Angular package which can be found [here]() and which is the foundation of the corresponding apps under geomat.uni-frankfurt.de and dive.uni-frankfurt.de


## Get started
Requirements for this package are:
* Django >3.0.0
* Djangorestframework 3.11.0
* django-mptt 0.11.0
* pillow 7.1.2
* django-cleanup 4.0.0
* psycopg2-binary 2.8.5
* django-taggit 1.5.1

Psycopg2 is important because we are using PostgreSQL specific databasefields. This means that
you are also required to use a PostgreSQL database.

### Installation

The solid-backend package is distributed via PyPi so you can simply install it via
	
	pip install solid-backend
	
Add the apps to your `INSTALLED_APPS` for a bare minimum functionality
	
	settings.py
	
	INSTALLED_APPS = [
    ...,
    "solid_backend.content",
    "solid_backend.photograph",
]

or all apps
	
	settings.py
	
	INSTALLED_APPS = [
		"solid_backend.contact",
		"solid_backend.content",
		"solid_backend.glossary",
		"solid_backend.message",
		"solid_backend.quiz",
		"solid_backend.slideshow",
		"solid_backend.photograph",
	]

Afterwards, don't forget to add the url's to your url-config.
Here, again, you can either decide which urls to include or include all of them:

Specific urls:

	urls.py
	
	urlpatterns = [
		...,
		url(r"", include("solid_backend.content.urls"), name="content"),
		url(r"", include("solid_backend.message.urls"), name="message"),
		url(r"", include("solid_backend.photograph.urls"), name="photograph"),
	
	]

All urls:

		urls.py
	
	urlpatterns = [
		...,
		url("", include("solid_backend.urls")),
		
	]
	
After this you are ready to run the migrations and you are good to go.



## Documentation

Documentation is available [here](https://app.gitbook.com/@zentrumnawi/s/dive/).
The Documentation is currently only available in german. If you are a non-german speaker
and want to know more about something feel free to contact us directly via mail and we 
will figure it out.

## Coverage

Coming soon...

## Try it out and local development

For a How-To guide see the README in the sample_project directory.

