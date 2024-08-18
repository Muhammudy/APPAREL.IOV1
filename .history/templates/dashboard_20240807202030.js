const sideMenu = document.querySelector("aside");
const menuBtn = document.querySelector('#menu-btn');
const closeBtn = document.querySelector('#close-btn');
const themeToggler = document.querySelector(".theme-toggler");




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

function fetchMostPopularSneakers() {
    fetch('http://localhost:4000/get-most-popular')
        .then(response => {
            if (!response.ok) {
                throw new Error(`Network response was not ok ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            let updates = document.querySelectorAll('.update');
            if (data.length === 0) {
                updates.forEach(update => {
                    update.querySelector('.message').innerHTML = '<p>No popular sneakers found.</p>';
                });
            } else {
                updates.forEach((update, index) => {
                    if (index < data.length) {
                        let item = data[index];
                        let shoeName = item.shoeName.replace(/"/g, "&quot;");
                        let brand = item.brand.replace(/"/g, "&quot;");
                        let releaseDate = item.releaseDate;
                        let retailPrice = item.retailPrice;
                        let img = item.imageUrl.replace(/"/g, "&quot;");
                        
                        update.querySelector('.profile-photo img').src = img;
                        update.querySelector('.message').innerHTML = `
                            <p><b>${shoeName} - ${brand}</b></p>
                            <p>Release Date: ${releaseDate}</p>
                            <p>Retail Price: $${retailPrice}</p>
                        `;
                        
                    } else {
                        update.querySelector('.message').innerHTML = '<p>No more popular sneakers found.</p>';
                    }
                });
            }
        })
        .catch(error => console.error('Error:', error));
}

document.addEventListener('DOMContentLoaded', () => {
    fetchMostPopularSneakers();
});




