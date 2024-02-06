window.onload = function() {
  const checkbox3 = document.getElementById("gasDigital");
  const slider3 = document.getElementById("gasAnolog");
  const gasValve = document.getElementById("gas");

  checkbox3.addEventListener("change", function() {
    if (this.checked) {
      slider3.disabled = false;
      gasValve.disabled = true;
      gasValve.checked = false;
    } else {
      slider3.disabled = true;
      gasValve.disabled = false;
    }
  });
};
