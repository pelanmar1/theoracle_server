const TRAIN_CSV_URL = "http://localhost:5000/getTrainHTML/"
const RES_DF_URL = "http://localhost:5000/getResultsHTML/"
const MODEL_IMG_URL ="http://localhost:5000/getModelImage/"

var current_req_id = sessionStorage.getItem('current_req_id');
$(document).ready(function(){
    setCurrentReqIdTitle()
    loadTrainingDataCSVs()
    loadResultsDataFrames()
    
    
});


function setCurrentReqIdTitle(){
    $('#curr_req_id').text(getCurrentReqId());
}

function loadTrainingDataCSVs(){
    $.ajax({
        url: TRAIN_CSV_URL+getCurrentReqId(),
        type: 'GET',
        contentType: false,
        processData: false,
        success: function(responseData, textStatus, jqXHR) {
                if(responseData!=null&&responseData.trainCSV!=null){
                    $('#csv-table').html(responseData.trainCSV)
                }
                
        },
        error: function (responseData, textStatus, errorThrown) {
            console.log(' Error: '+errorThrown + ". Status: "+textStatus);

        }

    });
}

function loadResultsDataFrames(){
    $.ajax({
        url: RES_DF_URL+getCurrentReqId(),
        type: 'GET',
        contentType: false,
        processData: false,
        success: function(responseData, textStatus, jqXHR) {
                if(responseData!=null&&responseData.resTable!=null){
                    $('#res-table').html(responseData.resTable);
                    setTableRowClickListener();
                }
                
        },
        error: function (responseData, textStatus, errorThrown) {
            console.log(' Error: '+errorThrown + ". Status: "+textStatus);

        }

    });
}

function getCurrentReqId(){
    if(current_req_id!= null){
        return current_req_id;
    }
    else
        return ""
}

function setTableRowClickListener(){
    $('#res-table tr').click(function(e){
        var model_id = $(this).find('td').eq(0).text();
        var req_id = getCurrentReqId();
        $("#res-table tr").each(function () {
                $(this).attr("class", "");
        });
        $(this).attr("class", "active");
        buildImageModal(req_id,model_id);
    });
}

function buildImageModal(rid,mid){
    var imgSrc,imgTitle;
    if(rid!=null && mid!=null){
        mid = parseInt(mid);
        imgTitle = rid+'/'+mid;
        imgSrc = MODEL_IMG_URL+imgTitle;
    }else{
        imgTitle = 'File not found.';
        imgSrc = '../res/img/not_found.jpg';
    }
    $('#modal-image').attr('src',imgSrc);
    $('#modal-title').text(imgTitle);
    $('#graphModal').modal();

}
