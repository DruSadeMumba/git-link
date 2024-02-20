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

const addRepo = (button) => {
  if (auth.currentUser) {
    const userId = auth.currentUser.uid;
    const repoRef = database.ref('users/' + userId + '/saved_repos');
    const repo = {
      name: button.getAttribute('data-name'),
      description: button.getAttribute('data-description'),
      forks_count: button.getAttribute('data-forks-count'),
      stargazers_count: button.getAttribute('data-stargazers-count'),
      html_url: button.getAttribute('data-html-url')
    };
    repoRef.child(repo.name).set(repo)
      .then(() => {
        alert("Repo saved")
      })
      .catch((error) => {
        console.error('Error saving repo:', error)
        alert('Failed to save repo. Try again later')
      });
  } else  {
    alert('Please log in to save repository.');
  }
}

const fireLogin = () => {
  if (auth.currentUser) {
    alert('Already logged in');
    setTimeout(() => {
      const userId = auth.currentUser.uid;
      window.location.href = profileUrl + userId;
    }, 2000);
  } else {
    setTimeout(() => {
      window.location.href = loginUrl;
    }, 2000);
  }
}

const viewProfile = () => {
  if (auth.currentUser) {
    const userId = auth.currentUser.uid;
    window.location.href = profileUrl + userId;
  } else {
    alert('Login to view profile page');
  }
}
