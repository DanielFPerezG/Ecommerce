document.addEventListener("DOMContentLoaded", function() {
    const applyCouponBtn = document.getElementById("applyCouponBtn");

    applyCouponBtn.addEventListener("click", function() {
        const couponCode = document.getElementById("couponInput").value;

        // Construir el objeto JSON para enviar en la solicitud POST
        const requestData = {
            cuponCode: couponCode,
            // Otros datos necesarios para la validación del cupón
        };

        fetch('validateCupon', {
            method: 'POST',
            body: JSON.stringify(requestData),
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrftoken,
            },
        })
        .then(response => response.json())
        .then(data => {
            // Realizar acciones basadas en la respuesta del servidor
            if (data.valid) {
                const subTotalElement = document.getElementById("subtotal");
                const totalElement = document.getElementById("total_price");
                const subTotalText = subTotalElement.textContent;
                const totalText = totalElement.textContent;

                const total = parseInt(totalText.replace(/[^0-9]/g, ""));
                const subTotal = parseInt(subTotalText.replace(/[^0-9]/g, ""));

                const discountValue = data.discountValue;
                const cuponDescription = data.cuponDescription;

                const newSubtotal = subTotal - (subTotal * (discountValue/100));
                const newTotal = total - (subTotal * (discountValue/100));


                subTotalElement.innerHTML = subTotalElement.innerHTML = `
                    <span class="original-price" style="text-decoration: line-through;">${subTotalElement.textContent.toLocaleString()}</span>
                    <span class="new-price">&nbsp;&nbsp;${newSubtotal.toLocaleString()}</span>`;
                totalElement.innerHTML = `
                    <span class="original-price" style="text-decoration: line-through;">${totalElement.textContent.toLocaleString()}</span>
                    <span class="new-price">&nbsp;&nbsp;${newTotal.toLocaleString()}</span>`;

                const couponResult = document.getElementById("couponResult");
                const couponContent = document.createElement("div");
                const couponInput = document.getElementById("couponInput");
                couponContent.classList.add("row");
                couponInput.disabled = true;
                applyCouponBtn.disabled = true;

                couponContent.innerHTML = `
                    <div class="col-11">
                        <div id="couponResult" class="text-muted pt-2">
                            <div>Cupón aplicado: ${cuponDescription}</div>
                        </div>
                    </div>
                    <div class="col-1 d-flex align-items-center justify-content-end">
                        <button class="btn btn-sm btn-danger ml-2" id="removeCouponBtn">
                            <i class="fa fa-times"></i>
                        </button>
                    </div>`;
                couponResult.innerHTML = ""; // Limpia el contenido previo
                couponResult.appendChild(couponContent);

                const removeCouponBtn = document.getElementById("removeCouponBtn");
                removeCouponBtn.addEventListener("click", function() {
                    // Realizar solicitud AJAX para eliminar el cupón
                    fetch('removeCupon', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-Requested-With': 'XMLHttpRequest',
                            'X-CSRFToken': csrftoken,
                        },
                    })
                    .then(response => {
                        window.location.href = checkoutURL;
                    })
                    .catch(error => {
                        console.error("Error al eliminar el cupón:", error);
                    });
                });
            } else {
                // Manejar el caso en que el cupón no sea válido
            }
        })
        .catch(error => {
            console.error("Error al procesar la solicitud:", error);
        });
    });
});