/* JS for homepage.html */
function mypw() {
    var x = document.getElementById("pwhomepage");
    if (x.type === "password") {
        x.type = "text";
    } else {
        x.type = "password";
    }
}


// Get the modal
var modal = document.getElementById('id01');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

var i = 0;
var txt = 'Welcome to Trifecta!';
var speed = 50;

function typeWriter() {
  if (i < txt.length) {
    document.getElementById("demo").innerHTML += txt.charAt(i);
    i++;
    setTimeout(typeWriter, speed);
  }
}