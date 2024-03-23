
$("#payment-methods").on("click", function() {
  const isMobile = window.innerWidth < 512;
  let widthPercentage;

  if (window.innerWidth >= 512 && window.innerWidth < 991) {
    widthPercentage = '80%';
  } else if (isMobile) {
    widthPercentage = '100%';
  } else {
    widthPercentage = '40%';
  }
  Swal.fire({
    title: '<strong style="text-align: center; display: block;">Medios de Pago</strong>',
    width: widthPercentage,
    html:
        '<div style="' +
        (isMobile
          ? 'text-align: center;'
          : 'display: flex; justify-content: space-between; align-items: center;') +
      '">' +
        '<div style="' +
          (isMobile
            ? 'margin-bottom: 20px;'
            : 'flex: 1; margin-right: 30px;') +
        '">' +
          '<img src="media/logo/bancolombia.png" alt="Bancolombia" class="img-fluid payment-logo rounded align-items-start align-content-start" style="max-width: 50%; height: auto; max-height: 100px; float: left; clear: left;">' +
          '<img src="media/logo/bancolombiaQR.png" alt="Código QR 1" style="max-width: 100%; height: auto; max-height: 300px;" />' +
          '<div class="text-left ml-3"><h5>Cuenta de Ahorros Bancolombia</h5>'+
          '<p>Numero de cuenta: 213424142</p>'+
          '<p>Titular: Geny Pérez</p></div>'+

        '</div>' +
        '<div style="' +
          (isMobile ? '' : 'flex: 1;') +
        '">' +
        '<img src="media/logo/daviplata.png" alt="Daviplata" class="img-fluid payment-logo rounded" style="max-width: 33%; height: auto; max-height: 100px; float: right; clear: right;">' +
          '<img src="media/logo/daviviendaQR.jpeg" alt="Código QR 2" style="max-width: 100%; height: auto; max-height: 300px;" />' +
        '<div class="text-left ml-3"><h5>Cuenta de Ahorros Digital Daviplata</h5>'+
          '<p>Numero de telefono: 3144009545</p>'+
          '<p>Titular: Geny Pérez</p></div>'+
        '</div>' +
      '</div>' +
       '<div style="display: flex; align-items: center; justify-content: center; margin-top: 20px;"> ' +
      '<img src="media/logo/nequi.png" alt="Nequi" style="width: 100px; height: 100px; margin-right: 10px;">' +
      '<h4 style="background-color: #2f2461; color: white; padding: 5px; border-radius: 5px;">3140009545</h4>' +
      '</div>' +
      '<p style="margin-top: 20px;">Para confirmar tu compra envia el comprobante de pago al <a href="https://wa.me/3207015028" target="_blank" style="color: green;">whatsapp: +57 320 7015028.</a> Una vez que confirmemos la recepción del dinero se procedera al envío del pedido.</p>'+
        '<p style="margin-top: 20px; font-size: 12px; color: grey;">*Si realizas la compra desde Honda-Tolima o Puerto Bogota-Cundinamarca solo debes enviar el valor total antes de envío. Los productos los llevaremos a la puerta de tu casa GRATIS.</p>',
    showCloseButton: true,
    confirmButtonText:
        'Entendido <i class="fa fa-thumbs-up"></i>',
    confirmButtonAriaLabel: 'Entendido',
  });
});


$("#payment-methods-button").on("click", function() {
    const isMobile = window.innerWidth < 512;
  let widthPercentage;

  if (window.innerWidth >= 512 && window.innerWidth < 991) {
    widthPercentage = '80%';
  } else if (isMobile) {
    widthPercentage = '100%';
  } else {
    widthPercentage = '40%';
  }
  Swal.fire({
    title: '<strong style="text-align: center; display: block;">Medios de Pago</strong>',
    width: widthPercentage,
    html:
        '<div style="' +
        (isMobile
          ? 'text-align: center;'
          : 'display: flex; justify-content: space-between; align-items: center;') +
      '">' +
        '<div style="' +
          (isMobile
            ? 'margin-bottom: 20px;'
            : 'flex: 1; margin-right: 30px;') +
        '">' +
          '<img src="media/logo/bancolombia.png" alt="Bancolombia" class="img-fluid payment-logo rounded align-items-start align-content-start" style="max-width: 50%; height: auto; max-height: 100px; float: left; clear: left;">' +
          '<img src="media/logo/bancolombiaQR.png" alt="Código QR 1" style="max-width: 100%; height: auto; max-height: 300px;" />' +
          '<div class="text-left ml-3"><h5>Cuenta de Ahorros Bancolombia</h5>'+
          '<p>Numero de cuenta: 213424142</p>'+
          '<p>Titular: Geny Pérez</p></div>'+

        '</div>' +
        '<div style="' +
          (isMobile ? '' : 'flex: 1;') +
        '">' +
        '<img src="media/logo/daviplata.png" alt="Daviplata" class="img-fluid payment-logo rounded" style="max-width: 33%; height: auto; max-height: 100px; float: right; clear: right;">' +
          '<img src="media/logo/daviviendaQR.jpeg" alt="Código QR 2" style="max-width: 100%; height: auto; max-height: 300px;" />' +
        '<div class="text-left ml-3"><h5>Cuenta de Ahorros Digital Daviplata</h5>'+
          '<p>Numero de telefono: 3144009545</p>'+
          '<p>Titular: Geny Pérez</p></div>'+
        '</div>' +
      '</div>' +
       '<div style="display: flex; align-items: center; justify-content: center; margin-top: 20px;"> ' +
      '<img src="media/logo/nequi.png" alt="Nequi" style="width: 100px; height: 100px; margin-right: 10px;">' +
      '<h4 style="background-color: #2f2461; color: white; padding: 5px; border-radius: 5px;">3140009545</h4>' +
      '</div>' +
      '<p style="margin-top: 20px;">Para confirmar tu compra envia el comprobante de pago al <a href="https://wa.me/3207015028" target="_blank" style="color: green;">whatsapp: +57 320 7015028.</a> Una vez que confirmemos la recepción del dinero se procedera al envío del pedido.</p>'+
        '<p style="margin-top: 20px; font-size: 12px; color: grey;">*Si realizas la compra desde Honda-Tolima o Puerto Bogota-Cundinamarca solo debes enviar el valor total antes de envío. Los productos los llevaremos a la puerta de tu casa GRATIS.</p>',
    showCloseButton: true,
    confirmButtonText:
        'Entendido <i class="fa fa-thumbs-up"></i>',
    confirmButtonAriaLabel: 'Entendido',
  });
});


