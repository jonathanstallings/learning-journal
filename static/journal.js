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
        context: main
    })
    .done(function(response) {
        $(this).html(response.text);
    })
    .fail(function() {
        alert( "error" );
    });
});
