$("button[id|=button-accept-invite]").click(function (event){
    $(this).prop('disabled', true).text('Invite Accepted')
    
    $.get({
        url: ajaxUrl,
        data: {event_id: $(this).attr("id").split('-')[3]},
        success: function(resp) {
            console.log('Invite Accepted');
        }
    });
});