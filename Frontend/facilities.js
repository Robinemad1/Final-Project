// document.getElementById('facilityForm').addEventListener('submit', function(e) {
//     e.preventDefault();
//     const formData = new FormData(this);
//     fetch('/api/facilities', {
//         method: 'POST',
//         body: JSON.stringify(Object.fromEntries(formData)),
//         headers: {
//             'Content-Type': 'application/json'
//         }
//     }).then(response => response.json())
//       .then(data => console.log(data))
//       .catch(error => console.error('Error:', error));
// });


async function fetchFacility() {
    const response = await fetch('http://127.0.0.1:5000/api/facilities');
    const res = await response.json();
    console.log(res)
    // Code to dynamically populate table with facilities
}
