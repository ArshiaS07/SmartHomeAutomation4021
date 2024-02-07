window.onload = function() {
  const checkbox2 = document.getElementById("waterDigital");
  const slider2 = document.getElementById("waterAnolog");
  const waterValve = document.getElementById("water");

  checkbox2.addEventListener("change", function() {
    if (this.checked) {
      slider2.disabled = false;
      waterValve.disabled = true;
      waterValve.checked = false;
    } else {
      slider2.disabled = true;
      waterValve.disabled = false;
    }
  });
};
