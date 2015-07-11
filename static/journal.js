

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
        ajaxCancelEdit(e);
    } else if (newEntryButton) {
        newEntryView(e);
    } else if (cancelButtonCreate) {
        cancelCreate(e);
    } else if (saveButtonCreate) {
        ajaxSaveCreate(e);
    }
};

var newEntryView = function (e) {
    //Send AJAX GET request for edit view
    e.preventDefault();
    $('#new-entry').hide();
    $('#entry-list').hide();
    $('#create-container').show();
};

var ajaxSaveCreate = function (e) {
    //Send AJAX POST request to save edit
    e.preventDefault();
    var title = $('#title-create').val();
    var text = $('#text-create').val();
    var url = "/create";

    $.ajax({
        method: "POST",
        url: url,
        data: {
            title: title,
            text: text
        }
    }).done(function(response) {
        $('#create-container').hide();
        $('#new-entry').show();
        ajaxCreateUpdate();
    }).fail(function() {
        alert( "error" );
    });
};

var ajaxCreateUpdate = function (e) {
    //Send AJAX POST request to save edit
    var url = "/list";
    var $entriesUL = $('#entry-list ul');
    var $newEntry = document.createElement("li");
    var $newEntryLink = document.createElement("a");
    var $newEntryDate = document.createElement("span");

    $.ajax({
        method: "GET",
        url: url,
    }).done(function(response) {
        // $newEntryLink.attr({
        //     href: $newEntryLink.data('url-base') + response.new_entry.id,
        //     id: "entry" + response.new_entry.id
        // }).text(response.new_entry.title);
        $newEntryDate.text(response.new_entry.created);
        $firstEntry.before($newEntry);
    }).fail(function() {
        alert( "error" );
    });
};

var cancelCreate = function (e) {
    //Send AJAX GET request for edit view
    e.preventDefault();
    $('#new-entry').show();
    $('#entry-list').show();
    $('#create-container').hide();
    $('#title-create').val('');
    $('#text-create').val('');
};

var ajaxEditView = function (e) {
    //Send AJAX GET request for edit view
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
    //Send AJAX POST request to save edit
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


var ajaxCancelEdit = function (e) {
    //Send AJAX GET request for detail view
    e.preventDefault();
    var url = "/detail/" + $("article").data('entry-id');

    $.ajax({
        method: "GET",
        url: url,
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
