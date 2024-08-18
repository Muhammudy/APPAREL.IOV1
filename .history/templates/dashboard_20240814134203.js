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
        // Determine the current theme based on the presence of the class
        let currentTheme = document.body.classList.contains('dark-theme-variables') ? 'dark' : 'light';
        let newTheme = currentTheme === 'light' ? 'dark' : 'light';
        
        // Toggle the theme class on the body
        document.body.classList.toggle('dark-theme-variables');

        // Set the cookie to the new theme with a max age of 30 days
        document.cookie = `theme=${newTheme}; path=/; max-age=${30*24*60*60};`;

        // Log the current cookies to the console for debugging
        console.log(document.cookie);
    });

    // Immediately apply the theme based on the cookie value on page load
    let themeFromCookie = document.cookie.split('; ').find(row => row.startsWith('theme='));
    if (themeFromCookie) {
        let theme = themeFromCookie.split('=')[1];
        if (theme === 'dark') {
            document.body.classList.add('dark-theme-variables');
        } else {
            document.body.classList.remove('dark-theme-variables');
        }
    }

    // Log the current cookies to the console for debugging
    console.log(document.cookie);
});
