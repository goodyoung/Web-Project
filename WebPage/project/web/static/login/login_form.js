function tr() {
    let hy = document.querySelector('#te')
    let text = hy.firstChild.innerText
    re = document.querySelectorAll('#validate')
    console.log(re)
    re.forEach((i) => {
        console.log(text)
        if (text === i.getAttribute('name')){
                i.innerHTML = `<span style="color:#4DAB3C;">${text}</span>은 필수입력 항목입니다.`
        }
    })
hy.remove()
}