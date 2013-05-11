function populateAllUsers(loc_name) {
    $.getJSON('/duty_calls/json/users.json', function(data) {
        var items = [];
        var list = $("#add-user-list")
        
        items.push("<form name='add_users' method=POST action='" + loc_name + "/add'>");
        items.push('<table>');
        items.push('<tr>');
        items.push('<td>' + "Select" + '</td>');
        items.push('<td>' + "User ID" + '</td>');
        items.push('<td>' + "Name" + '</td>');
        items.push('<td>' + "Phone" + '</td>');
        items.push('<td>' + "Email" + '</td>');
        items.push('</tr>');
        $.each(data['users'], function(uid, user_data) {
            items.push('<tr>');
            items.push('<td>' + "<input type=checkbox name='add_ids' value='" + uid + "'>" + '</td>');
            items.push('<td>' + uid + '</td>');
            items.push('<td>' + user_data['name'] + '</td>');
            items.push('<td>' + user_data['phone'] + '</td>');
            items.push('<td>' + user_data['email'] + '</td>');
            items.push('</tr>');
        });
        items.push('</table>')
        items.push("<input type=submit value='Add Selected Users'>")
        items.push('</form>')

        var html = '';
        for(i=0; i<items.length; i++) {
            //list.append(items[i]);
            html = html + items[i];
        }
        list.html(html);
    });
}

var user_table;   
function toggleAddUser(loc_name) {
        
    $('#add-user-div').toggle();
    
    if (!user_table) {
        user_table = $('#add-user-list').dataTable( {
            "bProcessing": true,
            "sAjaxSource": '/duty_calls/json/users.json',
        });

        $('#add-user-list tbody').on( 'click', 'tr', function () {
            $(this).toggleClass('row_selected');
        } );
    }
}
