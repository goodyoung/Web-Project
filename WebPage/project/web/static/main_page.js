var todo_list;

async function store_todo(is_complete, content, nth){
    console.log(content)
    let result = await fetch(".", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            "func": "store",
            "is_complete": is_complete,
            "content": content,
            "nth": nth
        }),
        }).then((response) => response.json());

    if(result["exp"]!=0){
        get_exp(result["exp"])
    }
    
    return result
}

async function get_todo(date){
    let result = await fetch(window.location.href, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            "func": "get",
            "date" : date
        }),
        }).then((response) => response.json());
        

    return result
}

async function make_todos(date = new Date()){

    let year = date.getFullYear()
    let month = date.getMonth()+1
    let days = date.getDate()

    let formated_date = `${year}-${month >= 10 ? month : '0' + month}-${date >= 10 ? days : '0' + days}`

    let todos = await get_todo(formated_date)
    console.log(todos)

    let ul = document.createElement("ul")
    ul.classList.add("todo-list")

    for(let i = 0; i < 5; i++){
        let li = document.createElement("li")
        li.dataset.nth = i;

        let p = document.createElement("p")
        p.classList.add("todo_show")

        let button1 = document.createElement("button")
        button1.classList.add("modify_button")

        let button2 = document.createElement("button")
        button2.classList.add("complete_button")
        button2.addEventListener('click', async function(){
            let response = await store_todo(1, button2.parentNode.querySelector("p").innerText, i)
            
            p.classList.add("complete")

            button1.classList.add("deactivate")
            button2.classList.add("complete")
            button2.disabled = true;
        })

        if(todos[i]["is_complete"]==-1){
            button1.appendChild(document.createTextNode("입력"))
            button1.addEventListener('click', ({target}) => {
                label_to_input(target)
            }, {once: true})

            button2.classList.add("deactivate")
        }

        else if(todos[i]["is_complete"]==0){
            p.appendChild(document.createTextNode(todos[i]["content"]))

            button1.appendChild(document.createTextNode("수정"))
            button1.addEventListener('click', ({target}) => {
                label_to_input(target)
            }, {once: true})
        }
        else{
            p.appendChild(document.createTextNode(todos[i]["content"]))
            p.classList.add("complete")

            button1.classList.add("deactivate")
            button2.classList.add("complete")
            button2.disabled = true;
        }

        li.appendChild(button2)
        li.appendChild(p)
        li.appendChild(button1)

        ul.appendChild(li)
    }

    document.querySelector(".todo").appendChild(ul)
}

function label_to_input(target){
    label = target.parentNode.querySelector("p")

    prev = label.nextSibling

    let text_input = document.createElement("input")
    text_input.setAttribute("type", "text")
    text_input.classList.add("todo_input")
    text_input.value = label.innerText

    target.addEventListener('click', ({target})=>{
        input_to_label(target)
    }, {once:true})

    target.innerText = "저장"

    complete_button = target.parentNode.querySelector(".complete_button")
    if(!complete_button.classList.contains("deactivate")){
        complete_button.classList.toggle("deactivate")
    }

    prev.parentNode.insertBefore(text_input, prev)
    label.remove()
}

async function input_to_label(target){
    text_input = target.parentNode.querySelector("input")
    console.log(text_input.value)


    if(text_input.value.length > 30){
        todo_error()
        target.addEventListener('click', ({target})=>{
            input_to_label(target)
        }, {once:true})
    }
    else if(text_input.value != ""){
        prev = text_input.nextSibling
    
        let label = document.createElement("p")
        label.classList.add("todo_show")
        label.innerText = text_input.value
        target.addEventListener('click', ({target}) => {label_to_input(target)}, {once: true})
    
        target.innerText = "수정"
        let response = await store_todo(0, text_input.value, target.parentNode.dataset.nth)
        if(response["exp"]!=0){
            get_exp(response["exp"])
        }

        complete_button = target.parentNode.querySelector(".complete_button")
        if(complete_button.classList.contains("deactivate")){
            complete_button.classList.toggle("deactivate")
        }
    
        prev.parentNode.insertBefore(label, prev)
        text_input.remove()
    }
    else{
        target.addEventListener('click', ({target})=>{
            input_to_label(target)
        }, {once:true})
    }
}

function todo_error(){
    document.querySelector(".error-modal").classList.add("show")
}

window.onload = function assign_event(){
    todo = document.getElementsByClassName("todo")[0]

    make_todos()

    check_lvup()

    document.querySelector(".error-modal-modal_close").addEventListener('click', () => {
        document.querySelector(".error-modal").classList.remove("show")
    })
}