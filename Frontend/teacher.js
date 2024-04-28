document.getElementById('teacherForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const firstname = document.getElementById('firstname').value;
    const lastname = document.getElementById('lastname').value;
    const room_id = document.getElementById('room_id').value;
    fetch('http://127.0.0.1:5000/api/teachers', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({firstname: firstname, lastname: lastname, room_id: parseInt(room_id)})
    }).then(response => response.json())
      .then(data => {
          console.log(data);
          fetchTeachers();  // Refresh the list of teachers
      })
      .catch(error => console.error('Error:', error));
});

function fetchTeachers() {
    fetch('http://127.0.0.1:5000/api/teachers')
        .then(response => response.json())
        .then(teachers => {
            const table = document.getElementById('teachersTable');
            table.innerHTML = '';  // Clear previous entries
            teachers.forEach(teacher => {
                let row = table.insertRow();
                let firstname = row.insertCell(0);
                let lastname = row.insertCell(1);
                let room = row.insertCell(2);
                firstname.innerHTML = teacher.firstname;
                lastname.innerHTML = teacher.lastname;
                room.innerHTML = teacher.room_id;
                // Add more cells for editing and deleting
            });
        })
        .catch(error => console.error('Error fetching teachers:', error));
}
