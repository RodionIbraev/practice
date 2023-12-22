function togglePopupReg() {
    document.getElementById("popup-1").classList.toggle("active");
}

function togglePopupLog() {
    document.getElementById("popup-2").classList.toggle("active");
};

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
})