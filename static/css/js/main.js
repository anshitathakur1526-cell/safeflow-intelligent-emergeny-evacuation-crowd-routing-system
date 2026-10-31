let authToken = null;

async function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    console.log("Login clicked:", username, password);

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username: username, password: password})
        });

        const data = await response.json();
        console.log("Response:", data);

        if (response.ok) {
            authToken = data.token;
            document.getElementById('login-section').style.display = 'none';
            document.getElementById('dashboard-section').style.display = 'block';
            document.getElementById('user-info').innerText = 'Logged in as: ' + username + ' (' + data.role + ')';
            loadRoute('Room_101');
        } else {
            alert('Login Failed: ' + data.message);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Connection error! Check console.');
    }
}

async function triggerEmergency(location) {
    if (!authToken) return alert('Please login first');
    const sensorData = {location: location, severity: 'high'};
    const fakeSignature = "valid_hmac_signature_for_demo";

    try {
        const response = await fetch('/emergency', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + authToken
            },
            body: JSON.stringify({
                location: location,
                sensor_data: sensorData,
                signature: fakeSignature
            })
        });
        const data = await response.json();
        alert(data.message);
        if (response.ok) loadRoute('Room_101');
    } catch (error) {
        console.error('Error:', error);
    }
}

async function loadRoute(startNode) {
    try {
        const response = await fetch('/route/' + startNode);
        const data = await response.json();
        document.getElementById('route-output').innerText =
            'Safest Path: ' + data.route.join(' -> ') + ' | Cost: ' + data.total_cost + ' | ML: ' + data.ml_status;
    } catch (error) {
        console.error('Error:', error);
    }
}