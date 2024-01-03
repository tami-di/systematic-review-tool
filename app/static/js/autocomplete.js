$(document).ready(function() {
    $('#searchInput').on('input', function() {
        let term = $(this).val();
        $.ajax({
            url: '/autocomplete',
            data: { term: term },
            success: function(data) {
                $('#suggestions').empty();
                data.forEach(function(item) {
                    $('#suggestions').append('<li>' + item + '</li>');
                });
            }
        });
    });
});
