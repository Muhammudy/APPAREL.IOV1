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
    console.log("DOM fully loaded and parsed");

    const themeToggler = document.getElementById('themeToggler');
    console.log("Theme Toggler:", themeToggler);

    themeToggler.addEventListener('click', () => {
        let currentTheme = document.body.classList.contains('dark-theme-variables') ? 'dark' : 'light';
        let newTheme = currentTheme === 'light' ? 'dark' : 'light';

        // Log the current and new theme
        console.log("Current Theme:", currentTheme);
        console.log("New Theme:", newTheme);

        // Toggle the theme class
        document.body.classList.toggle('dark-theme-variables');

        // Set the cookie
        document.cookie = `theme=${newTheme}; path=/; max-age=${30*24*60*60};`;

        // Log the updated cookie
        console.log("Updated Document Cookie:", document.cookie);
    });

    let themeFromCookie = document.cookie.split('; ').find(row => row.startsWith('theme='));
    console.log("Theme from Cookie:", themeFromCookie);

    if (themeFromCookie) {
        let theme = themeFromCookie.split('=')[1];
        if (theme === 'dark') {
            document.body.classList.add('dark-theme-variables');
            console.log("Dark theme applied from cookie.");
        } else {
            console.log("Light theme applied from cookie.");
        }
    } else {
        console.log("No theme cookie found, using default theme.");
    }
});


