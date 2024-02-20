//firebase user profile
document.addEventListener("DOMContentLoaded", () => {
  auth.onAuthStateChanged((user) => {
    if (user) {
      const userId = user.uid;
      const userRef = database.ref('users/' + userId);
      const repoRef = database.ref('users/' + userId + '/saved_repos');

      userRef.on('value', (snapshot) => {
        const userData = snapshot.val();
        document.getElementById('username').innerText = userData.username;
        document.getElementById('email').innerText = userData.email;
      });
      repoRef.on('value', (snapshot) => {
        const repoData = snapshot.val();
        const savedContainer = document.querySelector('.scroll');

        savedContainer.innerHTML = '';
        for (const repoKey in repoData) {
          const repo = repoData[repoKey];
          const repoCard = document.createElement('div');
          repoCard.classList.add('card');
          repoCard.innerHTML =
            `<h5 id="repo-name">${repo.name}</h5>
            <p id="description">${repo.description}</p>
            <p id="more-info">
              <span id="share" onclick="shareRepo('${repo.html_url}')">
                <img src="../static/images/share.png" alt="share">
              </span>
              <span id="link">
                <a href="${repo.html_url}" target="_blank">
                  <img src="../static/images/link.png" alt="link">
                </a>
              </span>
            </p>
          `;
          savedContainer.appendChild(repoCard);
        }
      });
    } else {
      console.log('No user signed in.');
      setTimeout(() => {
        window.location.href = loginUrl;
      }, 3000);
    }
  });

  document.getElementById('logout').addEventListener('click', () => {
    auth.signOut().then(() => {
      console.log('User signed out.');
      setTimeout(() => {
        window.location.href = searchUrl;
      }, 2000);
    }).catch((error) => {
      console.log('Error signing out: ', error);
    });
  });
});

const shareRepo = (url) => {
  const links = encodeURI(url);
  const txt = encodeURIComponent('Hey, check out this repo');
  const title = encodeURIComponent('');
  const fb = document.querySelector('.facebook');
  const twitter = document.querySelector('.twitter');
  const linkedIn = document.querySelector('.linkedin');
  const reddit = document.querySelector('.reddit');
  const whatsapp = document.querySelector('.whatsapp');
  const telegram = document.querySelector('.telegram');

  fb.href = `https://www.facebook.com/share.php?u=${links}`;
  twitter.href = `https://twitter.com/share?&url=${links}&text=${txt}&hashtags=github,alx`;
  linkedIn.href = `https://www.linkedin.com/sharing/share-offsite/?url=${links}`;
  reddit.href = `https://www.reddit.com/submit?url=${links}&title=${title}`;
  whatsapp.href = `https://api.whatsapp.com/send?text=${txt}: ${links}`;
  telegram.href = `https://telegram.me/share/url?url=${links}&text=${txt}`;
  
  document.getElementById("social-share").style.width = "400px";
  document.querySelector(".wrapper").style.opacity = "0.4";
}

const closeShare = () => {
  document.getElementById("social-share").style.width = "0px";
  document.querySelector(".wrapper").style.opacity = "1";
};
