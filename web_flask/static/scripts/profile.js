//firebase user profile
document.addEventListener("DOMContentLoaded", function() {
  firebase.auth().onAuthStateChanged(function(user) {
    if (user) {
      const userId = user.uid;
      const userRef = firebase.database().ref('users/' + userId);

      userRef.on('value', function(snapshot) {
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
