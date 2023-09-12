function selectType() {
    nextBtn.disabled = false;
}

const nextBtn = document.getElementById("type-next");
nextBtn.disabled = true;

const radioBtns = document.getElementsByClassName("type-radio");
for(let i = 0; i < radioBtns.length; i++) {
    radioBtns[i].checked = false;
}