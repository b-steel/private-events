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
        - (attending) - relationship from Event.Attendees
        - (invited_to) - relationship from Event.Invited
    - Event
        - time
        - location - ForeignKey to Location
        - invited - ManyToMany to User
        - sttending - ManyToMany to User
    - Location
        - name
        - address
        - (events) - relationship from Event.Location


# Workflow

Here's a basic overview of the steps I took (following the overview in the TOP guidelines for the project) and the resources I used

## User Model
First off I created a User model and some basic views / templates for some associated tasks.  Most of this was accomplished with Django's builtin User class and Generic Templates
    - Creating a new user
    - Showing details about a user
    - A sign-in page that does not require authentication (just put you user ID in)
