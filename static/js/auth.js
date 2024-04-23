// Script for managing user authentication state and redirections.

// Sign up new users and handle redirection after successful registration.
function signUp(email, password) {
    firebase.auth().createUserWithEmailAndPassword(email, password)
        .then((userCredential) => {
            console.log('User created and signed in');
            window.location.href = '/'; // Redirecting to home page
        })
        .catch((error) => {
            console.error('Error signing up:', error.message);
        });
}

// Sign in existing users and handle redirection after successful login.
function signIn(email, password) {
    firebase.auth().signInWithEmailAndPassword(email, password)
        .then((userCredential) => {
            console.log('User signed in');
            window.location.href = '/'; // Redirecting to home page
        })
        .catch((error) => {
            console.error('Error signing in:', error.message);
        });
}

// Send a password reset email to the provided email address.
function sendPasswordReset(email) {
    firebase.auth().sendPasswordResetEmail(email)
        .then(() => {
            console.log('Password reset email sent.');
        })
        .catch((error) => {
            console.error('Error sending password reset email:', error.message);
        });
}
