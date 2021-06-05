window.addEventListener('DOMContentLoaded', (event) => {

    var username = document.getElementById("profileUsername").innerHTML;
    
    document.getElementById("friend").addEventListener("click", () => {
        
        if( document.getElementById("friend").innerHTML == "Add Friend") {
            $.ajax(
                {
                url : '/add_friend_JSON/'+username ,
                method : 'GET' ,
                processData: false,
                contentType: false,
                success: function(status) {
                    if ( status["status"] == 0 ) {
                        document.getElementById("friend").innerHTML  = "Unfriend";
                        document.getElementById("friend").className = "btn btn-danger d-btn";
                    }
                }
                })
        }
        else {
            $.ajax(
                {
                url : '/remove_friend_JSON/'+username ,
                method : 'GET' ,
                processData: false,
                contentType: false,
                success: function(status) {
                    if ( status["status"] == 0 ) {
                        document.getElementById("friend").innerHTML  = "Add Friend";
                        document.getElementById("friend").className = "btn btn-warning d-btn";
                    }
                }
                })
        }
    })


});
