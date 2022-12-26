var todo_list;

function make_todo(){
    let li = document.createElement("li")

    let p = document.createElement("p")
    p.classList.add("todo_show")

    let button1 = document.createElement("button")
    button1.classList.add("modify_button")
    button1.appendChild(document.createTextNode("수정"))

    let button2 = document.createElement("button")
    button2.classList.add("complete_button")
    button2.appendChild(document.createTextNode("완료"))


    li.appendChild(p)
    li.appendChild(button1)
    li.appendChild(button2)

    return li
}

function label_to_input(label){
    prev = label.nextSibling

    let text_input = document.createElement("input")
    text_input.setAttribute("type", "text")
    text_input.value = label.innerText
    text_input.addEventListener('keypress', (e)=>{
        if(e.key=="Enter"){
            input_to_label(text_input)
        }
    })

    prev.parentNode.insertBefore(text_input, prev)
    label.remove()
}

function input_to_label(text_input){
    prev = text_input.nextSibling

    let label = document.createElement("label")
    label.innerText = text_input.value
    label.addEventListener('dblclick', () => {label_to_input(label)})

    prev.parentNode.insertBefore(label, prev)
    text_input.remove()
}

window.onload = function assign_event(){
    todo_list = document.getElementsByClassName("todo-list")[0]

    for(let i = 0; i < 5; i++){
        todo_list.appendChild(make_todo())
    }
}