let que = document.querySelector('#question')
function name_select(){
    que.addEventListener('keypress', (target) =>{
        if (target.key == 'Enter'){
            fetch(window.location.href, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    "column": "user_name",
                    "value": que.value
                }),
            })
            .then(res => res.json())
            .then(result => {
                let url = (window.location.protocol + "//" + window.location.host + window.location.pathname + `?page=${result['user_page']}`)
                window.location.href = url
            })
        }
    })
}

name_select()