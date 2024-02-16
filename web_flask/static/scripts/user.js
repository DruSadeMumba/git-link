//git user client side operations
const openNav = () => {
  document.getElementById("navigation").style.width = "250px";
};

const closeNav = () => {
  document.getElementById("navigation").style.width = "0";
};

document.getElementById("search").addEventListener("click", () => {
  document.getElementById("search-form").submit();
});

document.getElementById("search-input").addEventListener("keypress", (e) => {
  if (e.key === 'Enter') {
    document.getElementById("search-form").submit();
  }
});

save_repo = (uid, name, description, html_url) => {
  $.ajax({
    type: 'POST',
    url: '/save_repo/${uid}',
    data: {
      uid: uid,
      name: name,
      description: description,
      html_url: html_url
    },
    success: (response) => {
      console.log(response)
      alert('Repository saved successfully!');
      },
    error: (xhr, status, error) => {
      console.error(error);
      alert('Failed to save repository.');
    }
  });
}

