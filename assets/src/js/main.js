import '../fonts/Sk-Modernist-Regular.otf'
import 'bootstrap/js/src/collapse'
import 'bootstrap/js/src/dropdown'
import reportValidity from 'report-validity'

const feather = require('feather-icons')
feather.replace()


// Localize mail validation msg.
var email_msg = "Email and confirmation email don't match."
if (document.documentElement.lang === 'es'){
	var email_msg = "La dirección de correo y la confirmación de la dirección de correo no coinciden."
}

// Function to compare two emails and send error msg.
function validateEmail(email, email_confirm) {
	let a = document.getElementById(email),
		b = document.getElementById(email_confirm)
	b.addEventListener('input', () => {
		if (a.value !== b.value) {
			b.setCustomValidity(email_msg)
			reportValidity(b);
		} else {
			b.setCustomValidity('')
			reportValidity(b);
		}
	})
}

// Check for email field in sign up form.
var emailA =  document.getElementById('id_user-email');
if (typeof(emailA) != 'undefined' && emailA != null)
{
	validateEmail('id_user-email', 'id_user-email_confirm')
}

// Check for email field in update email form.
var emailB =  document.getElementById('id_email');
if (typeof(emailB) != 'undefined' && emailB != null)
{
	validateEmail('id_email', 'id_email_confirm')
}

