

/* Template Name: Pricepeg - ootstrap 5 Pricing Table Template 
   Author: Themesdesign
   Version: 1.0
   Auther : https://codecanyon.net/user/themesdesign
   File Description: Main JS file of the template
*/


// js for Pricing-8

function check() {
  var checkBox = document.getElementById("checbox");
  var text1 = document.getElementsByClassName("text1");
  var text2 = document.getElementsByClassName("text2");

  for (var i = 0; i < text1.length; i++) {
      if (checkBox.checked == true) {
          text1[i].style.display = "block";
          text2[i].style.display = "none";
      } else if (checkBox.checked == false) {
          text1[i].style.display = "none";
          text2[i].style.display = "block";
      }
  }
}
check();


// js for Pricing-2 & 9

var buttonGroups = document.querySelectorAll('.nav-item button');
for (var i = 0; i < buttonGroups.length; i++) {
  buttonGroups[i].addEventListener('click', onButtonGroupClick);
}
function onButtonGroupClick(event) {
  if (event.target.id === 'pills-home-tab') {
    document.getElementById("pills-home").classList.add("show", "active");
    document.getElementById("pills-profile").classList.remove("show", "active");
  } else {
    document.getElementById("pills-profile").classList.add("show", "active");
    document.getElementById("pills-home").classList.remove("show", "active");
  }
}