// Event delegation to handle click events on dynamically added elements
$(document).on("click", ".payment-method-img", function() {
  const isMobile = window.innerWidth < 512;
  let widthPercentage;

  if (window.innerWidth >= 512 && window.innerWidth < 991) {
    widthPercentage = '80%';
  } else if (isMobile) {
    widthPercentage = '100%';
  } else {
    widthPercentage = '40%';
  }
  Swal.fire({
    title: '<strong style="text-align: center; display: block;">Medios de Pago</strong>',
    width: widthPercentage,
    html:
        '<div style="' +
        (isMobile
          ? 'text-align: center;'
          : 'display: flex; justify-content: space-between; align-items: center;') +
      '">' +
        '<div style="' +
          (isMobile
            ? 'margin-bottom: 20px;'
            : 'flex: 1; margin-right: 30px;') +
        '">' +
          '<img src="media/logo/bancolombia.png" alt="Bancolombia" class="img-fluid payment-logo rounded align-items-start align-content-start" style="max-width: 50%; height: auto; max-height: 100px; float: left; clear: left;">' +
          '<img src="media/logo/bancolombiaQR.png" alt="Código QR 1" style="max-width: 100%; height: auto; max-height: 300px;" />' +
          '<div class="text-left ml-3"><h5>Cuenta de Ahorros Bancolombia</h5>'+
          '<p>Numero de cuenta: 213424142</p>'+
          '<p>Titular: Geny Pérez</p></div>'+

        '</div>' +
        '<div style="' +
          (isMobile ? '' : 'flex: 1;') +
        '">' +
        '<img src="media/logo/daviplata.png" alt="Daviplata" class="img-fluid payment-logo rounded" style="max-width: 33%; height: auto; max-height: 100px; float: right; clear: right;">' +
          '<img src="media/logo/daviviendaQR.jpeg" alt="Código QR 2" style="max-width: 100%; height: auto; max-height: 300px;" />' +
        '<div class="text-left ml-3"><h5>Cuenta de Ahorros Digital Daviplata</h5>'+
          '<p>Numero de telefono: 3144009545</p>'+
          '<p>Titular: Geny Pérez</p></div>'+
        '</div>' +
      '</div>' +
       '<div style="display: flex; align-items: center; justify-content: center; margin-top: 20px;"> ' +
      '<img src="media/logo/nequi.png" alt="Nequi" style="width: 100px; height: 100px; margin-right: 10px;">' +
      '<h4 style="background-color: #2f2461; color: white; padding: 5px; border-radius: 5px;">3140009545</h4>' +
      '</div>' +
      '<p style="margin-top: 20px;">Para confirmar tu compra envia el comprobante de pago al <a href="https://wa.me/3207015028" target="_blank" style="color: green;">whatsapp: +57 320 7015028.</a> Una vez que confirmemos la recepción del dinero se procedera al envío del pedido.</p>'+
        '<p style="margin-top: 20px; font-size: 12px; color: grey;">*Si realizas la compra desde Honda-Tolima o Puerto Bogota-Cundinamarca solo debes enviar el valor total antes de envío. Los productos los llevaremos a la puerta de tu casa GRATIS.</p>',
    showCloseButton: true,
    confirmButtonText:
        'Entendido <i class="fa fa-thumbs-up"></i>',
    confirmButtonAriaLabel: 'Entendido',
  });
});