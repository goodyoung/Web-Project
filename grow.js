var todo_list;
var add_todo_input;
var todo_underbar;
var filter_buttons;
var current_filter = "All";

function change_list(){
    todo_underbar.getElementsByTagName("p")[0].innerText = todo_list.children.length + " items left"
}

function add_todo(todo_text){
    let new_todo = document.createElement("li")
    new_todo.setAttribute("class", "showed-item")
    
    let checkbox = document.createElement("input")
    checkbox.setAttribute("type", "checkbox")
    checkbox.setAttribute("class", "check-complete")

    new_todo.appendChild(checkbox)

    let label = document.createElement("label")
    let text = document.createTextNode(todo_text)
    label.appendChild(text)
    new_todo.appendChild(label)

    let button = document.createElement("input")
    button.setAttribute("type", "button")
    button.setAttribute("class", "del-todo")
    new_todo.appendChild(button)

    button.addEventListener('click', () => {del_todo(new_todo)})
    label.addEventListener('dblclick', () => {label_to_input(label)})

    if(todo_list.length==0) todo_list.appendChild(new_todo);
    else todo_list.insertBefore(new_todo, todo_list.firstChild)
    change_list()
    filter(current_filter)
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

function del_todo(elem){
    elem.remove()
    change_list()
}

function filter(target){
    let index;
    let filter_target;
    switch(target){
        case "All":
            index = 0;
            break;
        case "Active":
            index = 1;
            filter_target = false;
            break;
        case "Completed":
            index = 2;
            filter_target = true;
            break;
    }

    for (var list of todo_list.children){
        is_checked = list.getElementsByClassName("check-complete")[0].checked

        if(filter_target == is_checked || target == "All"){
            list.setAttribute("class", "showed-item");
        }
        else{
            list.setAttribute("class", "hided-item");
        }
    }
    
    for (let i = 0; i < filter_buttons.children.length; i++){
        if(index==i) filter_buttons.children[i].setAttribute("class", "todo-filter-selected");
        else filter_buttons.children[i].setAttribute("class", "todo-filter");
    }
}

function clear_completed(){
    i = 0;
    while(i < todo_list.children.length){
        is_checked = todo_list.children[i].getElementsByClassName("check-complete")[0].checked;

        if(is_checked){
            todo_list.children[i].remove();
        }
        else{
            i+=1;
        }
    }
    change_list()
}

window.onload = function assign_event(){
    todo_list = document.getElementsByClassName("todo-list")[0]
    add_todo_input = document.getElementsByClassName("todo-input")[0]
    todo_underbar = document.getElementsByClassName("todo-underbar")[0]
    filter_buttons = document.getElementsByClassName("filter-buttons")[0]

    add_todo_input.addEventListener('keypress', (e)=>{
        if(e.key=="Enter"){
            add_todo(add_todo_input.value)
            add_todo_input.value = ""
        }
    })

    for (var button of filter_buttons.children){
        let target = button.children[0].value
        console.log(target)

        button.addEventListener('click', () => {
            current_filter = target;
            filter(current_filter)
        })
    }

    let clear_complete = document.getElementsByClassName("clear-complete")[0]
    clear_complete.addEventListener('click', () => {
        clear_completed()
    })

    console.log("함수 로드 성공!")
}