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

    // Initial theme setup based on cookie
    let themeFromCookie = document.cookie.split('; ').find(row => row.startsWith('theme='));
    if (themeFromCookie) {
        let theme = themeFromCookie.split('=')[1];
        if (theme === 'dark') {
            document.body.classList.add('dark-theme-variables');
            themeToggler.querySelector('span:nth-child(2)').classList.add('active'); // Dark mode icon
            themeToggler.querySelector('span:nth-child(1)').classList.remove('active'); // Light mode icon
        } else {
            document.body.classList.remove('dark-theme-variables');
            themeToggler.querySelector('span:nth-child(1)').classList.add('active'); // Light mode icon
            themeToggler.querySelector('span:nth-child(2)').classList.remove('active'); // Dark mode icon
        }
    } else {
        // If no theme is set, default to light
        document.body.classList.remove('dark-theme-variables');
        themeToggler.querySelector('span:nth-child(1)').classList.add('active'); // Light mode icon
        themeToggler.querySelector('span:nth-child(2)').classList.remove('active'); // Dark mode icon
    }

    // Add event listener for the theme toggler
    themeToggler.addEventListener('click', () => {
        let currentTheme = document.body.classList.contains('dark-theme-variables') ? 'dark' : 'light';
        let newTheme = currentTheme === 'light' ? 'dark' : 'light';

        // Toggle the theme class
        document.body.classList.toggle('dark-theme-variables');
        themeToggler.querySelector('span:nth-child(2)').classList.toggle('active'); // Dark mode icon
        themeToggler.querySelector('span:nth-child(1)').classList.toggle('active'); // Light mode icon

        // Set the cookie with the new theme
        document.cookie = `theme=${newTheme}; path=/; max-age=${30*24*60*60};`;

        console.log("New Theme:", newTheme); // Debugging
        console.log("Document Cookie:", document.cookie); // Debugging
    });
});
