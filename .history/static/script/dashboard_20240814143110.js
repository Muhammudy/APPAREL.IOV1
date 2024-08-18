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
    console.log("DOM fully loaded and parsed"); // Debugging

    const themeToggler = document.getElementById('themeToggler');

    if (themeToggler) {
        console.log("Theme toggler found"); // Debugging

        // Check the current theme from the cookie
        let themeFromCookie = document.cookie.split('; ').find(row => row.startsWith('theme='));
        if (themeFromCookie) {
            let theme = themeFromCookie.split('=')[1];
            if (theme === 'dark') {
                document.body.classList.add('dark-theme-variables');
                themeToggler.querySelector('span:nth-child(1)').classList.add('active');
                themeToggler.querySelector('span:nth-child(2)').classList.remove('active');
            } else {
                document.body.classList.remove('dark-theme-variables');
                themeToggler.querySelector('span:nth-child(1)').classList.remove('active');
                themeToggler.querySelector('span:nth-child(2)').classList.add('active');
            }
        } else {
            // If no theme is set, default to light
            document.body.classList.remove('dark-theme-variables');
            themeToggler.querySelector('span:nth-child(1)').classList.remove('active');
            themeToggler.querySelector('span:nth-child(2)').classList.add('active');
        }

        // Add event listener for the theme toggler
        themeToggler.addEventListener('click', () => {
            let currentTheme = document.body.classList.contains('dark-theme-variables') ? 'dark' : 'light';
            let newTheme = currentTheme === 'light' ? 'dark' : 'light';

            // Toggle the theme class
            document.body.classList.toggle('dark-theme-variables');
            themeToggler.querySelector('span:nth-child(1)').classList.toggle('active');
            themeToggler.querySelector('span:nth-child(2)').classList.toggle('active');

            // Set the cookie with the new theme
            document.cookie = `theme=${newTheme}; path=/; max-age=${30*24*60*60};`;

            console.log("New Theme:", newTheme); // Debugging
            console.log("Document Cookie:", document.cookie); // Debugging
        });
    } else {
        console.error("Theme toggler not found in the DOM");
    }
});
