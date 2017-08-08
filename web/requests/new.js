const TRAIN_URL = "http://localhost:5000/train"
const PENDING_REQ_URL = "http://localhost:5000/getPending"

$(document).ready(function(){
    populateRequestList();

    $('#uploadFile').submit(function(e){ 
        e.preventDefault()
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
                        $('#new-req-msg').html('Request created! Your request ID is <code>'+responseData+'</code>')
                    }
                    
            },
            error: function (responseData, textStatus, errorThrown) {
                console.log(' Error: '+errorThrown + ". Status: "+textStatus);
                
            }

        });

    });


    
    

});







function populateRequestList(){
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
                            temp+='<li class="list-group-item">'+pendingReqs[i]+'</li>'
                        }
                        list.empty().append(temp); 
                    }
                    
                    console.log(responseData.results);
                    
            },
            error: function (responseData, textStatus, errorThrown) {
                console.log(' Error: '+errorThrown + ". Status: "+textStatus);
            }

        });
}