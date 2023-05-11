
function wcqib_refresh_quantity_increments_cart() {
    jQuery("div.quantity:not(.buttons_added), td.quantity:not(.buttons_added)").each(function(a, b) {
        var c = jQuery(b);
        c.addClass("buttons_added");
        c.find('input[type="number"]').before('<input type="button" value="-" class="minus-cart" />');
        c.find('input[type="number"]').after('<input type="button" value="+" class="plus-cart" />');
    });
}

String.prototype.getDecimals || (String.prototype.getDecimals = function() {
    var a = this,
        b = ("" + a).match(/(?:\.(\d+))?(?:[eE]([+-]?\d+))?$/);
    return b ? Math.max(0, (b[1] ? b[1].length : 0) - (b[2] ? +b[2] : 0)) : 0;
});

jQuery(document).ready(function() {
    wcqib_refresh_quantity_increments_cart();
});

jQuery(document).on("updated_wc_div", function() {
    wcqib_refresh_quantity_increments_cart();
});

jQuery(document).on("click", ".plus-cart, .minus-cart", function() {
    var quantityInput = jQuery(this).siblings('input.qty');
    var filaProductId = jQuery(this).closest('tr');
    var productId = filaProductId.find("td:first-child").text();
    var quantityValue = parseFloat(quantityInput.val());
    var maxQuantity = parseFloat(quantityInput.attr("max"));
    var minQuantity = parseFloat(quantityInput.attr("min"));
    var step = quantityInput.attr("step");

    if (isNaN(quantityValue) || quantityValue === '') {
        quantityValue = 0;
    }

    if (isNaN(maxQuantity) || maxQuantity === '') {
        maxQuantity = '';
    }

    if (isNaN(minQuantity) || minQuantity === '') {
        minQuantity = 0;
    }

    if (step === 'any' || step === '' || step === undefined || isNaN(parseFloat(step))) {
        step = 1;
    }

    if (jQuery(this).hasClass("plus-cart")) {
        if (maxQuantity !== '' && quantityValue >= maxQuantity) {
            quantityInput.val(maxQuantity);
        } else {
            quantityInput.val((quantityValue + parseFloat(step)).toFixed(step.getDecimals()));
        }
    } else if (jQuery(this).hasClass("minus-cart")) {
        if (minQuantity !== '' && quantityValue <= minQuantity) {
            quantityInput.val(minQuantity);
        } else if (quantityValue > 0) {
            quantityInput.val((quantityValue - parseFloat(step)).toFixed(step.getDecimals()));
        }
    }

    quantityInput.trigger("change");

    var newValue = parseFloat(quantityInput.val());
    console.log(productId)
    createJSON(newValue,productId);
});

function createJSON(a,productId) {
      const data = [];


        const jsonRow = {
          id: productId,
            quantity: a
        };

        data.push(jsonRow);

      const json = JSON.stringify(data);

      fetch('updateCart',{
            method: 'POST',
          body: json,
            headers:{
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrftoken,
            }
        }
        )
        .then(response => {
                return response.json() //Convert response to JSON
        })
        .then(data => {
                var subTotal = document.getElementById("subtotal");
                var totalPrice = document.getElementById("total_price");
                var subTotalcount = 0;

                for (let i = 0; i < data.length; i++) {
                    var totalElement = document.getElementById("total_price_"+data[i]["id"]);
                    totalElement.textContent = "$"+data[i]["total"]
                    subTotalcount += data[i]["total"]
                }
                subTotal.textContent = "$"+subTotalcount
                totalPrice.textContent = "$"+(subTotalcount+10000)
        });



    }
;