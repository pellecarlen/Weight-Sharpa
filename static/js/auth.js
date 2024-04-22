// Initialize Firebase
firebase.initializeApp({
    apiKey: "AIzaSyCQiubOrlJYxF3U2Cqd9otCDsS6ISXVmYI",
    authDomain: "weight-sharpa-app.firebaseapp.com",
    projectId: "weight-sharpa-app",
    storageBucket: "weight-sharpa-app.appspot.com",
    messagingSenderId: "87756158274",
    appId: "1:87756158274:web:045603802248c1875084db",
    measurementId: "G-MQFK0940LY"
});

// Redirect unauthenticated users to the login page
firebase.auth().onAuthStateChanged((user) => {
    if (user) {
        // User is signed in, show the content
        document.body.style.display = 'block';
    } else {
        // User is not signed in
        window.location.href = '/login'; // Redirecting to login page
    }
});

// Sign up new users
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

// Sign in existing users
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

// Send password reset email
function sendPasswordReset(email) {
    firebase.auth().sendPasswordResetEmail(email)
        .then(() => {
            console.log('Password reset email sent.');
        })
        .catch((error) => {
            console.error('Error sending password reset email:', error.message);
        });
}
