// Validate Functions
validate_email = (email) => {
  let expression = /^[^@]+@\w+(\.\w+)+\w$/;
  return expression.test(email) === true;
}

validate_password = (password) => {
  return password >= 6;
}

validate_field = (field) => {
  if (field == null) {
    return false;
  }

  return field.length > 0;
}
