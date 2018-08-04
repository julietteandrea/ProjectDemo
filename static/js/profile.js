// Get the modal
var modal = document.getElementById('myModal');

// Get the button that opens the modal
var btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal 
btn.onclick = function() {
    modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

function msg(evt) {
    alert("Call Deleted");
    evt,preventDefault();
}
    
//Tell browser what to call when the page is ready to be viewed
$(document).ready( 
    //Call this anonymous function
    function () {
        //Create a DataTable
        var data_table = $('#calllog_table').DataTable(
            {
                "order": [[ 0, "desc" ]]
            });
        //var column = data_table.columns(0);
        //column.visible(false);
    } 
);
