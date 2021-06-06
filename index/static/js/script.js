window.addEventListener('DOMContentLoaded', (event) => {
    console.log("in index/js outside")
    document.getElementById("username").addEventListener("input",() => {
        $.ajax(
            {
            url : '/find_users_JSON/'+ document.getElementById("username").value,
            method : 'GET' ,
            processData: false,
            contentType: false,
            success: function(data){
                console.log(data["usernames"])
                
            }
           
            })
        
    })
   
});