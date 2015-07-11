

var taskEventHandler = function (e) {
    //Examine event and send to approriate handler
    var el = e.target;
    var editButton = el.matches("#edit-button");
    var saveButton = el.matches("#save-button");
    var cancelButton = el.matches("#cancel-button");
    
    if (editButton) {
        ajaxEditView(e);
    } else if (saveButton) {
        ajaxSaveEdit(e);
    } else if (cancelButton) {
        ajaxCancelEdit(e);
    }
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
