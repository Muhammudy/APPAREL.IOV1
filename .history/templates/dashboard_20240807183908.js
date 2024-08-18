const sideMenu = document.querySelector("aside");
const menuBtn = document.querySelector('#menu-btn');
const closeBtn = document.querySelector('#close-btn');
const themeToggler = document.querySelector(".theme-toggler");


function fetchMostPopularSneakers() {
    fetch('http://localhost:4000/get-most-popular')
        .then(response => {
            if (!response.ok) {
                throw new Error(`Network response was not ok ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            let resultArea = document.getElementById('results');
            resultArea.innerHTML = '';

            if (data.length === 0) {
                resultArea.innerHTML = '<li>No popular sneakers found.</li>';
            } else {
                data.forEach(item => {
                    let shoeName = item.shoeName.replace(/"/g, "&quot;");
                    let brand = item.brand.replace(/"/g, "&quot;");
                    let sku = item.styleID.replace(/"/g, "&quot;");
                    let description = item.description.replace(/"/g, "&quot;");
                    let imageUrl = item.imageUrl.replace(/"/g, "&quot;");
                    let releaseDate = item.releaseDate;
                    let retailPrice = item.retailPrice;
                    let img = item.img;
                    
                    let listItem = document.createElement('li');
                    listItem.innerHTML = `
                        <a href="#" onclick='showProductDetails("${shoeName.replace(/'/g, "&#39;").replace(/"/g, "&quot;")}", "${brand.replace(/'/g, "&#39;").replace(/"/g, "&quot;")}", "${sku.replace(/'/g, "&#39;").replace(/"/g, "&quot;")}", "${description.replace(/'/g, "&#39;").replace(/"/g, "&quot;")}", "${imageUrl}", "${releaseDate}", "${retailPrice}", "${img}")'>
                            <img src="${imageUrl}" alt="${shoeName}" class="result-image">
                            <p>${item.shoeName} - ${item.brand}</p>
                            <p>Release Date: ${releaseDate}</p>
                            <p>Retail Price: $${retailPrice}</p>
                        </a>
                    `;
                    resultArea.appendChild(listItem);
                });
            }
        })
        .catch(error => console.error('Error:', error));
}




//show the side bar
menuBtn.addEventListener('click', () => {
    sideMenu.style.display = 'block';
});


//close the side bar
closeBtn.addEventListener('click', ()=> {

    sideMenu.style.display = 'none';



});


themeToggler.addEventListener('click',()=>{

    document.body.classList.toggle('dark-theme-variables');
    themeToggler.querySelector('span:nth-child(1)').classList.toggle('active');
    themeToggler.querySelector('span:nth-child(2)').classList.toggle('active');


})




