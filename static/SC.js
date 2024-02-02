document.getElementById("second").onblur =
chkPasswords;

document.getElementById("myForm").onsubmit =
chkPasswords;
    function chkPasswords() {

var init = document.getElementById("initial");

var sec = document.getElementById("second");

if (init.value == "") {

alert("You did not enter a password \n" +

"Please enter one now");

return false;

}

if (init.value != sec.value) {

alert("The two passwords you entered are not the same \n" +

"Please re-enter both now");

return false;

} else

return true;

}