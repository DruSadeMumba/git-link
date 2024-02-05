const openNav = () => {
  $("#navigation").css("width", "250px");
};

const closeNav = () => {
  $("#navigation").css("width", "0");
};

$("#search").click(() => {
  $("#search-form").submit();
});
