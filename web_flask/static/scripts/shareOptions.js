//Share functions
const setSocialMediaLinks = (url, msg, title) => {
  const links = encodeURI(url);
  const txt = encodeURIComponent(msg);
  const encodedTitle = encodeURIComponent(title);

  const fb = document.querySelector('.facebook');
  const twitter = document.querySelector('.twitter');
  const linkedIn = document.querySelector('.linkedin');
  const reddit = document.querySelector('.reddit');
  const whatsapp = document.querySelector('.whatsapp');
  const telegram = document.querySelector('.telegram');

  fb.href = `https://www.facebook.com/share.php?u=${links}`;
  twitter.href = `https://twitter.com/share?&url=${links}&text=${txt}&hashtags=github,alx`;
  linkedIn.href = `https://www.linkedin.com/sharing/share-offsite/?url=${links}`;
  reddit.href = `https://www.reddit.com/submit?url=${links}&title=${encodedTitle}`;
  whatsapp.href = `https://api.whatsapp.com/send?text=${txt}: ${links}`;
  telegram.href = `https://telegram.me/share/url?url=${links}&text=${txt}`;
}

const shareRepo = (url) => {
  setSocialMediaLinks(url, 'Hey, check out this repo', '');
  document.getElementById("social-share").style.width = "600px";
  document.querySelector(".wrapper").style.opacity = "0.4";
}

const shareOptions = () => {
  setSocialMediaLinks('https://github.com/DruSadeMumba/git-link', 'Hey, check this repo out!', 'GIT-LINK');
  closeNav();
  document.getElementById("social-share").style.width = "600px";
  document.querySelector(".wrapper").style.opacity = "0.4";
};

const closeShare = () => {
  document.getElementById("social-share").style.width = "0px";
  document.querySelector(".wrapper").style.opacity = "1";

  if (typeof openNav === 'function') {
    openNav();
  }
};
