//firebase user profile
document.addEventListener("DOMContentLoaded", function() {
  firebase.auth().onAuthStateChanged(function(user) {
    if (user) {
      var userId = user.uid;
      var userRef = firebase.database().ref('users/' + userId);

      userRef.on('value', function(snapshot) {
        var userData = snapshot.val();
        document.getElementById('username').innerText = userData.username;
        document.getElementById('email').innerText = userData.email;
      });
    } else {
      console.log('No user signed in.');
      setTimeout(() => {
        window.location.href = "http://127.0.0.1:5000/profile/" + user.uid;
      }, 3000);
    }
  });
});

