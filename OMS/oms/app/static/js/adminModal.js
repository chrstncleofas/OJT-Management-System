function validatePassword(studentId) {
    var inputPasswordElement = document.getElementById('adminPassword' + studentId);
    if (inputPasswordElement === null) {
        console.error('Cannot find element with ID:', 'adminPassword' + studentId);
        return;
    }

    var inputPassword = inputPasswordElement.value;
    if (!inputPassword) {
        alert('Please enter the admin password.');
        return;
    }

    fetch("/adminSite/get_admin_password_hash/")
        .then(response => response.json())
        .then(data => {
            const hashedPassword = data.password;
            const inputPasswordHash = CryptoJS.SHA256(inputPassword).toString();

            if (hashedPassword === inputPasswordHash) {
                archiveStudent(studentId);
            } else {
                alert('Incorrect password');
            }
        })
        .catch(error => console.error('Error:', error));
}

function archiveStudent(studentId) {
    const url = `/adminSite/archivedStudent/${studentId}/`;
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify({
            studentID: studentId
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert(data.message);
            location.reload();
        } else {
            alert(data.message);
        }
    })
    .catch(error => console.error('Error:', error));
}