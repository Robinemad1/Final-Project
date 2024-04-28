document.getElementById('childForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const firstname = document.getElementById('firstname').value;
    const lastname = document.getElementById('lastname').value;
    const age = document.getElementById('age').value;
    const room_id = document.getElementById('room_id').value;
    fetch('http://127.0.0.1:5000/api/children', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({firstname: firstname, lastname: lastname, age: parseInt(age), room_id: parseInt(room_id)})
    }).then(response => response.json())
      .then(data => {
          console.log(data);
          fetchChildren();  // Refresh the list of children
      })
      .catch(error => console.error('Error:', error));
});

function fetchChildren() {
    fetch('http://127.0.0.1:5000/api/children')
        .then(response => response.json())
        .then(children => {
            const table = document.getElementById('childrenTable');
            table.innerHTML = '';  // Clear previous entries
            children.forEach(child => {
                let row = table.insertRow();
                let firstname = row.insertCell(0);
                let lastname = row.insertCell(1);
                let age = row.insertCell(2);
                let room = row.insertCell(3);
                firstname.innerHTML = child.firstname;
                lastname.innerHTML = child.lastname;
                age.innerHTML = child.age;
                room.innerHTML = child.room_id;
                // Add more cells for editing and deleting
            });
        })
        .catch(error => console.error('Error fetching children:', error));
}
