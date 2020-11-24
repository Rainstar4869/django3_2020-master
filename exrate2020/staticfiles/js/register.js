const submitBtn = document.querySelector("#login-form-submit");
const emailField = document.querySelector("#email");
const emailField_checker = document.querySelector("#email_check");
const emailField_checker_wrapper = document.querySelector("#email_check_wrapper");
const usernameField = document.querySelector("#username");
const usernameField_checker = document.querySelector("#username_check");
const usernameField_checker_wrapper = document.querySelector("#username_check_wrapper");

if (emailField_checker_wrapper) {
  emailField_checker_wrapper.classList.add("d-none");
}
if (usernameField_checker_wrapper) {
  usernameField_checker_wrapper.classList.add("d-none");
}

emailField.addEventListener("keyup", (e) => {
  const emailVal = e.target.value;

  // emailField.classList.remove("is-invalid");

  if (emailVal.length > 3) {
    fetch("/webauth/validate-email", {
      body: JSON.stringify({ email: emailVal }),
      method: "POST",
      // headers: {
		// 	'Authorization': data.token_type + ' ' + data.access_token,
		// }
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.email_error) {
          submitBtn.disabled = true;
          emailField_checker_wrapper.classList.remove("d-none");
          emailField.classList.add("is-invalid");
          emailField_checker.innerHTML = `<i class="icon-times-circle text-danger"></i>`;
        } else {
          submitBtn.removeAttribute("disabled");
          emailField_checker_wrapper.classList.remove("d-none");
          emailField.classList.remove("is-invalid");
          emailField_checker.innerHTML = `<i class="icon-check-circle text-success"></i>`;
        }
      });
  }
});


usernameField.addEventListener("keyup", (e) => {
  const usernameVal = e.target.value;

  if (usernameVal.length > 3) {
    fetch("/webauth/validate-username/", {
      body: JSON.stringify({ username: usernameVal }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log(data)
        if (data.username_error) {
          usernameField.classList.add("is-invalid");
          usernameField_checker_wrapper.classList.remove("d-none");
          usernameField_checker.innerHTML = `<i class="icon-times-circle text-danger"></i>`;
          submitBtn.disabled = true;
        } else {
          submitBtn.removeAttribute("disabled");
          usernameField_checker_wrapper.classList.remove("d-none");
          usernameField.classList.remove("is-invalid");
          usernameField_checker.innerHTML = `<i class="icon-check-circle text-success"></i>`;
        }
      });
  }
});