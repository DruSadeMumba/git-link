function openNav() {
  document.getElementById("navigation").style.width = "250px"
}

function closeNav() {
  document.getElementById("navigation").style.width = "0";
}



document.getElementById('search').addEventListener('click', function() {
  document.getElementById('search-form').submit();
});