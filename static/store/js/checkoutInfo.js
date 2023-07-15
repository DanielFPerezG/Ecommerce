$(document).ready(function() {
  function showTooltip() {
    var infoIcon = $("#info-icon");
    var tooltipText = "La información proporcionada sera utilizada por parte del Edjo exclusivamente para el envio de los productos seleccionados con la empresa 'Interrapidisimo'.";

    infoIcon.on("mouseover", function() {
      var tooltip = $("<div>")
        .addClass("tooltip-text")
        .text(tooltipText)
        .appendTo("body");

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

  showTooltip();
});
