// document.addEventListener('DOMContentLoaded', function () {

//     if (window.innerWidth >= 900) {

//         document.querySelector('.menu').style.display = 'block';

//     } else {

//         document.querySelector('.menu').style.display = 'none';
//     }


//     let displayed = false;

//     document.querySelector('#menu-button').onclick = function() {

//         if (displayed) {

//             document.querySelector('.menu').style.display = 'none';
//             document.querySelector(".menuImage").style.display = "block";
//             document.querySelector(".closeImage").style.display = "none";
//             displayed = false;
//         } else {

//             document.querySelector('.menu').style.display = 'block';
//             document.querySelector(".menuImage").style.display = "none";
//             document.querySelector(".closeImage").style.display = "block";


//             displayed = true;
//         }

//     }

// })





document.addEventListener("DOMContentLoaded", function () {
  if (window.innerWidth >= 700) {
    document.querySelector(".menu").style.display = "block";
  } else {
    document.querySelector(".menu").style.display = "none";
  }


/* */


  let displayed = false;

  document.querySelector("#menu-button").onclick = function () {
    if (displayed) {
      document.querySelector("#menu-button").innerHTML = "Menu";
      document.querySelector(".menu").style.display = "none";

      displayed = false;
    } else {
      document.querySelector(".menu").style.display = "block";
      document.querySelector("#menu-button").innerHTML = "Close ↑";
      displayed = true;
    }
  };



  window.onresize = function () {
    setTimeout(function () {
      if (window.innerWidth >= 700) {
        document.querySelector(".menu").style.display = "block";
        document.querySelector("#menu-button").style.display = "none";
      } else {
        document.querySelector(".menu").style.display = "none";
        document.querySelector("#menu-button").style.display = "block";
      }
      //document.querySelector(".menu").style.display = "none";
    }, 0);
  };



// upload image pre-view file input for settings
// for profile et cover photos
   const profileInput = document.querySelector("#id_photo");
   const coverImageInput = document.querySelector("#id_cover_image");

   const photo = document.querySelector("#user-photo");
   const cover_image = document.querySelector("#user-cover-image");

    profileInput.onchange = function(){
       const [file]= profileInput.files;
       if (file) {
           photo.src = URL.createObjectURL(file);
       }
   }
   coverImageInput.onchange = function(){
       const [file] = coverImageInput.files;
       if(file){
           cover_image.src = URL.createObjectURL(file);
       }
   }



});