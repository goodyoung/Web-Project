const modifyName = document.getElementById('myinfomodify_name');
const modifyNickname = document.getElementById('myinfomodify_nickname');
const modifyPassword = document.getElementById('myinfomodify_password');

function modify_name_recusion(target) {            
    const original = target.parentNode.innerHTML;
    let user_name = document.querySelector('.myinfomodify_content_sub').innerText
    target.parentNode.firstElementChild.innerHTML = `<input type="text" id="name_input" value = '${user_name}'/>`;        
    target.parentNode.lastElementChild.value = "확인";
    target.parentNode.lastElementChild.id = "myinfomodify_confirm";
    const modify_confirm = target.parentNode.lastElementChild;
    const modify_cancel = target.parentNode.lastElementChild.cloneNode();
    modify_cancel.value = '취소';
    modify_cancel.id = 'myinfomodify_cancel';        
    target.parentNode.appendChild(modify_cancel);    

    modify_confirm.addEventListener('click',({target}) => {       
        fetch(window.location.href, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                "column": "name",
                "value": document.querySelector("#name_input").value
            }),
            });

        target.parentNode.innerHTML = original;

        document.querySelector("#myinfomodify_name").addEventListener('click', ({target}) => {
            modify_name_recusion(target)
        }, { once: true })  

        window.location.reload()

    }, { once: true })

    modify_cancel.addEventListener('click',({target}) => {                           
        target.parentNode.innerHTML = original;        
        document.querySelector("#myinfomodify_name").addEventListener('click', ({target}) => {
            modify_name_recusion(target)
        }, { once: true })             
    }, { once: true })        
}

function modify_name() {
    modifyName.addEventListener('click',({target}) => {        
        modify_name_recusion(target)
    }, { once: true })
}


function modify_password_recusion(target) {            
    const original = target.parentNode.innerHTML;
    target.parentNode.firstElementChild.innerHTML = '<input type="password" id="password_input"/>';        
    target.parentNode.lastElementChild.value = "확인";
    target.parentNode.lastElementChild.id = "myinfomodify_confirm";
    const modify_confirm = target.parentNode.lastElementChild;
    const modify_cancel = target.parentNode.lastElementChild.cloneNode();
    modify_cancel.value = '취소';
    modify_cancel.id = 'myinfomodify_cancel';        
    target.parentNode.appendChild(modify_cancel);

    modify_confirm.addEventListener('click', ({target}) => {        
        fetch(window.location.href, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                "column": "pwd",
                "value": document.querySelector('#password_input').value
            }),
            });

        target.parentNode.innerHTML = original;
        
        document.querySelector("#myinfomodify_password").addEventListener('click', ({target}) => {
            modify_password_recusion(target)

        window.location.reload()
        }, { once: true })  
    }, { once: true })    

    modify_cancel.addEventListener('click',({target}) => {                           
        target.parentNode.innerHTML = original;        
        document.querySelector("#myinfomodify_password").addEventListener('click', ({target}) => {
            modify_password_recusion(target)
        }, { once: true })             
    }, { once: true })        
}

function modify_password() {
    modifyPassword.addEventListener('click',({target}) => {        
       modify_password_recusion(target)
    }, { once: true })   
}

function init() {
    modify_name()
    modify_password()
}

init()