//firebase user profile
document.addEventListener("DOMContentLoaded", () => {
  firebase.auth().onAuthStateChanged((user) => {
    if (user) {
      const userId = user.uid;
      const userRef = firebase.database().ref('users/' + userId);

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
});
