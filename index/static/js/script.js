

window.addEventListener('DOMContentLoaded', (event) => {

    const search = document.getElementById("username")
    const matchList = document.getElementById("match-list")
    const theme = document.getElementById("darkMode")
    const logo = document.getElementById("CClogo")
    setTheme();

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

    // day mode   =  false
    // night mode =  true
    theme.addEventListener("click",() => {

        changeTheme();
        var mode = theme.checked;
        localStorage.setItem("theme",mode)
        
    });
    function changeTheme() {
        var element = document.body;
        element.classList.toggle("dark");
        if (!logo.src.match("dark")){
            logo.src = darkLogo
        }
        else {
            logo.src = lightlogo
        }

    }

    function setTheme() {
        var theme = localStorage.getItem("theme")
        console.log(theme)
        if(theme === 'true') {
            document.getElementById("darkMode").checked = theme;
            changeTheme();
            
        }
    }

    
});
 
