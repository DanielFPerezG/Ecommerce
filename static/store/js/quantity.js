function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

function wcqib_refresh_quantity_increments() {
    jQuery("div.quantity:not(.buttons_added), td.quantity:not(.buttons_added)").each(function(a, b) {
        var c = jQuery(b);
        c.addClass("buttons_added"), c.children().first().before('<input type="button" value="-" class="minus" />'), c.children().last().after('<input type="button" value="+" class="plus" />')
    });

}
String.prototype.getDecimals || (String.prototype.getDecimals = function() {
    var a = this,
        b = ("" + a).match(/(?:\.(\d+))?(?:[eE]([+-]?\d+))?$/);
    return b ? Math.max(0, (b[1] ? b[1].length : 0) - (b[2] ? +b[2] : 0)) : 0
}), jQuery(document).ready(function() {
    wcqib_refresh_quantity_increments()
}), jQuery(document).on("updated_wc_div", function() {
    wcqib_refresh_quantity_increments()
}), jQuery(document).on("click", ".plus, .minus", function() {
    var a = jQuery(this).closest(".quantity").find(".qty"),
        b = parseFloat(a.val()),
        c = parseFloat(a.attr("max")),
        d = parseFloat(a.attr("min")),
        e = a.attr("step");
    b && "" !== b && "NaN" !== b || (b = 0), "" !== c && "NaN" !== c || (c = ""), "" !== d && "NaN" !== d || (d = 0), "any" !== e && "" !== e && void 0 !== e && "NaN" !== parseFloat(e) || (e = 1), jQuery(this).is(".plus") ? c && b >= c ? a.val(c) : a.val((b + parseFloat(e)).toFixed(e.getDecimals())) : d && b <= d ? a.val(d) : b > 0 && a.val((b - parseFloat(e)).toFixed(e.getDecimals())), a.trigger("change");
    updateProductsPrice(a);

})
;

function updateProductsPrice(a) {
      var oldQuantity = document.getElementById("product-quantity-detail");
      var quantity = parseInt(a.val());
      var totalElement = document.getElementById("total-price-detail");
      var price = document.getElementById("price-detail").textContent;
      price = price.replace("$", "");
      price = parseFloat(price)*1000;
      totalElement.textContent = (quantity*price).toLocaleString()
      oldQuantity.textContent = quantity
    };

function addProductDetail(productId, stock) {
      var quantity = parseInt(document.getElementById("product-quantity-detail").textContent);
      var productId = productId;
      var stock = parseInt(stock);

      if (quantity > stock) {
          Swal.fire({
              icon: 'error',
              title: 'El producto no tiene tantas unidades disponibles',
              text: 'Revisa junto al nombre cuantas unidades disponibles quedan. Pronto volveremos a abastecer nuestro inventario'
      }
      );
          }
      else{
          const data = [];

        const jsonRow = {
          id: productId,
            quantity: quantity
        };

        data.push(jsonRow);
      const json = JSON.stringify(data);

      fetch('../addCartDetail/'+productId,{
            method: 'POST',
            body: json,
            headers:{
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrftoken,
            }
        }
        )
        .then(response => {
                return response.json()
        })
        .then(data => {
            if (data.success) {
            // Redirigir al usuario al "home"
            window.location.href = "..";
            }
        });
      }
    };