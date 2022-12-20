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
    let correct;
    if(problem_type.innerText == "객관식"){
        try{
            db = "objective"
            answer = document.querySelector(".problem_answer:checked").value

        }
        catch (TypeError){
            console.log("정답을 선택해주세요.")
            return;
        }
    }
    else{
        db = "subjective"
        answer = document.querySelector(".problem_answer").value
        if(answer=="") {console.log("정답을 입력해주세요."); return;}
    }

    correct = await send_SQL(`SELECT CASE WHEN answer = '${answer}' THEN TRUE ELSE FALSE END AS success FROM ${db} WHERE id = ${problem_id}`)
    if(correct[0]["success"]){
        console.log("정답입니다!")
    }
    else{
        console.log("오답입니다.")
    } 
    return
}

async function call_id(){
    let userid = await fetch("/get_ID")
    return userid
}

window.onload = function () {

    answer_commit = document.querySelector(".answer_commit")
    answer_commit.addEventListener('click', () => {
        check_answer()
    })

    console.log(sessionStorage.getItem("id"))
}