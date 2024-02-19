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
      window.location.href = profileUrl;
    }, 2000);
  } else {
    setTimeout(() => {
      window.location.href = loginUrl;
    }, 2000);
  }
}

const shareOptions = () => {
  closeNav();
  document.getElementById("social-share").style.width = "400px";
  document.querySelector(".wrapper").style.opacity = "0.3";
};

const closeShare = () => {
  document.getElementById("social-share").style.width = "0px";
  document.querySelector(".wrapper").style.opacity = "1";
  openNav();
};

const links = encodeURI("https://github.com/DruSadeMumba/git-link");
const msg = encodeURIComponent('Hey, check this repo out');
const title = encodeURIComponent('GIT-LINK');
const fb = document.querySelector('.facebook');
const twitter = document.querySelector('.twitter');
const linkedIn = document.querySelector('.linkedin');
const reddit = document.querySelector('.reddit');
const whatsapp = document.querySelector('.whatsapp');
const telegram = document.querySelector('.telegram');


fb.href = `https://www.facebook.com/share.php?u=${links}`;
twitter.href = `https://twitter.com/share?&url=${links}&text=${msg}&hashtags=github,alx`;
linkedIn.href = `https://www.linkedin.com/sharing/share-offsite/?url=${links}`;
reddit.href = `https://www.reddit.com/submit?url=${links}&title=${title}`;
whatsapp.href = `https://api.whatsapp.com/send?text=${msg}: ${links}`;
telegram.href = `https://telegram.me/share/url?url=${links}&text=${msg}`;



