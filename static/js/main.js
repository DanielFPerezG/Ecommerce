(function ($) {
    "use strict";
    
    // Dropdown on mouse hover
    $(document).ready(function () {
        function toggleNavbarMethod() {
            if ($(window).width() > 992) {
                $('.navbar .dropdown').on('mouseover', function () {
                    $('.dropdown-toggle', this).trigger('click');
                }).on('mouseout', function () {
                    $('.dropdown-toggle', this).trigger('click').blur();
                });
            } else {
                $('.navbar .dropdown').off('mouseover').off('mouseout');
            }
        }
        toggleNavbarMethod();
        $(window).resize(toggleNavbarMethod);
    });
    
    
    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 100) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });
    


    // Vendor carousel
    $('.vendor-carousel').owlCarousel({
        loop: true,
        margin: 29,
        nav: false,
        autoplay: true,
        smartSpeed: 1000,
        responsive: {
            0:{
                items:2
            },
            576:{
                items:3
            },
            768:{
                items:4
            },
            992:{
                items:5
            },
            1200:{
                items:6
            }
        }
    });


    // Related carousel
    $('.related-carousel').owlCarousel({
        loop: true,
        margin: 29,
        nav: false,
        autoplay: true,
        smartSpeed: 1000,
        responsive: {
            0:{
                items:1
            },
            576:{
                items:2
            },
            768:{
                items:3
            },
            992:{
                items:4
            }
        }
    });


    // Product Quantity

    $('.quantity button').on('click', function () {
        var button = $(this);
        var oldValue = button.parent().parent().find('input').val();
        if (button.hasClass('btn-plus')) {
            var newVal = parseFloat(oldValue) + 1;
        } else {
            if (oldValue > 0) {
                var newVal = parseFloat(oldValue) - 1;
            } else {
                newVal = 0;
            }
        }
        button.parent().parent().find('input').val(newVal);
        total_price();
    });

    // Seleccionar la tabla y sus filas
    total_price();
    function total_price (){
        const table = document.getElementById("CartTable");
        const rows = table.getElementsByTagName("tr");
        const sub_total = document.getElementById("subtotal")
        const total_price = document.getElementById("total_price");
        let totalPrice = 0;
      // Iterar por cada fila, omitiendo la fila de encabezado
      for (let i = 1; i < rows.length; i++) {
        const row = rows[i];

        // Obtener los valores de las columnas "precio" y "cantidad"
        const price = parseInt(row.cells[1].textContent);
        const quantity = parseInt(row.cells[2].querySelector('input').value);
        // Calcular el valor total
        const total = price * quantity;
        totalPrice += total;

        // Actualizar la columna "total" con el valor calculado
        row.cells[3].textContent = total;
        sub_total.textContent = totalPrice;
        total_price.textContent = totalPrice + 10000;

      }

    }



    //Data table
    $(document).ready(function() {
        $('#table-data-model').DataTable({
            responsive: true
        });
        
    });

})(jQuery);