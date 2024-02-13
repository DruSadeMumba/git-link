//firebase login config
login = () => {
  email = document.getElementById('email').value
  password = document.getElementById('password').value

  if (validate_email(email) === false) {
    alert('Invalid Email!!')
    return
  }

  if (validate_password(password) === false) {
    alert('Invalid Password!!')
    return
  }

  auth.signInWithEmailAndPassword(email, password)
  .then(() => {
    var user = auth.currentUser
    var database_ref = database.ref()

    var user_data = {
      last_login : Date.now()
    }

    database_ref.child('users/' + user.uid).update(user_data)
    alert('User Logged In!!')
    setTimeout(function() {
      window.location.href = "http://127.0.0.1:5000/profile/" + user.uid;
    }, 3000);
  })

  .catch((error) => {
    var error_code = error.code
    var error_message = error.message

    alert(error_code)
    alert(error_message)
  })
}
