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

function addCartNoStock(name_product){
    Swal.fire({
  icon: 'error',
  title: 'El producto ' +name_product+' no tiene unidades disponibles',
  text: 'Pronto volveremos a abastecer nuestro inventario'
})

}

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

function updatePassword(userId){
    Swal.fire({
      title: 'Cambia tu contraseña',
      html: '<div class="form-group">' +
    '<label for="lastPassword">Contraseña actual:</label>' +
    '<input id="lastPassword" class="form-control" placeholder="Ingresa tu contraseña actual" type="password">' +
    '</div>' +
    '<div class="form-group">' +
    '<label for="newPassword">Nueva contraseña</label>' +
    '<input id="newPassword" class="form-control" placeholder="Ingresa tu nueva contraseña" type="password">' +
    '</div>' +
    '<div class="form-group">' +
    '<label for="confirmPassword">Repite la nueva contraseña</label>' +
    '<input id="confirmPassword" class="form-control" placeholder="Ingresa tu nueva contraseña" type="password">' +
    '</div>',
      focusConfirm: false,
      showCancelButton: true,
      cancelButtonText: 'Cancelar',
      preConfirm: () => {
        newPassword = Swal.getPopup().querySelector('#newPassword').value;
        confirmPassword = Swal.getPopup().querySelector('#confirmPassword').value;
        lastPassword = Swal.getPopup().querySelector('#lastPassword').value;

        return fetch(`updatePassword/${userId}`, {
            method: 'POST',
            body: JSON.stringify({ 'lastPassword': lastPassword, 'newPassword': newPassword, 'confirmPassword': confirmPassword }),
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
          .then(data => {
          if (data.error) {
            // Display error message in the modal
            Swal.showValidationMessage(data.error);
          }
          })
          .catch(error => {
            Swal.showValidationMessage(
              `Request failed: ${error}`
            )
          })

      },
      allowOutsideClick: false,
    }).then((result) => {
      if (result.isConfirmed) {
        Swal.fire({
      position: 'top-end',
      icon: 'success',
      title: 'Has cambiado tu contraseña con exito',
      showConfirmButton: false,
      timer: 1500
    });
      }
    });
}
function deleteUser(userId){
    Swal.fire({

        title: 'Eliminar contraseña',
      html: '<div class="form-group">' +
    '<label>Si eliminas tu cuenta perderas todo el registro de tus compras.</label>' +
    '</div>',
      focusConfirm: false,
      showCancelButton: true,
      cancelButtonText: 'Cancelar',
      preConfirm: () => {
        return fetch(`deleteUser/${userId}`, {
            method: 'POST',
            headers:{
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrftoken,
            }
            }
        )
       .then(response => {
        if (response.ok) {

          window.location.href = '/';
        } else {
          console.error('Error al eliminar el usuario.');
        }
      });
      },
      allowOutsideClick: false,
    }).then((result) => {
    });
}