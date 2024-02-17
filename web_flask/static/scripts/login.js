//firebase login config
login = () => {
  let email = document.getElementById('email').value
  let password = document.getElementById('password').value

  const validations = [
    { isValid: validate_email(email), errorMessage: 'Invalid Email!!' },
    { isValid: validate_password(password), errorMessage: 'Invalid Password!!' }
  ];

  for (const validation of validations) {
    if (!validation.isValid) {
      alert(validation.errorMessage);
      return;
    }
  }

  auth.signInWithEmailAndPassword(email, password)
  .then(() => {
    let user = auth.currentUser
    let database_ref = database.ref()
    let date = new Date();

    let user_data = {
      last_login : date.toUTCString()
    }

    database_ref.child('users/' + user.uid).update(user_data)
    alert('User Logged In!!')
    setTimeout(() => {
      window.location.href = profileUrl + user.uid;
    }, 3000);
  })

  .catch((error) => {
    let error_code = error.code
    let error_message = error.message

    console.log(error_code)
    alert(error_message)
  })
}
