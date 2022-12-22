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

async function check_answer(){
    let problem_type = document.querySelector(".problem_type")
    let problem_id = document.querySelector(".problem_id").innerText
    let db;
    let answer;
    if(problem_type.innerText == "객관식"){
        try{
            db = "objective"
            answer = document.querySelector(".answer_choice > input[type=\"radio\"]:checked").value

        }
        catch (TypeError){
            console.log("정답을 선택해주세요.")
            document.querySelector('.error_modal').classList.toggle("show");
            return;
        }
    }
    else{
        db = "subjective"
        answer = document.querySelector(".problem_answer").value
        if(answer=="") {
            console.log("정답을 입력해주세요.");
            document.querySelector('.error_modal').classList.toggle("show");
            return;}
    }

    let correct = await fetch(window.location.href, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            "problem_id": problem_id,
            "type": db,
            "answer": answer
        }),
        }).then((response) => response.json());

    if(correct[0]["success"]){
        console.log("정답입니다!")
        document.querySelector('.correct_modal').classList.toggle("show");
    }
    else{
        console.log("오답입니다.")
        document.querySelector('.incorrect_modal').classList.toggle("show");
    } 
    return
}

function set_content_height(){
    let problem_content = document.querySelector(".problem_content")
    let problem_height = document.querySelector("body").clientHeight

    problem_height -= document.querySelector("header").clientHeight
    problem_height -= document.querySelector("footer").clientHeight
    problem_height -= document.querySelector("nav").clientHeight

    console.log(`${problem_height-40}px`)
    problem_content.style.height=`${problem_height-40}px`
}

window.onload = function () {

    let answer_button = document.querySelector("footer > button")

    if (answer_button.classList.contains("answer_commit")){
        answer_button.addEventListener('click', () => {
            check_answer()
        })
    }
    else if (answer_button.classList.contains("answer_show")){
        answer_button.addEventListener('click', () => {
            if(answer_button.classList.contains("answer_shown")){
                answer_button.innerText = "해설보기"
            }
            else{
                answer_button.innerText = "입력보기"
            }
            answer_button.classList.toggle("answer_shown")
            document.querySelector(".problem_answer").classList.toggle("deactivate")
            document.querySelector(".answer_explanation").classList.toggle("deactivate")

            set_content_height()
        })
    }

    for (let close_button of document.querySelectorAll('.modal_close')){
        close_button.addEventListener('click', () => {
            console.log(close_button.parentNode.parentNode)
            close_button.parentNode.parentNode.classList.toggle("show");
            window.location.reload() 
        });
    }

    set_content_height()
}