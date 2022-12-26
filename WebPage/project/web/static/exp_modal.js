for (let close_button of document.querySelectorAll('.level-modal_close')){
    close_button.addEventListener('click', () => {
        console.log(close_button.parentNode.parentNode)
        close_button.parentNode.parentNode.classList.toggle("show");
    });
}

function get_exp(obtained_exp){
    document.querySelector(".obtained_exp").innerText = obtained_exp
    document.querySelector(".exp-modal").classList.add("show")

    setTimeout(() => {document.querySelector(".exp-modal").classList.remove("show")}, 2000);
}

function level_up(current_lv){
    document.querySelector(".current_lv").innerText = current_lv
    document.querySelector(".level-modal").classList.toggle("show")
}

async function check_lvup(){
    let is_getexp = await fetch("/chk_lvup").then((response) => response.json())
    if(is_getexp["lv"]>0){
        level_up(is_getexp["lv"]);
        return true
    }
    else return false;
}