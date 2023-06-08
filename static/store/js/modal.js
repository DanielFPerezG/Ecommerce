function addCart(idProduct){
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
        var number_products = document.getElementById("number_products");
        json1 = data.json1
        json2 = JSON.parse(data.json2)
        var name_product = json2[0].name;
        number_products.textContent = json1
        console.log(name_product)
        Toast.fire({
            icon: 'success',
            title: 'Has agregado el producto '+name_product+' a tu carrito de compra'
        })
    });
};

function updateUserInfo(userId, type){
    var title;
    var finalTitle;
    var input;
    if (type === "name") {
      title = 'Ingrese su nombre';
      finalTitle = 'Has cambiado tu nombre exitosamente';
    } else if (type === "lastName") {
      title = 'Ingrese su apellido';
      finalTitle = 'Has cambiado tu apellido exitosamente';
    } else if (type === 'card') {
        title = 'Ingrese su Documento de identidad';
        finalTitle = 'Has cambiado tu Documento exitosamente'
    } else if (type === 'phone') {
        title = 'Ingrese su Numero de Celular';
        finalTitle = 'Has cambiado tu numero exitosamente'
    }

    Swal.fire({
  title: title,
  input: 'text',
  inputAttributes: {
    autocapitalize: 'off'
  },
  showCancelButton: true,
  cancelButtonText: 'Cancelar',
  confirmButtonText: 'Aceptar',
  showLoaderOnConfirm: true,
  preConfirm: (newInfo) => {
    var userInfo = document.getElementById("userInfo_"+type);
    userInfo.textContent = newInfo;
    return fetch(`/updateUserInfo/${userId}`, {
        method: 'POST',
        body: JSON.stringify({ 'newInfo': newInfo, 'type': type }),
        headers:{
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrftoken,
        }
        }
    )
      .then(response => {
        if (!response.ok) {
          throw new Error(response.statusText)
        }
        return response.json()
      })
      .catch(error => {
        Swal.showValidationMessage(
          `Request failed: ${error}`
        )
      })
  },
  allowOutsideClick: () => !Swal.isLoading()
}).then((result) => {
  if (result.isConfirmed) {
    Swal.fire({
      position: 'top-end',
      icon: 'success',
      title: finalTitle,
      showConfirmButton: false,
      timer: 1500
    })
  }
})
}