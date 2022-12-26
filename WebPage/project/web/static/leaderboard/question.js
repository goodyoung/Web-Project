let que = document.querySelector('#question')
que.addEventListener('keypress', (target) =>{
    console.log(target)
    if (target.key == 'Enter'){
        try{

            fetch(window.location.href, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    "column": "user_name",
                    "value": que.value ? que.value : ''
                }),
            })
            
            .then(res => res.json())
            .then(result => {
                let url = (window.location.protocol + "//" + window.location.host + window.location.pathname + `?page=${result['user_page']}`)
                window.location.href = url
            })

        } catch(error){
            alert('이름 오류')
        }
        
    }
})
