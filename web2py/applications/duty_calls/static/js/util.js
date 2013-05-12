
var add_user_table;   
function toggleAddUser(loc_name) {
    $('#add-user-div').toggle();
    
    if (!add_user_table) {
        add_user_table = $('#add-user-list').dataTable( {
            "bProcessing": true,
            "sAjaxSource": '/duty_calls/json/users.json',
            "aoColumnDefs": [
                { "bSearchable": false, "bVisible": false, "aTargets": [ 3 ] }
            ]
        });

        $('#add-user-list tbody').on( 'click', 'tr', function () {
            $(this).toggleClass('row_selected');
        } );
    }
}

function addSelectedUsers() {
    selected_rows = add_user_table.$('tr.row_selected');
    form = $('#add_users')
    for(var i=0; i<selected_rows.length; i++) {
        var position = add_user_table.fnGetPosition(selected_rows[i]);
        var uid = add_user_table.fnGetData(position)[3];
        form.append("<input type='checkbox' name='add_ids' value='" + uid + "' checked>");
    }
    return true;
}

$('#add_users').submit(addSelectedUsers);
