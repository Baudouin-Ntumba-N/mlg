

document.addEventListener("DOMContentLoaded", function(){

let eyeLink = document.querySelector(".eye");
let image = document.querySelector(".eye-image");
let password = document.querySelector(".password-div input");

let open = true;
eyeLink.onclick = function(){
    if(open){
    image.src = "/media/icons/visibility_off.png";
    password.type = "text";
    open = false;
    }else{
    image.src = "/media/icons/visibility.png";
    password.type = "password";
    open = true;
    }
}

});