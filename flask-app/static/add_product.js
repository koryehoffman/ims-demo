$(document).ready(function() {
    $('#add-product-form').on('submit', function(event) {
        event.preventDefault();

        var productData = {
            product_name: $('#product-name').val(),
            product_category: $('#product-category').val(),
            price: $('#price').val(),
            available_quantity: $('#available-quantity').val(),
            description: $('#description').val()
        };

        // Check if any of the required fields are empty
        for (var key in productData) {
            if (!productData[key]) {
                alert('All fields are required!');
                return;
            }
        }

        $.ajax({
            url: '/products',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(productData),
            success: function(data) {
                alert('Product added successfully!');
                $('#add-product-form')[0].reset();
            },
            error: function(request, status, error) {
                alert(request.responseText);
            }
        });
    });
});
