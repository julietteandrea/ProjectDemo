/* JS for homepage.html */
function mypw() {
    var x = document.getElementById("pwhomepage");
    if (x.type === "password") {
        x.type = "text";
    } else {
        x.type = "password";
    }
}
