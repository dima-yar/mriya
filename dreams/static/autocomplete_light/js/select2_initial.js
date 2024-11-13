$(document).ready(function() {
    $('#id_tags').select2({
        placeholder: 'Виберіть теги',
        allowClear: true,
        ajax: {
            url: '/tag-autocomplete/',
            dataType: 'json',
            delay: 250,
            data: function (params) {
                return {
                    q: params.term
                };
            },
            processResults: function (data) {
                return {
                    results: data.results
                };
            },
            cache: true
        }
    });
});
