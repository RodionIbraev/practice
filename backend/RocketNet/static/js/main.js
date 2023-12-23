//Модальное окно

function togglePopupReg() {
    document.getElementById("popup-1").classList.toggle("active");
}

function togglePopupLog() {
    document.getElementById("popup-2").classList.toggle("active");
};


//Кнопки тарифов
var btn_phone = document.getElementById("btn-phone");
var btn_home = document.getElementById("btn-home");
var btn_combo = document.getElementById("btn-combo");
var phone = document.getElementById("phone");
var home = document.getElementById("home");
var combo = document.getElementById("combo");

btn_phone.addEventListener('click', ()=>{
    phone.style.display='block';
    home.style.display='none';
    combo.style.display='none';
});

btn_home.addEventListener('click', ()=>{
    home.style.display='block';
    phone.style.display='none';
    combo.style.display='none';
})
btn_combo.addEventListener('click', ()=>{
    combo.style.display='block';
    phone.style.display='none';
    home.style.display='none';
});

window.addEventListener('load', function() {
    var button = document.getElementsByClassName('icon-box');
    if (button.length > 0) {
      button[0].focus();
    }
});


// Ошибки регистрации пользователей
const form = document.getElementById('registration-form');

// Пароль

const passwordInput = document.getElementById('password');
const passwordErrorMessage = passwordInput.nextElementSibling;

form.addEventListener('submit', function(event) {
  var passwordErrorMessages = '';

  if (passwordInput.value.length < 8) {
    passwordErrorMessages += 'Пароль не может быть меньше 8 символов. ';
  }

  if (/^\d+$/.test(passwordInput.value)) {
    passwordErrorMessages += 'Пароль не может состоять только из цифр. ';
  }

  if (passwordErrorMessages !== '') {
    passwordErrorMessage.textContent = passwordErrorMessages.trim();
    event.preventDefault();
  } else {
    passwordErrorMessage.textContent = '';
  }
});

// Номер телефона

const phoneNumberInput = document.getElementById('phone_number');
const phoneNumberErrorMessage = phoneNumberInput.nextElementSibling;

form.addEventListener('submit', function(event) {
  var phoneNumberErrorMessages = '';

  if (!/^([+]7|8)\d{10}$/.test(phoneNumberInput.value)) {
    phoneNumberErrorMessages += 'Некорректный номер телефона.';
  }

  if (phoneNumberErrorMessages !== '') {
    phoneNumberErrorMessage.textContent = phoneNumberErrorMessages.trim();
    event.preventDefault();
  } else {
    phoneNumberErrorMessage.textContent = '';
  }
});