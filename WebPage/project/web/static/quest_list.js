

async function send_SQL(query){

    let result = await fetch("/runSQL", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            "query": query
        }),
        }).then((response) => response.json());
    
    return result
}

async function make_category(){
    let categories = await send_SQL("SELECT category, COUNT(category) AS n FROM problem GROUP BY category ORDER BY category")

    console.log(categories)
    let category_list = document.querySelector(".category_list")

    let li = document.createElement("li")

    let button = document.createElement("button")
    button.classList.add("category_list_button")

    let label1 = document.createElement("label")
    label1.appendChild(document.createTextNode("ALL"))
    let label2 = document.createElement("label")
    label2.appendChild(document.createTextNode(""))

    button.appendChild(label1)
    button.appendChild(label2)
    button.addEventListener('click', ()=>{
        category_value = document.querySelector(".category_value")
        category_value.innerText = "ALL"

        category_list = document.querySelector(".category_list")
        category_list.classList.toggle("visible")
        
        make_problem("ALL")
    })


    li.appendChild(button)
    category_list.appendChild(li)

    for (let category of categories){
        let li = document.createElement("li")

        let button = document.createElement("button")
        button.classList.add("category_list_button")

        let label1 = document.createElement("label")
        label1.appendChild(document.createTextNode(category.category))
        let label2 = document.createElement("label")
        label2.appendChild(document.createTextNode(category.n))

        button.appendChild(label1)
        button.appendChild(label2)

        button.addEventListener('click', ()=>{
            category_value = document.querySelector(".category_value")
            category_value.innerText = category.category

            category_list = document.querySelector(".category_list")
            category_list.classList.toggle("visible")

            make_problem(category.category)
        })

        li.appendChild(button)

        category_list.appendChild(li)
    }
}

async function make_problem(category="ALL"){
    let problems;
    if(category=="ALL") problems = await send_SQL("SELECT id FROM problem");
    else problems = await send_SQL(`SELECT id FROM problem WHERE category = '${category}'`);

    console.log(problems)
    let problem_list = document.querySelector(".problem_list")
    problem_list.innerHTML = ""

    for (let problem of problems){
        let li = document.createElement("li")

        let div = document.createElement("div")
        div.classList.add("problem_icon", "unsolved")

        let a = document.createElement("a")
        a.setAttribute("href", "/quest/"+problem.id)
        a.classList.add("problem_link")
        a.appendChild(document.createTextNode(problem.id))

        li.appendChild(div)
        li.appendChild(a)

        problem_list.appendChild(li)
    }
}

async function initUI(){
    await make_problem()
    await make_category()   
}


window.onload = function(){
    let category_button = document.querySelector(".category_button")

    category_button.addEventListener('click', () => {
        category_list = category_button.parentNode.querySelector('.category_list').classList.toggle("visible")
    })

    initUI()
}