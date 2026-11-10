// Shows a focus ring on the PDF frame while keyboard focus is inside it.
// Browsers do not match :focus or :focus-within on an <iframe> once focus
// has moved into the frame's document, so a CSS outline alone never shows.
// When focus enters the frame, this window loses focus and the frame
// becomes document.activeElement; the class follows that.
(function () {
  "use strict";
  var frame = document.querySelector(".pdf-frame");
  if (!frame) return;
  function update() {
    frame.classList.toggle("has-focus", document.activeElement === frame);
  }
  window.addEventListener("blur", function () { setTimeout(update, 0); });
  window.addEventListener("focus", update);
  document.addEventListener("focusin", update);
})();
