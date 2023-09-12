const languages = {
    "Русский": "./img/ru.svg",
    "English": "./img/en.svg",
}

const langBtn = document.getElementsByClassName("dropdown-lang")[0];
const langDrop = document.getElementsByClassName("dropdown-content")[0];
const langs = Array.from(document.getElementsByClassName("lang-li"));

langBtn.addEventListener('click', () => {
    langDrop.classList.toggle('block');
})

langs.forEach(elem => {
    elem.addEventListener('click', () => {
        const langImg = document.getElementById('lang-prew');
        langImg.src = languages[elem.innerText];
    })
});