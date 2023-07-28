function cancelOrder(orderId){
    Swal.fire({
  title: '¿Quiéres cancelar la orden?',
  html: '<p> No podras reactivar la orden despues de cancelarla</p>',
  showCancelButton: true,
  confirmButtonText: 'Cancelar',
  cancelButtonText: `Regresar`,
}).then((result) => {
  if (result.isConfirmed) {
    return fetch(`/cancelStoreOrder/${orderId}`, {
        method: 'POST',
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
            window.location.href = '/viewOrder';
            }

        )
      .catch(error => {
        Swal.showValidationMessage(
          `Request failed: ${error}`
        )
      })
  } else if (result.isDenied) {
    Swal.fire('Changes are not saved', '', 'info')
  }
})
}