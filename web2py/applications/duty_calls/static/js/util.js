var add_user_table;   
function toggleAddUser(loc_name) {
    $('#add-user-div').toggle();
    
    if (!add_user_table) {
        add_user_table = $('#add-user-list').dataTable( {
            "bProcessing": true,
            "sAjaxSource": '/duty_calls/json/users.json',
            "aoColumnDefs": [
                { "bSearchable": false, "bVisible": false, "aTargets": [ 3 ] },
                { "bSearchable": false, "bVisible": false, "aTargets": [ 4 ] },
                { "bSearchable": false, "bVisible": false, "aTargets": [ 5 ] }
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
        var uid = add_user_table.fnGetData(position)[5];
        form.append("<input type='checkbox' name='add_ids' value='" + uid + "' checked>");
    }
    return true;
}

var remove_user_table;
function showRemoveUserTable(loc_name) {
    remove_user_table = $('#remove-user-list').dataTable( {
        "bProcessing": true,
        "sAjaxSource": '/duty_calls/json/users.json/'+loc_name,
        "aoColumnDefs": [
            { "bSearchable": false, "bVisible": false, "aTargets": [ 3 ] },
            { "bSearchable": false, "bVisible": false, "aTargets": [ 4 ] },
            { "bSearchable": false, "bVisible": false, "aTargets": [ 5 ] }
        ]
    });

    $('#remove-user-list tbody').on( 'click', 'tr', function () {
        $(this).toggleClass('row_selected');
    } );
}

function removeSelectedUsers() {
    selected_rows = remove_user_table.$('tr.row_selected');
    form = $('#remove_users');
    for(var i=0; i<selected_rows.length; i++) {
        var position = remove_user_table.fnGetPosition(selected_rows[i]);
        var uid = remove_user_table.fnGetData(position)[5]; // get the uid of the user to be removed
        form.append("<input type='checkbox' name='remove_ids' value='" + uid + "' checked>");
    }
    return true;
}

editing = false;
function editInfo(loc_name) {
    if (!editing) {
        curr_fail_name = $('#fail_name').text();
        curr_fail_num = $('#fail_num').text();
        curr_is_rl = $('#is_rl').text();
        curr_forwarding_id = $('#forwarding_id').text();
        curr_calendar_url = $('#calendar_url').text();

        if (curr_is_rl == "False") { is_rl = false; }
        else { is_rl = true; }

        var f = document.createElement("form");
        f.setAttribute('method',"POST");
        f.setAttribute('action',"/duty_calls/admin/locations/"+loc_name+"/update");

        var span_fail_name = document.createElement("span");
        span_fail_name.innerHTML = "Fail Name: "
        var input_fail_name = document.createElement("input"); 
        input_fail_name.setAttribute('type',"text");
        input_fail_name.setAttribute('name',"fail_name");
        input_fail_name.setAttribute('value', curr_fail_name);
        
        var span_fail_num = document.createElement("span");
        span_fail_num.innerHTML = "Fail Number: "
        var input_fail_num = document.createElement("input");
        input_fail_num.setAttribute('type',"text");
        input_fail_num.setAttribute('name',"fail_num");
        input_fail_num.setAttribute('value', curr_fail_num);
        
        var span_is_rl = document.createElement("span");
        span_is_rl.innerHTML = "Is Res Life? ";
        var input_is_rl = document.createElement("input"); 
        input_is_rl.setAttribute('type',"checkbox");
        input_is_rl.setAttribute('name',"is_res_life");
        input_is_rl.setAttribute('value', "true");
        if (is_rl) {
            input_is_rl.setAttribute('checked',"true");
        }
        
        var span_forwarding_id = document.createElement("span");
        span_forwarding_id.innerHTML = "Twilio Forwarding ID: "
        var input_forwarding_id = document.createElement("input");
        input_forwarding_id.setAttribute('type',"text");
        input_forwarding_id.setAttribute('name',"forwarding_id");
        input_forwarding_id.setAttribute('value', curr_forwarding_id);

        var span_calendar_url = document.createElement("span");
        span_calendar_url.innerHTML = "Duty Calendar URL: "
        var input_calendar_url = document.createElement("input");
        input_calendar_url.setAttribute('type',"text");
        input_calendar_url.setAttribute('name',"calendar_url");
        input_calendar_url.setAttribute('value', curr_calendar_url);

        var submit = document.createElement("input");
        submit.setAttribute('type', "submit");
        submit.setAttribute('value', "Update Location Info");

        f.appendChild(span_fail_name);
        f.appendChild(document.createElement('br'));
        f.appendChild(input_fail_name);
        f.appendChild(document.createElement('br'));

        f.appendChild(span_fail_num);
        f.appendChild(document.createElement('br'));
        f.appendChild(input_fail_num);
        f.appendChild(document.createElement('br'));

        f.appendChild(span_is_rl);
        f.appendChild(document.createElement('br'));
        f.appendChild(input_is_rl);
        f.appendChild(document.createElement('br'));
        f.appendChild(document.createElement('br'));
    
        f.appendChild(span_forwarding_id);
        f.appendChild(document.createElement('br'));
        f.appendChild(input_forwarding_id);
        f.appendChild(document.createElement('br'));

        f.appendChild(span_calendar_url);
        f.appendChild(document.createElement('br'));
        f.appendChild(input_calendar_url);
        f.appendChild(document.createElement('br'));
        f.appendChild(document.createElement('br'));

        f.appendChild(submit);
        f.appendChild(document.createElement('br'));
        f.appendChild(document.createElement('br'));
        f.appendChild(document.createElement('br'));
        
        $('#location_info').html(f);
        editing = true;
    }
    
    else {
        location.reload();
    }   

}
