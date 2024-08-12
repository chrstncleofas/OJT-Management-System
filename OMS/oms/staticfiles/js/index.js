const csrfToken = "{{ csrf_token }}";

$(".navbar-toggler").click(function (e) {
    e.preventDefault();
    $("#wrapper").toggleClass("toggled");
});
document.getElementById('id_image').addEventListener('change', function () {
    if (this.files && this.files[0]) {
        document.getElementById('timeInBtn').disabled = false;
        document.getElementById('timeOutBtn').disabled = false;
    }
});
// 
function previewImage(event) {
    var preview = document.getElementById('preview');
    var file = document.getElementById('id_image').files[0];
    var reader = new FileReader();
    reader.onload = function () {
        preview.src = reader.result;
        preview.style.display = 'block';
    }
    if (file) {
        reader.readAsDataURL(file);
    }
}
document.getElementById('id_image').addEventListener('change', previewImage);

// 
function submitRejection(studentId) {
    const reason = document.getElementById(`rejectReason${studentId}`).value;
    if (reason.trim() === "") {
        alert("Please provide a reason for rejection.");
        return;
    }
    const url = "{% url 'reject_students' 0 %}".replace('/0/', '/' + studentId + '/');
    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ reason: reason })
    }).then(response => {
        if (response.ok) {
            window.location.reload();
        } else {
            alert('Failed to reject student.');
        }
    });
}