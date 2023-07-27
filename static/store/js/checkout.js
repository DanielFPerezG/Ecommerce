function updateAddressFields(selectElement) {
    var selectedOption = selectElement.options[selectElement.selectedIndex].text;

    var selectedAddress = null;
    for (var i = 0; i < addresses.length; i++) {
        if (addresses[i].address === selectedOption) {
            selectedAddress = addresses[i];
            break;
        }
    }

    document.getElementById('city-input').value = selectedAddress.city;
    document.getElementById('state-input').value = selectedAddress.state;
    document.getElementById('complement-input').value = selectedAddress.complement;
};



function confirmPurchase() {
    var selectedOption = document.getElementById('address-select').value;
    var selectedAddressId = null;
    for (var i = 0; i < addresses.length; i++) {
        if (addresses[i].address === selectedOption) {
            selectedAddressId = addresses[i].id;
            break;
        }
    }

    return fetch(`/createOrder/`+selectedAddressId, {
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
            })
          .catch(error => {
            Swal.showValidationMessage(
              `Request failed: ${error}`
            )
          })
    }