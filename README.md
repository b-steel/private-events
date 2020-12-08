# private-events

This project is from *The Odin Project's* Ruby on Rails course, but I've chosen to design it in Python/ Django.

[Link](https://www.theodinproject.com/courses/ruby-on-rails/lessons/associations) the the project page and description. 

In simple terms it's a basic level clone of [Eventbrite](http://www.eventbrite.com/) facilitating event coordination

# Models 
This project was realtively simple on the databas end, requiring only two models: user and event.
## User
I used djangos built in [User](https://docs.djangoproject.com/en/3.1/ref/contrib/auth/) class and added a few methods for getting the full name and inviting a user to an event. Overall, the model had the following fields used, with a few related fields as well
- First Name
- Last Name
- Username
- Date Joined
- (events_attending) - relationship from Event.Attendees
- (events_invited_to) - relationship from Event.Invited
## Event
This model was created from scratch with the following fields
- Name
- Date
- Location 
- Description
- Invited - ManyToMany to User
- Attending - ManyToMany to User
- Creator - ForeignKey to User
- Hosts - ManyToMany to User
    


# Workflow
Here's a basic overview of the steps I took (following the overview in the TOP guidelines for the project) and the resources I used

## Utilities
After making the models I created a few utility functions for rapid creation of instances of events, users and locations to speed up the writing of tests.

I created a ModelFactory class that allows one to create random or specific events.  My hope is that this will make writing tests quicker and simpler, as well as testing within the shell for simple poking around.  


## User model and associated views
First off I created a User model and some basic views / templates for some associated tasks such as.
    - Creating a new user
    - Showing details about a user
        - Decided not to go with the Django generic DetailView here since the urlpattern for this requires that the slug be the primary key of the object instance. I wanted the user to be able to put in a username and see the users profile (provided they're logged in)
    - A sign-in page that does not require authentication (just put you user ID in)
    - Login / Logout links and Navigation links to empty pages (home, user account, etc)


## Events model and associated views
I built the Event model and began to integrate it's pieces in to the other model.  

The workflow was as follows: First create an event index page that listed events based on date, divided into past and future events.  Then an event detail page listing all the details of an event, and lastly an event creation page. After that I would integrage the events into the user's page as well so that a user's detail page showed the events that were attending.  

Up to this point I'd just been making things as I went, but for experience I decided to use Django's testing framework to do TDD for the rest of the project.

While writing tests for the 'Create Event' page I started to run into some trouble tring to devise how I wanted the page to work.  The question was how to allow you to invite (or set as a host) existing users - and a similar problem for the location of the event. The prompt for the assignment didn't have any info about this (plus the prompt is for Ruby / Rails), and I wanted the interface to be relatively intuitive.  I settled on having a list of all users with buttons for inviting / making them hosts.  After the user chose who to invite, an AJAX request is sent to the server to cache that information.  I chose to cache the info since the actual event hasn't been created yet, so there's no event to associate the invites with in the database.  I could have created a dummy event to attach the associations to and then update the event later, but this seemed simpler.  


## TODO

Tests for cannot make an event in the past

footer at bottom with short content
