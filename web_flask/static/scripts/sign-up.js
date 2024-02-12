//firebase signup config
var firebaseConfig = {
  apiKey: "AIzaSyAk2bynVPfj-5rW4y0K6256LdSE62cXDB0",
  authDomain: "git-link-d9cc9.firebaseapp.com",
  databaseURL: "https://git-link-d9cc9-default-rtdb.firebaseio.com/",
  projectId: "git-link-d9cc9",
  storageBucket: "git-link-d9cc9.appspot.com",
  messagingSenderId: "911947476553",
  appId: "1:911947476553:web:e8dbbbe137c97b524fd998",
  measurementId: "G-27ZGX5VGJS"
};

firebase.initializeApp(firebaseConfig);
const auth = firebase.auth();
const database = firebase.database();

function register () {
  let email = document.getElementById('email').value
  let password = document.getElementById('password').value
  let rePassword = document.getElementById('re-password').value
  let username = document.getElementById('username').value

  if (validate_field(username) === false) {
    alert('Invalid Username!!')
    return
  }

  if (validate_email(email) === false) {
    alert('Invalid Email!!')
    return
  }

  if (validate_password(password) === false) {
    alert('Invalid Password!!')
    return
  }

  if (password !== rePassword) {
    alert("Password mismatch!")
    return
  }


  auth.createUserWithEmailAndPassword(email, password)
  .then(function() {
    var user = auth.currentUser
    var database_ref = database.ref()
    var user_data = {
      email : email,
      username : username,
      last_login : Date.now()
    }
    database_ref.child('users/' + user.uid).set(user_data)
    alert('User Created!!')
    setTimeout(function() {
      window.location.href = "http://127.0.0.1:5000/profile/" + user.uid;
    }, 3000);
  })

  .catch(function(error) {
    const error_code = error.code;
    const error_message = error.message;

    alert(error_message)
  })
}


// Validate Functions
function validate_email(email) {
  let expression = /^[^@]+@\w+(\.\w+)+\w$/
  return expression.test(email) === true;
}

function validate_password(password) {
  return password >= 6;
}

function validate_field(field) {
  if (field == null) {
    return false
  }

  return field.length > 0;
}
