window.onload = function() {
  const checkbox1 = document.getElementById("myCheckbox");
  const slider1 = document.getElementById("mySlider");
  const lightSwitch = document.getElementById("light");

  checkbox1.addEventListener("change", function() {
    if (this.checked) {
      slider1.disabled = false;
      lightSwitch.disabled = true;
      lightSwitch.checked = false;
    } else {
      slider1.disabled = true;
      lightSwitch.disabled = false;
    }
  });

  const checkbox2 = document.getElementById("gasDigital");
  const slider2 = document.getElementById("gasAnolog");
  const gasValve = document.getElementById("gas");

  checkbox2.addEventListener("change", function() {
    if (this.checked) {
      slider2.disabled = false;
      gasValve.disabled = true;
      gasValve.checked = false;
    } else {
      slider2.disabled = true;
      gasValve.disabled = false;
    }
  });

  const checkbox3 = document.getElementById("waterDigital");
  const slider3 = document.getElementById("waterAnolog");
  const waterValve = document.getElementById("water");

  checkbox3.addEventListener("change", function() {
    if (this.checked) {
      slider3.disabled = false;
      waterValve.disabled = true;
      waterValve.checked = false;
    } else {
      slider3.disabled = true;
      waterValve.disabled = false;
    }
  });
};
