



 document.addEventListener('DOMContentLoaded', function () {
            document.querySelector('#menu').style.display = 'none';
   let a = 0;

            document.querySelector('#menu-button').onclick = function () {


                document.querySelector('#menu').style.display = 'block';



         document.querySelector('#menu-button').style.display = 'block';

              a = 1;

            }

       document.querySelector('#menu-button').onclick = function() {

         if (a==1){

          document.querySelector('#menu').style.display = 'none';

             a = 0
         }
         else{

           document.querySelector('#menu').style.display = 'block';
        a = 1
         }

       }

        })