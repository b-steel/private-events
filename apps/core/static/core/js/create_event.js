$("button[id|=button-invite-user], button[id|=button-host-user]").click(function (event) {
    if (this.id.includes('invite')) {
        if ($(this).text() !== 'Cancel Invite') {
            $(this).text('Cancel Invite').toggleClass('btn-primary btn-warning');
        } else {
            $(this).text('Invite').toggleClass('btn-primary btn-warning');
        }
    } else {
        if ($(this).text() !== 'Cancel Host') {
            $(this).text('Cancel Host').toggleClass('btn-primary btn-danger');
        } else {
            $(this).text('Make Host').toggleClass('btn-primary btn-danger');
        }
    }
});

var statusDictionary = {
    'Invite': false,
    'Cancel Invite': true, 
    'Make Host': false, 
    'Cancel Host': true
}
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

