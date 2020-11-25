# private-events

This project is from *The Odin Project's* Ruby on Rails course, but I've chosen to design it in Python/ Django.

[Link](https://www.theodinproject.com/courses/ruby-on-rails/lessons/associations) the the project page and description. 

In simple terms it's a basic level clone of [Eventbrite](http://www.eventbrite.com/) facilitating event coordination


If you'd like to log in as a basic user - 
    - username: temp
    - password: snoop-around

# Models 
    - User
        - user_id
        - first_name
        - last_name
        - email
        - (events_attending) - relationship from Event.Attendees
        - (events_invited_to) - relationship from Event.Invited
    - Event
        - name
        - date
        - time
        - location - ForeignKey to Location
        - description
        - invited - ManyToMany to User
        - attending - ManyToMany to User
        - creator - ForeignKey to User
        - hosts - ManyToMany to User
    - Location
        - name
        - address
        - (events) - relationship from Event.Location


# Workflow

Here's a basic overview of the steps I took (following the overview in the TOP guidelines for the project) and the resources I used

## Utilities
After making the models I created a few utility functions for rapid creation of instances of events, users and locations to speed up the writing of tests.

I created a ModelFactory class that allows users to utilize three different preset Users, three preset Locations, and create random or specific events.  My hope is that this will make writing tests quicker and simpler, as well as testing within the shell for simple poking around.  


## User model and associated views
First off I created a User model and some basic views / templates for some associated tasks.
    - Creating a new user
    - Showing details about a user
        - Decided not to go with the Django generic DetailView here since the urlpattern for this requires that the slug be the primary key of the object instance. I wanted the user to be able to put in a username and see the users profile (provided they're logged in)
    - A sign-in page that does not require authentication (just put you user ID in)
    - Login / Logout links and Navigation links to empty pages (home, user account, etc)


## Events model and associated views
Build the Event model and begin to integrate it's pieces in to the other model (User - the creator of an Event) and the page.
    - Integrate the Event with the User models
    - Show all a user's events on their profile page

Up to this point I'd just been making things as I went, but for experience I decided to use Django's testing framework to do TDD for the rest of the project.
    - Next steps are to create pages to create events, show all events, show single event
    - Showing a single event - my requirements for the page are:
        - Details are unavailable unless logged in
        - There's an option to attend / not-attend depending on the current situation
            - These are only available to those who are invited
        - The attending people are listed, invited people are not listed
        - A host has the ability to edit the event

While writing tests for the 'Create Event' page I started to run into some trouble tring to devise how I wanted the page to work.  The question was how to allow you to invite (or set as a host) existing users - and a similar problem for the location of the event. The prompt for the assignment didn't have any info about this (plus the prompt is for Ruby / Rails), and I wanted the interface to be relatively intuitive.  I settled on having a list of all users with buttons for inviting them.  The buttons would be tied to an AJAX request to add the user to the invited list.  However, in my search for resources on how to do such AJAX requests I ended up on a tangent of learning some basic jQuery as well.  Needless to say that took me some time to figure out, but ultimately I'm very happy with the solution.


# TO BUILD
clicking invite guests will bring up modal of all the users (no search, too complicated). Each will have a button for Inite or host or Uninvite or unhost depending.  The button will toggle the info for that person and store the data in the cache

when the event is created, pull all htat info from the cache and update the event, then clear out the cache


- AJAX section
    - get invite data
        - class method .is_ivited or .is_inviteable
    - get host data
        - class method again
    - invite person
        - class method
    - host person
    - uninvite person
    - unhost person
    - attend
    - un-attend
- Modal section
    - Add/Edit hosts (html)
    - Add / edit invitations (html)

