

var taskEventHandler = function (e) {
    //Examine event and send to approriate handler
    var el = e.target;
    var editButton = el.matches("#edit-button");
    var saveButton = el.matches("#save-button");
    var cancelButtonEdit = el.matches("#cancel-button-edit");
    var cancelButtonCreate = el.matches("#cancel-button-create");
    var newEntryButton = el.matches("#new-entry-button");
    var saveButtonCreate = el.matches('#save-button-edit');
    
    if (editButton) {
        ajaxEditView(e);
    } else if (saveButton) {
        ajaxSaveEdit(e);
    } else if (cancelButtonEdit) {
        cancelEdit(e);
    } else if (newEntryButton) {
        newEntryView(e);
    } else if (cancelButtonCreate) {
        cancelCreate(e);
    } else if (saveButtonCreate) {
        ajaxSaveCreate(e);
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
    //Send AJAX GET request for data and update entry list.
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

var cancelEdit = function (e) {
    //Close edit view; show needed elements.
    e.preventDefault();

    $('#edit-container').hide();
    $('#entry-detail').show();
};

// Event Listener for Collapsible menu button
$('#navbar-toggle').on('click', function (e) {
    e.preventDefault();
    $('#navbar-collapse').toggleClass('collapse');
});


// Event Listener for main section
$('main').on("click", taskEventHandler);
