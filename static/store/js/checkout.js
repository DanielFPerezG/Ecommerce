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



