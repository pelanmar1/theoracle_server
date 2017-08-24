var picker;
var current_req_mod_id;
const PREDICT_URL = "http://localhost:5000/predict/"




$(document).ready(function(e){
    $('#alert_msg').hide(); 
    current_req_mod_id = getCurrentReqModId();
    picker = setupDatePicker("#datepicker");
    setCurrentReqModId();
    setupPredict();
});

function setupDatePicker(selector){
    var options = {
        mode: "multiple",
        dateFormat: "Y-m-d"
    }
    return $(selector).flatpickr(options);
    
    
}
function setCurrentReqModId(){
    $('#curr_req_model_id').text(getCurrentReqModId());
}

function getCurrentReqModId(){
    current_req_mod_id = sessionStorage.getItem('current_req_mod_id');    
    if(current_req_mod_id!= null){
        return current_req_mod_id;
    }
    else
        return ""
}

function getDPSelectedValues(){
    var temp = []
    if(picker!=null){
        for(var i=0;i<picker.selectedDates.length;i++)
            temp.push(picker.selectedDates[i].toISOString().slice(0,10));
        return temp;
        
    }
    else 
        return [];
}



function setupPredict(){
    $('#predict').click(function(e){
        var values = getDPSelectedValues();
        var reqId = getCurrentReqModId()
        if( reqId != null && reqId.length==0){
            return;
        }
        if(values==null || values.length==0)
            $('#alert_msg').show();
        else
            $('#alert_msg').hide();

        req={'values':values}

        $.ajax({
            url: PREDICT_URL+reqId,
            type: 'POST',
            data : JSON.stringify(req),
            contentType: 'application/x-www-form-urlencoded',
            dataType:'',
            processData: 'false',
            success: function(responseData, textStatus, jqXHR) {
                console.log(responseData);
                if(responseData!=null&&responseData.resTable!=null){
                    $('#res-table').html(responseData.resTable);
                }
            },
            error: function (responseData, textStatus, errorThrown) {
                console.log(' Error: '+errorThrown + ". Status: "+textStatus);

            }
        });
        
            

    });
}



