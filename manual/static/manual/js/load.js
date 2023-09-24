// Отображает анимацию загрузки // 
function displayLoadingAnimation(button){
    button.style.display = "none";
    let loadingIcon = document.getElementById("loading-icon");
    loadingIcon.style.display = "inline-block"; // покажем объект загрузки
}

// Копирование почты // 
document.querySelector('.faq-link').addEventListener('click', function(e) {
    e.preventDefault();

    // Копировать почту в буфер обмена
    let dummy = document.createElement('input'),
        emailLink = e.target.closest('.faq-link'),
        email = emailLink.getAttribute('href').split(":")[1];
    document.body.appendChild(dummy);
    dummy.value = email;
    dummy.select();
    document.execCommand('copy');
    document.body.removeChild(dummy);

    // Показать всплывающее окно
    let toast = document.getElementById('copyToast');
    toast.classList.add('show');
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
});