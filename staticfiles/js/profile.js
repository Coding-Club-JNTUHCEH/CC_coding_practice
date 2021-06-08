window.addEventListener('DOMContentLoaded', (event) => {

    
    if ( document.getElementById("friend")!=null ){
        var username = document.getElementById("profileUsername").innerHTML;

        document.getElementById("friend").addEventListener("click", () => {
            
            if( document.getElementById("friend").value == "1") {
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
                            document.getElementById("friend").value  = "0";
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
                            document.getElementById("friend").value  = "1";
                        }
                    }
                    })
            }
        })
    }

    $('.removeFriend').on('click', function() {
        var username = $(this).val()
        console.log(username)
        $.ajax(
            {
                url : '/remove_friend_JSON/'+username ,
                method : 'GET' ,
                processData: false,
                contentType: false,
                success: function(status) {}
            })
            
        $(this).closest('tr').children('td').addClass('deleteHighlight').animate({
            padding: 0
        }).wrapInner('<div />').children().slideUp(function() {
            $(this).closest('tr').remove();
        });
        return false;
    });


});
