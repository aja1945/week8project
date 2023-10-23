document.addEventListener('DOMContentLoaded', function () {
    const registrationForm = document.getElementById('registrationForm');
    registrationForm.addEventListener('submit', function (event) {
        event.preventDefault();
        const formData = new FormData(registrationForm);
        fetch('/user/register', {
            method: 'POST',
            body: JSON.stringify(Object.fromEntries(formData)),
            headers: {
                'Content-Type': 'application/json',
            },
        })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                registrationForm.reset();
            });
    });
});
// Login form submission event (implement similar logic)

    // Function to handle JWT tokens (e.g., store tokens in localStorage)
    function handleJWTToken(token) {
        // Store the token in localStorage
        localStorage.setItem('access_token', token);
    }

    // Function to retrieve JWT tokens
    function getJWTToken() {
        return localStorage.getItem('access_token');
    }
    document.addEventListener('DOMContentLoaded', function () {
        // Function to fetch and display the user's books
        function displayBooks() {
            const bookListItems = document.getElementById('bookListItems');
            bookListItems.innerHTML = '';
    
            fetch('/books/list', {
                method: 'GET',
                headers: {
                    'Authorization': 'Bearer ' + getJWTToken(), // Include JWT token in the request headers
                },
            })
                .then(response => response.json())
                .then(data => {
                    data.forEach(book => {
                        const li = document.createElement('li');
                        li.textContent = `Title: ${book.title}, Author: ${book.author}, Published Date: ${book.published_date}`;
                        bookListItems.appendChild(li);
                    });
                });
        }
    
        // Add Book Form submission event
        const addBookForm = document.getElementById('addBookForm');
        addBookForm.addEventListener('submit', function (event) {
            event.preventDefault();
            const formData = new FormData(addBookForm);
            fetch('/books/create', {
                method: 'POST',
                body: JSON.stringify(Object.fromEntries(formData)),
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + getJWTToken(), // Include JWT token in the request headers
                },
            })
                .then(response => response.json())
                .then(data => {
                    alert(data.message);
                    addBookForm.reset();
                    displayBooks();
                });
        });
    
        // Implement similar logic for update and delete operations
    
        // Call the displayBooks function to initially fetch and display the user's books
        displayBooks();
    });