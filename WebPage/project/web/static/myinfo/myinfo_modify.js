const modifyName = document.getElementById('myinfomodify_name');
const modifyNickname = document.getElementById('myinfomodify_nickname');
const modifyPassword = document.getElementById('myinfomodify_password');

function modify_name_recusion(target) {            
    const original = target.parentNode.innerHTML;
    target.parentNode.firstElementChild.innerHTML = '<input type="text"/>';        
    target.parentNode.lastElementChild.value = "확인";
    target.parentNode.lastElementChild.id = "myinfomodify_confirm";
    const modify_confirm = target.parentNode.lastElementChild;
    const modify_cancel = target.parentNode.lastElementChild.cloneNode();
    modify_cancel.value = '취소';
    modify_cancel.id = 'myinfomodify_cancel';        
    target.parentNode.appendChild(modify_cancel);    

    modify_confirm.addEventListener('click',({target}) => {                           
        target.parentNode.innerHTML = original;
        // myinfomodify_confirm 버튼 누르면, input에 작성한 이름 이 데이터베이스로 전달되어 나타나도록
        document.querySelector("#myinfomodify_name").addEventListener('click', ({target}) => {
            modify_name_recusion(target)
        })  
    })

    modify_cancel.addEventListener('click',({target}) => {                           
        target.parentNode.innerHTML = original;        
        document.querySelector("#myinfomodify_name").addEventListener('click', ({target}) => {
            modify_name_recusion(target)
        })             
    })        
}

function modify_name() {
    modifyName.addEventListener('click',({target}) => {        
        modify_name_recusion(target)
    })
}

function modify_nickname_recusion(target) {            
    const original = target.parentNode.innerHTML;
    target.parentNode.firstElementChild.innerHTML = '<input type="text"/>';        
    target.parentNode.lastElementChild.value = "확인";
    target.parentNode.lastElementChild.id = "myinfomodify_confirm";
    const modify_confirm = target.parentNode.lastElementChild;
    const modify_cancel = target.parentNode.lastElementChild.cloneNode();
    modify_cancel.value = '취소';
    modify_cancel.id = 'myinfomodify_cancel';        
    target.parentNode.appendChild(modify_cancel);

    modify_confirm.addEventListener('click',({target}) => {                           
        target.parentNode.innerHTML = original;
        // myinfomodify_confirm 버튼 누르면, input에 작성한 별명 이 데이터베이스로 전달되어 나타나도록
        document.querySelector("#myinfomodify_nickname").addEventListener('click', ({target}) => {
            modify_nickname_recusion(target)
        })  
    })    

    modify_cancel.addEventListener('click',({target}) => {                           
        target.parentNode.innerHTML = original;        
        document.querySelector("#myinfomodify_nickname").addEventListener('click', ({target}) => {
            modify_nickname_recusion(target)
        })             
    })        
}

function modify_nickname() {         
    modifyNickname.addEventListener('click',({target}) => {
        modify_nickname_recusion(target)
    })    
}

function modify_password_recusion(target) {            
    const original = target.parentNode.innerHTML;
    target.parentNode.firstElementChild.innerHTML = '<input type="password"/>';        
    target.parentNode.lastElementChild.value = "확인";
    target.parentNode.lastElementChild.id = "myinfomodify_confirm";
    const modify_confirm = target.parentNode.lastElementChild;
    const modify_cancel = target.parentNode.lastElementChild.cloneNode();
    modify_cancel.value = '취소';
    modify_cancel.id = 'myinfomodify_cancel';        
    target.parentNode.appendChild(modify_cancel);

    modify_confirm.addEventListener('click',({target}) => {                           
        target.parentNode.innerHTML = original;
        // myinfomodify_confirm 버튼 누르면, input에 작성한 별명 이 데이터베이스로 전달되어 나타나도록
        document.querySelector("#myinfomodify_password").addEventListener('click', ({target}) => {
            modify_password_recusion(target)
        })  
    })    

    modify_cancel.addEventListener('click',({target}) => {                           
        target.parentNode.innerHTML = original;        
        document.querySelector("#myinfomodify_password").addEventListener('click', ({target}) => {
            modify_password_recusion(target)
        })             
    })        
}

function modify_password() {
    modifyPassword.addEventListener('click',({target}) => {        
       modify_password_recusion(target)
    })   
}

function init() {
    modify_name()
    modify_nickname()
    modify_password()
}

init()