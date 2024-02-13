//firebase signup configuration
register = () => {
  let email = document.getElementById('email').value
  let password = document.getElementById('password').value
  let rePassword = document.getElementById('re-password').value
  let username = document.getElementById('username').value

  const validations = [
    { isValid: validate_field(username), errorMessage: 'Invalid Username!!' },
    { isValid: validate_email(email), errorMessage: 'Invalid Email!!' },
    { isValid: validate_password(password), errorMessage: 'Invalid Password!!' }
  ];

  for (const validation of validations) {
    if (!validation.isValid) {
      alert(validation.errorMessage);
      return;
    }
  }

  if (password !== rePassword) {
    alert("Password mismatch!");
    return;
  }

  auth.createUserWithEmailAndPassword(email, password)
  .then(() => {
    var user = auth.currentUser
    var database_ref = database.ref()
    var user_data = {
      email : email,
      username : username,
      last_login : Date.now(),
      saved_repos : []
    }
    database_ref.child('users/' + user.uid).set(user_data)
    alert('User Created!!')
    setTimeout(() => {
      window.location.href = "http://127.0.0.1:5000/profile/" + user.uid;
    }, 3000);
  })

  .catch((error) => {
    const error_code = error.code;
    const error_message = error.message;

    alert(error_code)
    alert(error_message)
  })
}
