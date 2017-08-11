const TRAIN_URL = "http://localhost:5000/train"
const PENDING_REQ_URL = "http://localhost:5000/getPending"
const FINISHED_REQ_URL = "http://localhost:5000/getDone"

$(document).ready(function(){
    populateRequestsList();
    addItemClickListener();
    submitTrainCSVFile();
    // Refresh list of requests every certain amount of time
    refreshReqList();    

});

function refreshReqList(){
    setTimeout(function(){
        if($('#reqModal').hasClass('in')==false){
            window.location.reload();
        }
    },8000);

    
}

function submitTrainCSVFile(){
    $('#uploadFile').submit(function(e){ 
        e.preventDefault();
        var formData = new FormData(this);
        $.ajax({
            url: TRAIN_URL,
            type: 'POST',
            data : formData,
            contentType: false,
            processData: false,
            success: function(responseData, textStatus, jqXHR) {
                    console.log(responseData);
                    if(responseData!=null){
                        var msg = 'There was a problem with your request.';
                        if (responseData != 'not ok')
                            msg = 'Request created! Your request ID is <code>'+responseData+'</code>';
                        $('#new-req-msg').html(msg);
                        populateRequestsList();

                    }
            },
            error: function (responseData, textStatus, errorThrown) {
                console.log(' Error: '+errorThrown + ". Status: "+textStatus);

            }
        });

        return false;

    });
}

function populateRequestsList(){
    
    $.ajax({
            url: PENDING_REQ_URL,
            type: 'GET',
            contentType: false,
            processData: false,
            success: function(responseData, textStatus, jqXHR) {
                    if(responseData!=null){
                        var list = $('#request-list');
                        var pendingReqs = responseData.results;
                        var temp = '';
                        for(var i=0;i<pendingReqs.length;i++){
                            temp+='<a data-toggle="tooltip" data-placement="right" title="Request in progress. Please wait." class="list-group-item list-group-item-warning">'+pendingReqs[i]+'</a>'
                        }
                        list.empty().append(temp); 
                    }
                    $('[data-toggle="tooltip"]').tooltip(); 
                    console.log(responseData.results);
                    
            },
            error: function (responseData, textStatus, errorThrown) {
                console.log(' Error: '+errorThrown + ". Status: "+textStatus);
            }

        });
        $.ajax({
            url: FINISHED_REQ_URL,
            type: 'GET',
            contentType: false,
            processData: false,
            success: function(responseData, textStatus, jqXHR) {
                    if(responseData!=null){
                        var list = $('#request-list');
                        var doneReqs = responseData.results;
                        var temp = '';
                        for(var i=0;i<doneReqs.length;i++){
                            temp+='<a href="../models/models.html" class="list-group-item list-group-item-success">'+doneReqs[i]+'</a>'
                            if(addItemClickListener(doneReqs[i])==false){
                                if($('#request-list a').length ==0 || !checkIfRequestInList(doneReqs[i]))
                                    temp+='<a href="../models/models.html" class="list-group-item list-group-item-success">'+doneReqs[i]+'</a>'
                                alert('new');
                            }
                        }
                        list.append(temp); 
                    }
                    
                    console.log(responseData.results);
                    addItemClickListener();
                    
            },
            error: function (responseData, textStatus, errorThrown) {
                console.log(' Error: '+errorThrown + ". Status: "+textStatus);
            }

        });
}



function addItemClickListener(){
    $('.list-group-item-success').click(function(e) {
        $(this).addClass('active').siblings().removeClass('active');
        sessionStorage.setItem('current_req_id', $(this).text());
    });
    
}

function checkIfRequestInList(reqId) {
    return $("#request-list a").filter(function(i, a2) {
        return $(a2).text() == reqId;
    }).length > 0;
};