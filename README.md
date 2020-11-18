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

## User Model
First off I created a User model and some basic views / templates for some associated tasks.
    - Creating a new user
    - Showing details about a user
        - Decided not to go with the Django generic DetailView here since the urlpattern for this requires that the slug be the primary key of the object instance. I wanted the user to be able to put in a username and see the users profile (provided they're logged in)
    - A sign-in page that does not require authentication (just put you user ID in)
    - Login / Logout links and Navigation links to empty pages (home, user account, etc)


## Events Model
Build the Event model and begin to integrate it's pieces in to the other model (User - the creator of an Event) and the page.
    - Integrate the Event with the User models
    - Show all a user's events on their profile page
    - Page to create events, show all events, show singe event

