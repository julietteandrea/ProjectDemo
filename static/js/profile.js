// Delete button in table
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
                "order": [[ 0, "asc" ]]
            });
        //var column = data_table.columns(0);
        //column.visible(false);
    } 
);