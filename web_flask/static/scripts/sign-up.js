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
    let user = auth.currentUser
    let database_ref = database.ref()
    const date = new Date();
    let user_data = {
      email : email,
      username : username,
      last_login : date.toUTCString(),
      saved_repos : []
    }
    
    database_ref.child('users/' + user.uid).set(user_data)
    alert('User Created!!')
    setTimeout(() => {
      window.location.href = profileUrl + user.uid;
    }, 3000);
  })

  .catch((error) => {
    const error_code = error.code;
    const error_message = error.message;

    console.log(error_code)
    alert(error_message)
  })
}
