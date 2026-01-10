
window.onscroll = function() {myFunction()};

var header = document.getElementById("opt-header");
var sticky = header.offsetTop;

function myFunction() {
if (window.pageYOffset > sticky) {
    header.classList.add("opt-sticky");
} else {
    header.classList.remove("opt-sticky");
}
}

$(".slug-title").keyup(function() {
    var Text = $(this).val();
    $(".meta-title").val(Text);
    Text = Text.toLowerCase();
    Text = Text.replace(/[^a-zA-Z0-9]+/g,'-');
    $(".slug-url").val(Text);        
  });