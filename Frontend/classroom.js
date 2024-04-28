document.getElementById('classroomForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const name = document.getElementById('name').value;
    const capacity = document.getElementById('capacity').value;
    const facility_id = document.getElementById('facility_id').value;
    fetch('http://127.0.0.1:5000/api/classrooms', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({name: name, capacity: parseInt(capacity), facility_id: parseInt(facility_id)})
    }).then(response => response.json())
      .then(data => {
          console.log(data);
          fetchClassrooms();  // Refresh the list of classrooms
      })
      .catch(error => console.error('Error:', error));
});

function fetchClassrooms() {
    fetch('http://127.0.0.1:5000/api/classrooms')
        .then(response => response.json())
        .then(classrooms => {
            const table = document.getElementById('classroomsTable');
            table.innerHTML = '';  // Clear previous entries
            classrooms.forEach(classroom => {
                let row = table.insertRow();
                let name = row.insertCell(0);
                let capacity = row.insertCell(1);
                let facility = row.insertCell(2);
                name.innerHTML = classroom.name;
                capacity.innerHTML = classroom.capacity;
                facility.innerHTML = classroom.facility_id;
                // Add more cells for editing and deleting
            });
        })
        .catch(error => console.error('Error fetching classrooms:', error));
}
