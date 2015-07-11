

var taskEventHandler = function (e) {
    //Examine event and send to approriate handler
    var target = e.target;
    
    switch(target.id) {
        case 'new-entry-button':
            newEntryView(e);
            break;
        case 'save-button-create':
            ajaxSaveCreate(e);
            break;
        case 'cancel-button-create':
            cancelCreate(e);
            break;
        case 'delete-button-detail':
            deleteConfirmation(e, 'check');
            break;
        case 'delete-confirm-button-detail':
            deleteConfirmation(e, 'confirm');
            break;
        case 'delete-cancel-button-detail':
            deleteConfirmation(e, 'cancel');
            break;
        case 'edit-button-detail':
            ajaxEditView(e);
            break;
        case 'save-button-edit':
            ajaxSaveEdit(e);
            break;
        case 'cancel-button-edit':
            cancelEdit(e);
            break;
    }
};

var newEntryView = function (e) {
    //Show the new entry view, hiding unneeded elements.
    e.preventDefault();
    $('#new-entry').hide();
    $('#entry-list').hide();
    $('#create-container').show();
};

var cancelCreate = function (e) {
    //Close new entry view; empty and hide form; show needed elements.
    e.preventDefault();
    $('#new-entry').show();
    $('#entry-list').show();
    $('#create-container').hide();
    $('#title-create').val('');
    $('#text-create').val('');
};

var ajaxSaveCreate = function (e) {
    //Send AJAX POST request to save new entry.
    e.preventDefault();
    var title = $('#title-create').val();
    var text = $('#text-create').val();
    var url = "/add";

    $.ajax({
        method: "POST",
        url: url,
        data: {
            title: title,
            text: text
        }
    }).done(function(response) {
        $('#create-container').hide();
        $('#entry-list').show();
        $('#new-entry').show();
        ajaxCreateUpdate(e);
    }).fail(function() {
        alert( "error" );
    });
};

var ajaxCreateUpdate = function (e) {
    //Send AJAX GET request for data and update entry list after new entry.
    var url = "/";

    $.ajax({
        method: "GET",
        url: url,
    }).done(function(response) {
        var entry = response.entries[0];
        var $ul = $('#entry-list ul');
        var $li = $('<li></li>');
        var $link = $('<a>' + entry.title + '</a>');
        var created = new moment(entry.created);
        created.locale('en');
        var dateParsed = created.format("MMM. D, YYYY");
        $link.attr({
           href: "/detail/" + entry.id,
           id: "entry" + entry.id,
           "class": "entry-link"
        });
        var $date = $('<span>' + dateParsed + '</span>');  //Fix date format
        $date.addClass('date');
        $li.append($link);
        $li.append($date);
        $ul.prepend($li);
    }).fail(function() {
        alert( "error" );
    });
};

var deleteConfirmation = function (e, step) {
    //Display confirmation button for deletion

    switch(step) {
        case 'check':
            newEntryView(e);
            $('#delete-button-detail').hide();
            $('#edit-button-detail').hide();
            $('#delete-confirm-button-detail').show();
            $('#delete-cancel-button-detail').show();
            break;
        case 'confirm':
            ajaxDeleteEntry(e);
            break;
        case 'cancel':
            $('#delete-button-detail').show();
            $('#edit-button-detail').show();
            $('#delete-confirm-button-detail').hide();
            $('#delete-cancel-button-detail').hide();
            break;
    }
};

var ajaxDeleteEntry = function (e) {
    //Send AJAX POST request to delete entry and then display entry list.
    e.preventDefault();
    var id = $("article").data('entry-id');
    var url = "/delete/" + id;

    $.ajax({
        method: "POST",
        url: url,
        data: {
            id: id,
        }
    }).done(function(response) {
        $('#entry-detail').hide();
        $('#entry-list').show();
        $('#new-entry').show();
        ajaxDeleteUpdate(e, response.entry);
    }).fail(function() {
        alert( "error" );
    });
};

var ajaxDeleteUpdate = function (e, deletedEntry) {
    //Send AJAX GET request for data and update entry list after deletion.
    var url = "/";

    $.ajax({
        method: "GET",
        url: url,
    }).done(function(response) {
        var $deletedEntry = $('#' + deletedEntry.id);
        $deletedEntry.remove();
    }).fail(function() {
        alert( "error" );
    });
};

var ajaxEditView = function (e) {
    //Send AJAX GET request and display edit view.
    e.preventDefault();
    var url = "/edit/" + $("article").data('entry-id');

    $.ajax({
        method: "GET",
        url: url,
        context: "#entry-edit"
    }).done(function(response) {
        $('#entry-detail').hide();
        $('#edit-container').show();
        $('#title-edit').val(response.entry.title);
        $('#text-edit').val(response.entry.text);
    }).fail(function() {
        alert( "error" );
    });
};

var cancelEdit = function (e) {
    //Close edit view; show needed elements.
    e.preventDefault();

    $('#edit-container').hide();
    $('#entry-detail').show();
};

var ajaxSaveEdit = function (e) {
    //Send AJAX POST request to save edit and display entry detail view.
    e.preventDefault();
    var id = $("article").data('entry-id');
    var title = $('#title-edit').val();
    var text = $('#text-edit').val();
    var url = "/edit/" + id;

    $.ajax({
        method: "POST",
        url: url,
        data: {
            id: id,
            title: title,
            text: text
        }
    }).done(function(response) {
        $('#edit-container').hide();
        $('#entry-detail').show();
        $('#title-detail').html(response.entry.title);
        $('#text-detail').html(response.entry.markdown);
    }).fail(function() {
        alert( "error" );
    });
};

// Event Listener for Collapsible menu button
$('#navbar-toggle').on('click', function (e) {
    e.preventDefault();
    $('#navbar-collapse').toggleClass('collapse');
});


// Event Listener for main section
$('main').on("click", taskEventHandler);
