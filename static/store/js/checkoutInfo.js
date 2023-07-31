$(document).ready(function() {
  function showTooltip(iconId, tooltipText, extraClass) {
    var infoIcon = $(iconId);

    infoIcon.on("mouseover", function() {
      var tooltip = $("<div>")
        .addClass("tooltip-text")
        .text(tooltipText)
        .appendTo("body");

      if (extraClass) {
        tooltip.addClass(extraClass); // Agrega la clase adicional específica para el tooltip de recuperar contraseña
      }

      var tooltipWidth = tooltip.outerWidth();
      var tooltipHeight = tooltip.outerHeight();
      var iconOffset = infoIcon.offset();

      var leftPosition = iconOffset.left - tooltipWidth - 10;

      if (leftPosition < 0) {
        leftPosition = iconOffset.left + infoIcon.outerWidth() + 10;
      }

      tooltip.css({
        top: iconOffset.top + infoIcon.outerHeight(),
        left: leftPosition,
      });
    });

    infoIcon.on("mouseout", function() {
      $(".tooltip-text").remove();
    });
  }

  // Llama la función showTooltip para el primer tooltip
  var tooltipTextCheckout = "La información proporcionada será utilizada por parte del Edjo exclusivamente para el envío de los productos seleccionados con la empresa 'Interrapidisimo'.";
  showTooltip("#info-icon", tooltipTextCheckout);

  // Llama la función showTooltip para el segundo tooltip y agrega la clase "tooltip-reset-password"
  var tooltipTextResetPassword = "Introduce tu correo electrónico y te enviaremos un enlace para restablecer tu contraseña.";
  showTooltip("#info-icon-reset-password", tooltipTextResetPassword, "tooltip-reset-password");
});