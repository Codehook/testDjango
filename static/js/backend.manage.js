/**
 * Shows and modifies the delete-leave modal
 */
function verify(link, action, scope) {
    var scopeTitle = null;
    var actionTitle = null;
    switch(scope) {
        case 'team':
            scopeTitle = 'Team';
            break;
        case 'organization':
            scopeTitle = 'Organization';
            break;
    }
    switch(action) {
        case 'delete':
            actionTitle = 'Delete';
            break;
        case 'leave':
            actionTitle = 'Leave';
            break;
    }
    $('#verify-title').text(actionTitle + ' ' + scopeTitle + '.');
    $('#verify-description').text('Are you sure you want to ' + action + ' this ' + scope + '? This action cannot be undone.');
    $('#verify-link').text(actionTitle).attr('href', link);
    $('#verify').modal('show');
}

/**
 * Removes the given user from an organization or team
 */
function remove(id) {
    $('[name=id]').val(id);
    $('#hidden').submit();
}