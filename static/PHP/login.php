<?php
// Database connection details
$host = "localhost";    // Change as per your setup
$dbUsername = "root";   // Your database username
$dbPassword = "";       // Your database password
$dbName = "login";      // Your database name

// Establish a connection to the MySQL database
$conn = new mysqli($host, $dbUsername, $dbPassword, $dbName);

// Check if the connection is successful
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Get the username and password from the login form
$username = $_POST['username'];
$password = $_POST['password'];

// Prevent SQL injection by using prepared statements
$sql = "SELECT * FROM users WHERE username = ? AND password = ?";
$stmt = $conn->prepare($sql);
$stmt->bind_param("ss", $username, $password);
$stmt->execute();
$result = $stmt->get_result();

// Check if any matching user is found
if ($result->num_rows > 0) {
    echo "Login successful!";
    // You can redirect to a dashboard or another page here
    // header("Location: dashboard.php");
} else {
    echo "Invalid username or password.";
}

// Close the prepared statement and connection
$stmt->close();
$conn->close();
?>
