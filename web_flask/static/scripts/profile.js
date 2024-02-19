//firebase user profile
document.addEventListener("DOMContentLoaded", () => {
  auth.onAuthStateChanged((user) => {
    if (user) {
      const userId = user.uid;
      const userRef = database.ref('users/' + userId);

      userRef.on('value', (snapshot) => {
        const userData = snapshot.val();
        document.getElementById('username').innerText = userData.username;
        document.getElementById('email').innerText = userData.email;
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
