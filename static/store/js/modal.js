function addCart(idProduct){
    console.log(idProduct)
    var Toast = Swal.mixin({
      toast: true,
      position: 'bottom-end',
      showConfirmButton: false,
      timer: 3000,
      customClass: {
        container: 'my-toast-container',
        title: 'my-toast-title',
        icon: 'my-toast-icon'
      }
    });

    fetch('/addCart/'+idProduct,{
        method: 'POST',
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
        //var number_products = document.getElementById("number_products");
        json1 = data.json1
        json2 = JSON.parse(data.json2)
        var name_product = json2[0].name;
        //number_products.textContent = json1
        console.log(name_product)
        Toast.fire({
            icon: 'success',
            title: 'Has agregado el producto '+name_product+' a tu carrito de compra'
        })
    });
};
