

window.addEventListener('DOMContentLoaded', (event) => {

    const search = document.getElementById("username")
    const matchList = document.getElementById("match-list")

    const searchUsers = async searchText => {
        let users = []
        if( searchText.length != 0) {
            const res = await fetch('/find_users_JSON/'+ searchText);
            const users_json = await res.json();
            users = users_json.usernames
        }
        // console.log(users)
        outputHtml(users);
        
    };
    const outputHtml = users => {
         {
            const html = users.map( user => `
                <div class = "card card-body">
                    ${user}
                </div>
            `).join('');
            matchList.innerHTML = html;
        }
    }
    search.addEventListener("input", () => searchUsers(search.value))


    document.getElementById("darkMode").addEventListener("click",() => {

        var element = document.body;
        element.classList.toggle("dark");

    });

    
});
 
