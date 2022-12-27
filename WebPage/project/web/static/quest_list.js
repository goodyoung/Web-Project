async function filter_problem(target_category="ALL", target_status="ALL"){
    console.log(target_category, target_status)
    let problem_list = document.querySelector(".problem_list")

    for(let problem of problem_list.children){
        let category = problem.querySelector(".problem_category").innerText
        let status = problem.dataset["status"]
        console.log(status, target_status)

        let valid = true
        if(target_category!="ALL"){
            valid = valid && category==target_category
        }
        if(target_status!="ALL"){
            valid = valid && status==target_status
        }

        if(valid && problem.classList.contains("deactivate") || !valid && !problem.classList.contains("deactivate")){
            problem.classList.toggle("deactivate")
        }
        else{

        }
    }
}

window.onload = function(){
    let dropdown_button = document.querySelectorAll(".dropdown_button")

    for (let droopdown of dropdown_button){
        droopdown.addEventListener('click', () => {
            category_list = droopdown.parentNode.querySelector('.dropdown_list').classList.toggle("visible")
        })

    }

    let status_list_button = document.querySelectorAll(".status_list_button")

    for(let button of status_list_button){
        button.addEventListener('click', ()=>{
            let target_category = document.querySelector(".category_value").innerText
            let target_status = button.dataset["status"]

            let status_value = document.querySelector(".status_value")
            status_value.classList.remove(...status_value.classList)
            status_value.classList.add("status_value", "status_icon")
            status_value.classList.add(target_status)
            status_value.dataset["status"] = target_status

            let status_list = document.querySelector(".status_list")
            status_list.classList.toggle("visible")

            filter_problem(target_category, target_status)
        })
    }

    let category_list_button = document.querySelectorAll(".category_list_button")

    for(let button of category_list_button){
        button.addEventListener('click', ()=>{
            let target_category = button.querySelector("label").innerText
            let target_status = document.querySelector(".status_value").dataset["status"]

            let category_value = document.querySelector(".category_value")
            category_value.innerText = target_category

            let category_list = document.querySelector(".category_list")
            category_list.classList.toggle("visible")

            filter_problem(target_category, target_status)
        })
    }
}