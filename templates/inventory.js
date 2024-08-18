function fetchSneakerData() {
    const info = document.getElementById('info').value;
    const category = document.getElementById('category').value;

    if (info.length > 2) {  // Only fetch data if input length is greater than 2
        fetch('http://localhost:4000/get-sneaker-data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ category, info })
        })
        .then(response => response.json())
        .then(data => {
            let resultArea = document.getElementById('results');
            resultArea.innerHTML = '';

            if (data.length === 0) {
                resultArea.innerHTML = '<li>No results found</li>';
            } else {
                data.forEach(item => {
                    let listItem = document.createElement('li');
                    listItem.innerText = `${item.shoeName} - ${item.brand}`;
                    resultArea.appendChild(listItem);
                    
                    // Add hidden inputs to the form for each result item
                    let form = document.querySelector('form');
                    let hiddenInput = document.createElement('input');
                    hiddenInput.type = 'hidden';
                    hiddenInput.name = 'result';
                    hiddenInput.value = `${item.shoeName} - ${item.brand}`;
                    form.appendChild(hiddenInput);
                });
            }
        })
        .catch(error => console.error('Error:', error));
    }
}

function openModal(shoeName, brand, sku) {
    document.getElementById('shoe-name').value = shoeName;
    document.getElementById('shoe-brand').value = brand;
    document.getElementById('sku-info').value = sku;
    document.getElementById('modal').style.display = 'block';
}

function closeModal() {
    document.getElementById('modal').style.display = 'none';
}
