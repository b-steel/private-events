# private-events

This project is from *The Odin Project's* Ruby on Rails course, but I've chosen to design it in Python/ Django.

[Link](https://www.theodinproject.com/courses/ruby-on-rails/lessons/associations) the the assignment page and description. 

In simple terms it's a **very** basic version of [Eventbrite](http://www.eventbrite.com/).  You can create an account, create events, and invite others to your events.  It's still missing a lot of functionality compared to what you'd really want to have in a page, but the main focus of the assignement was to get practice with Rails Active Records and Associations, which in Django means Models.    

# Models 
This project was realtively simple on the database end, requiring only two models: user and event.

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
- Date - Datetime.date
- Location - Text field
- Description
- Invited - ManyToMany to User
- Attending - ManyToMany to User
- Creator - ForeignKey to User
- Hosts - ManyToMany to User
    

# Utilities
After making the models I created a few utility functions for rapid creation of instances of events, users and locations to speed up the writing of tests.

I created a ModelFactory class that allows one to create random or specific events.  The ModelFactory uses the python package [Essential Generators](https://pypi.org/project/essential-generators/) for the creation of event and user names and descriptions. This will make writing tests quicker and simpler, as well as testing within the shell for simple poking around.  

# Hurdles
Most of the project did not give me much trouble, but I did have a hard time figuring out how to invite other users to an event.  The assignment itself makes no mention of being able to invite users or accept invites, it's just done through the command line for now.  However, I wanted to take a stab at having that functionality in my site. 

With Django, the way you add relations between models is via a related manager, but that isn't available until the event instance itself has been created. So when creating an event on the "create event" page, I had to first create the event without any invited guests, then add them immediately after. That in itself wasn't too hard, but the method for inviting the guests was a bit trickier.

I wanted an intuitive method for inviting people, without having to put a lot of work into it (this was after all a feature not even in the assignment). After some experimentation (and a bit of learning some jQuery) I settled on a small script that collected all the info from the invitation buttons and then sent that info via an AJAX request to the server to be cached. Then when the event itself is created, that info is pulled from the server, and incorporated into the event.  

It's quite verbose and I'm sure can be improved, but with my current js knowledge it gets the job done:

<<<<<<< Updated upstream
'''
=======
```javascript
>>>>>>> Stashed changes
    $("#modal-invite-submit").click(function (event) {
        var data = {
            invited: {},
            hosts: {}
        };
        $(".invitation-list-item").each(function(index) {
            let inviteButton = $(this).children("button[id|=button-invite-user]");
            let hostButton = $(this).children("button[id|=button-host-user]");
            let user_id = inviteButton.attr("id").split('-')[3];
            user_id = parseInt(user_id);
            let inviteStatus = statusDictionary[inviteButton.text().trim()];
            let hostStatus = statusDictionary[hostButton.text().trim()];

            data.invited[user_id] = inviteStatus;
            data.hosts[user_id] = hostStatus;

        });

        $.get({
            url: ajaxUrl,
            data: {data: JSON.stringify(data)},
            dataType:'json',
        });
    });
<<<<<<< Updated upstream
'''
=======
```
>>>>>>> Stashed changes
