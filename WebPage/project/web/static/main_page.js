var todo_list;

async function store_todo(is_complete, content, nth){
    let result = await fetch(".", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            "method": "store",
            "is_complete": is_complete,
            "content": content,
            "nth": nth
        }),
        }).then((response) => response.json());
    
    return result
}

async function get_todo(date){
    let result = await fetch(".", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            "method": "get",
            "date" : date
        }),
        }).then((response) => response.json());
    
    return result
}

function make_todos(date = new Date()){

    let ul = document.createElement("ul")
    ul.classList.add("todo-list")

    for(let i = 0; i < 5; i++){
        let li = document.createElement("li")
        li.dataset.nth = i;

        let p = document.createElement("p")
        p.classList.add("todo_show")

        let button1 = document.createElement("button")
        button1.classList.add("modify_button")
        button1.appendChild(document.createTextNode("입력"))
        button1.addEventListener('click', ({target}) => {
            label_to_input(target)
        }, {once: true})

        let button2 = document.createElement("button")
        button2.classList.add("complete_button", "deactivate")
    
        let img = document.createElement("img")
        img.setAttribute("src", "../static/ui/check.png")
        
        button2.appendChild(img)

        li.appendChild(button2)
        li.appendChild(p)
        li.appendChild(button1)


        ul.appendChild(li)
    }


    let li = document.createElement("li")

    let p = document.createElement("p")
    p.classList.add("todo_show")

    let button1 = document.createElement("button")
    button1.classList.add("modify_button")
    button1.appendChild(document.createTextNode("입력"))
    button1.addEventListener('click', ({target}) => {
        label_to_input(target)
    }, {once: true})

    let button2 = document.createElement("button")
    button2.classList.add("complete_button", "deactivate")
   
    let img = document.createElement("img")
    img.setAttribute("src", "../static/ui/check.png")
    
    button2.appendChild(img)

    li.appendChild(button2)
    li.appendChild(p)
    li.appendChild(button1)

    return li
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

function input_to_label(target){
    text_input = target.parentNode.querySelector("input")

    if(text_input.value != ""){
        prev = text_input.nextSibling
    
        let label = document.createElement("p")
        label.classList.add("todo_show")
        label.innerText = text_input.value
        target.addEventListener('click', ({target}) => {label_to_input(target)}, {once: true})
    
        target.innerText = "수정"
        store_todo(0, text_input.value, target.parentNode.dataset.nth)
    
        complete_button = target.parentNode.querySelector(".complete_button")
        if(complete_button.classList.contains("deactivate")){
            complete_button.classList.toggle("deactivate")
        }
    
        prev.parentNode.insertBefore(label, prev)
        text_input.remove()
    }
    else{
        prev = text_input.nextSibling
    
        let label = document.createElement("p")
        label.classList.add("todo_show")
        label.innerText = text_input.value
        target.addEventListener('click', ({target}) => {label_to_input(target)}, {once: true})
    
        target.innerText = "입력"

        prev.parentNode.insertBefore(label, prev)
        text_input.remove()
    }
}

window.onload = function assign_event(){
    todo_list = document.getElementsByClassName("todo-list")[0]

    for(let i = 0; i < 5; i++){
        let li = make_todo();
        li.dataset.nth = i;
        todo_list.appendChild(li)
    }

    check_lvup()
}