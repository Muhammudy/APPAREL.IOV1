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




document.addEventListener('DOMContentLoaded', function() {
    const themeToggler = document.getElementById('themeToggler');
    themeToggler.addEventListener('click', () => {
        let currentTheme = document.body.classList.contains('dark-theme-variables') ? 'dark' : 'light';
        let newTheme = currentTheme === 'light' ? 'dark' : 'light';
        
        // Update the cookie via JavaScript
        document.cookie = theme=${newTheme}; path=/; max-age=${30*24*60*60};;

        // Toggle the theme
        document.body.classList.toggle('dark-theme-variables');
        console.log(document.cookie); // See the cookies in the console
    });
})


