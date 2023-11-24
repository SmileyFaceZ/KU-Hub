// config.js
async function getFirebaseConfig() {
    const response = await fetch('/path/to/firebaseConfig.json');
    return await response.json();
}

export { getFirebaseConfig };
