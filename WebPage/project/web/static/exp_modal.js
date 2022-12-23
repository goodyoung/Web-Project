for (let close_button of document.querySelectorAll('.exp-modal_close')){
    close_button.addEventListener('click', () => {
        console.log(close_button.parentNode.parentNode)
        close_button.parentNode.parentNode.classList.toggle("show");
    });
}

function get_exp(obtained_exp){
    document.querySelector(".obtained_exp").innerText = obtained_exp
    document.querySelector(".get-exp").classList.toggle("show")
}

function level_up(current_lv){
    document.querySelector(".current_lv").innerText = current_lv
    document.querySelector(".level-up").classList.toggle("show")
}