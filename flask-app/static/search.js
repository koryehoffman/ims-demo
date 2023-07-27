$(document).ready(function() {
    $('#search-form').on('submit', function(event) {
        event.preventDefault();

        var query = $('#search-input').val();
        $.get('/products/search', { query: query }, function(data) {
            var results = $('#results');
            results.empty();
            data.forEach(function(product) {
                var item = $('<li class="list-group-item">' +
                             '<h5>' + product.product_name + '</h5>' +
                             '<p>' + product.description + '</p>' +
                             '<button class="btn btn-danger btn-sm delete-btn" style="display: none;">Delete</button>' +
                             '</li>');
                item.hover(function() {
                    $(this).find('.delete-btn').toggle();
                });
                item.find('.delete-btn').click(function() {
                    $.ajax({
                        url: '/products/' + product.product_id,
                        type: 'DELETE',
                        success: function(result) {
                            item.remove();
                        }
                    });
                });
                results.append(item);
            });
        });
    });
});
