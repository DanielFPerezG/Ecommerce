function loadJSON(callback) {
	var xobj = new XMLHttpRequest();
	xobj.overrideMimeType("application/json");
	xobj.open("GET", "/static/store/json/colombia.json", true);
	xobj.onreadystatechange = function () {
		if (xobj.readyState == 4 && xobj.status == "200") {
			callback(xobj.responseText);
		}
	};
	xobj.send(null);
}

function createAddress(userId) {
  loadJSON(function (response) {
    // Parse JSON string into object
    var colombiaJson = JSON.parse(response);
    var address, city, state, complement;
    Swal.fire({
      title: 'Ingrese la dirección de su residencia',
      html: '<div class="form-group">' +
    '<label for="address">Dirección</label>' +
    '<input id="address" class="form-control" placeholder="Dirección">' +
    '</div>' +
    '<div class="form-row">' +
    '<div class="form-group col-md-6">' +
    '<label for="state">Departamento</label>' +
    '<select id="state" class="form-control">' +
    '<option value="">Departamento</option>' +
    '</select>' +
    '</div>' +
    '<div class="form-group col-md-6">' +
    '<label for="city">Ciudad</label>' +
    '<select id="city" class="form-control" disabled>' +
    '<option value="">Ciudad</option>' +
    '</select>' +
    '</div>' +
    '</div>' +
    '<div class="form-group">' +
    '<label for="complement">Complemento</label>' +
    '<input id="complement" class="form-control" placeholder="Complemento">' +
    '</div>',
      focusConfirm: false,
      showCancelButton: true,
      cancelButtonText: 'Cancelar',
      preConfirm: () => {
        address = Swal.getPopup().querySelector('#address').value;
        state = Swal.getPopup().querySelector('#state').value;
        city = Swal.getPopup().querySelector('#city').value;
        complement = Swal.getPopup().querySelector('#complement').value;

        return fetch(`/createAddress`, {
            method: 'POST',
            body: JSON.stringify({ 'address': address, 'state': state, 'city': city, 'complement': complement }),
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
      allowOutsideClick: false,
      didOpen: () => {
        const stateSelect = Swal.getPopup().querySelector('#state');
        const citySelect = Swal.getPopup().querySelector('#city');

        // Filling the status drop-down menu
        colombiaJson.forEach((department) => {
          const option = document.createElement('option');
          option.value = department.departamento;
          option.text = department.departamento;
          stateSelect.appendChild(option);
        });

        // Update cities when a state is selected
        stateSelect.addEventListener('change', () => {
          const selectedState = stateSelect.value;

          // Clear the drop-down menu of cities
          citySelect.innerHTML = '<option value="">Seleccione una ciudad</option>';

          // Get the cities corresponding to the selected department
          const selectedDepartment = colombiaJson.find((department) => department.departamento === selectedState);
          if (selectedDepartment) {
            selectedDepartment.ciudades.forEach((city) => {
              const option = document.createElement('option');
              option.value = city;
              option.text = city;
              citySelect.appendChild(option);
            });
          }

          // Enable or disable the drop-down menu of cities according to the state selection
          citySelect.disabled = selectedState === '';


        });
      }
    }).then((result) => {
      if (result.isConfirmed) {
        Swal.fire({
      position: 'top-end',
      icon: 'success',
      title: 'Has registrado la dirección con exito',
      showConfirmButton: false,
      timer: 1500
    });
        const addressContainer = document.getElementById('addressContainer');

        var additionalContent = `<div class="card-body"><div class="d-flex align-items-center"><div class="mr-3"><i class="fa fa-map-marker fa-2x fa-gray-color" aria-hidden="true"></i></div><div class="text-left"><span class="text-dark">${address}</span><br><span class="text-muted small">${state}</span><span class="text-muted small"> - </span><span class="text-muted small">${city}</span><br><span class="text-muted small">${complement}</span></div></div></div>`;

        console.log(additionalContent)
        //add address info
          addressContainer.insertAdjacentHTML('afterbegin', additionalContent)
      }
    });
  });
}


