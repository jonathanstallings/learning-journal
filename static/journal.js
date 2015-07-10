

var taskEventHandler = function (e) {
    //Examine event and send to approriate handler
    var el = e.target;
    var editButton = $('#edit-button');
    var saveBuitton = $('#save-button');
};


// Event Listener for Collapsible menu button
$('#navbar-toggle').on('click', function (e) {
    e.preventDefault();
    $('#navbar-collapse').toggleClass('collapse');
});

//
$("#edit-button").on("click", function (e) {
    e.preventDefault();

    var url = "/edit/" + $("article").data('entry-id');
    var main = $('main');

    $.ajax({
        method: "GET",
        url: url,
        context: "#entry-edit"
    })
    .done(function(response) {
        $('#entry-detail').hide();
        $('#entry-edit').show();
        $('#title').val(response.entry.title);
        $('#text').val(response.entry.text);
    })
    .fail(function() {
        alert( "error" );
    });
});
