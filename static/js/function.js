console.log("working fine");

$("#commentForm").submit(function(e) {
    e.preventDefault();
    // Add your code here
    $.ajax(
        {
            data: $(this).serialize(),
            method: $(this).attr("method"),
            url: $(this).attr("action"),
            dataType: "json",
            success: function(res){
                console.log("comment saved to db");

                if (res.bool == true) {
                    $("#review-res").html("review added");
                }
            }
        }
    )
});


$(document).ready(function () {

    $("#price-filter-btn").on("click", function () {
        console.log("a checkbox hasbeen checked");
        let filter_object = {}

        let min_price = $("#price-number").attr("min")
        let max_price = $("#price-number").val()
        filter_object.min_price = min_price;
        filter_object.max_price = max_price;

        console.log("filter object is: ", filter_object);
        $.ajax({
            url: '/filter-products',
            data: filter_object,
            dataType: 'json',
            beforeSend: function () {
                console.log("trying to filter...");
            },
            success: function (response) {
                console.log(response);
                console.log("data filtered successfully");

                $("#filtered-product").html(response.data)

            }
        })
    })

    $("#price-number").on("blur", function () {
        let min_price = $(this).attr("min");
        let max_price = $(this).attr("max");
        let current_price = $(this).val();

        console.log("Current:", current_price);
        console.log("Max:", max_price);
        console.log("Min:", min_price);

        if (current_price < parseInt(min_price) || current_price > parseInt(max_price)) {

            min_price = Math.round(min_price*100)/100
            max_price = Math.round(max_price*100)/100

            alert("Price must be between " + min_price + "/- and " + max_price + "/-");
            $(this).val(min_price);
            $('#price-range').val(min_price);
            $(this).focus();
            return false;
        }
    })

    // Add to cart functionality
    $(".add-to-cart-btn").on("click", function() {

    let this_val = $(this)

    let index = this_val.attr("data-index")
    let quantity = $(".product-quantity-" +index).val();
    let product_title = $(".product-title-" +index).val();
    let product_id = $(".product-id-" +index).val();
    let product_price = $(".current-product-price-" +index).text();
    let product_pid = $(".product-pid-" +index).val();
    let product_image = $(".product-image-" +index).val()


  
    console.log("Quantity:", quantity);
    console.log("Title:", product_title);
    console.log("Price:", product_price);
    console.log("ID:", product_id);
    console.log("PID:", product_pid);
    console.log("Image:", product_image);
    console.log("Index:", index);


    console.log("Current Element:", this_val);
    
    $.ajax({
        url: '/add-to-cart',
        data: {
          'id': product_id,
          'pid': product_pid,
          'image': product_image,

          'qty': quantity,
          'title': product_title,
          'price': product_price
        },
        dataType: 'json',
        beforeSend: function() {
          console.log("Adding Product to Cart...");
        },
        success: function(response) {
          this_val.html("✓");
          console.log("Added Product to Cart!");
          $(".cart-items-count").text(response.totalcartitems)
        }
      })
    }) //addd to cart end

    $(".delete-product").on("click", function() {
        let product_id = $(this).attr("data-product");
        let this_val = $(this);
        console.log("Product ID:", product_id);

        $.ajax({
            url: "/delete-from-cart",
            data: {
                "id": product_id
            },
            dataType: "json",
            beforeSend: function() {
                this_val.hide();
            },
            success: function(response) {
                this_val.show();
                $(".cart-items-count").text(response.totalcartitems);
                $("#cart-list").html(response.data);
            }
        })
    })



    $(".update-product").on("click", function() {
        let product_id = $(this).attr("data-product");
        let this_val = $(this);
        let product_quantity = $(".product-qty-"+product_id).val()
        console.log("Product ID:", product_id);
        console.log("Product quantity:", product_quantity);


        
        $.ajax({
            url: "/update-cart",
            data: {
                "id": product_id,
                "qty": product_quantity,

            },
            dataType: "json",
            beforeSend: function() {
                this_val.hide();
            },
            success: function(response) {
                this_val.show();
                $(".cart-items-count").text(response.totalcartitems);
                $("#cart-list").html(response.data);
            }
        }) 
    })
    // Making Default Address
    $(document).on("click", ".make-default-address", function() {
        let id = $(this).attr("data-address-id")
        let this_val = $(this)
        console.log("ID is:", id);
        console.log("Element is:", this_val);
        $.ajax({
            url: "/make-default-address",
            data: {
                "id": id
            },
            dataType: "json",
            success: function(response) {
                console.log("Address Made Default....");
                if (response.boolean === true) {
                    $(".check").hide()
                    $(".action_btn").show()
                    $(".check" + id).show()
                    $(".button" + id).hide()
                }
                
            }
        })
        
    })

    $(document).on("click", ".add-to-wishlist", function() {
        let product_id = $(this).attr("data-product-item")
        let this_val = $(this)
        console.log("Product ID IS", product_id);
        $.ajax({
            url: "/add-to-wishlist",
            data: {
                "id": product_id
            },
            dataType: "json",
            beforeSend: function() {
                console.log("Adding to wishlist...");

            },
            success: function(response) {
                this_val.html("✓");

                if (response.bool ===true){
                    console.log("Added to wishlist...");

                }
            }
        })
        
    });


    // Remove from wishlist
    $(document).on("click", ".delete-wishlist-product", function() {
        let wishlist_id = $(this).attr("data-wishlist-product")
        let this_val = $(this);
        console.log("wishlist id is:", wishlist_id);
        $.ajax({
            url: "/remove-from-wishlist",
            data: { 
                "id": wishlist_id 
            },
            dataType: "json",
            beforeSend: function() {
                console.log("Deleting product from wishlist...");
            },
            success: function(response) {
                $("#wishlist-list").html(response.data);
            }
        })
    })
    
}); // ready end

  

