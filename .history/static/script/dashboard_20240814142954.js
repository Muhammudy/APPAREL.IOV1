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
    console.log("DOM fully loaded and parsed"); // Add this to check if the script is running
    const themeToggler = document.getElementById('themeToggler');
    if (themeToggler) {
        console.log("Theme toggler found"); // Check if the theme toggler is being selected correctly
        themeToggler.addEventListener('click', () => {
            console.log("Theme toggler clicked"); // Ensure the click event is firing

            let currentTheme = document.body.classList.contains('dark-theme-variables') ? 'dark' : 'light';
            let newTheme = currentTheme === 'light' ? 'dark' : 'light';

            document.body.classList.toggle('dark-theme-variables');
            themeToggler.querySelector('span:nth-child(1)').classList.toggle('active');
            themeToggler.querySelector('span:nth-child(2)').classList.toggle('active');

            document.cookie = `theme=${newTheme}; path=/; max-age=${30*24*60*60};`;

            console.log("New Theme:", newTheme);
            console.log("Document Cookie:", document.cookie);
        });

        let themeFromCookie = document.cookie.split('; ').find(row => row.startsWith('theme='));
        console.log("Theme from cookie:", themeFromCookie); // Check if the cookie is being read correctly
        if (themeFromCookie) {
            let theme = themeFromCookie.split('=')[1];
            if (theme === 'dark') {
                document.body.classList.add('dark-theme-variables');
                themeToggler.querySelector('span:nth-child(1)').classList.add('active');
                themeToggler.querySelector('span:nth-child(2)').classList.remove('active');
            } else {
                themeToggler.querySelector('span:nth-child(1)').classList.remove('active');
                themeToggler.querySelector('span:nth-child(2)').classList.add('active');
            }
        }
    } else {
        console.error("Theme toggler not found in the DOM");
    }
});
