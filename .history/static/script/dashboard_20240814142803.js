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




document.addEventListener('DOMContentLoaded', function() {
    const themeToggler = document.getElementById('themeToggler');

    themeToggler.addEventListener('click', () => {
        // Determine the current theme based on the presence of the class
        let currentTheme = document.body.classList.contains('dark-theme-variables') ? 'dark' : 'light';
        let newTheme = currentTheme === 'light' ? 'dark' : 'light';
        
        // Toggle the theme class
        document.body.classList.toggle('dark-theme-variables');
        themeToggler.querySelector('span:nth-child(1)').classList.toggle('active');
        themeToggler.querySelector('span:nth-child(2)').classList.toggle('active');

        // Set the cookie
        document.cookie = `theme=${newTheme}; path=/; max-age=${30*24*60*60};`;

        // Log the current theme and cookie for debugging
        console.log("New Theme:", newTheme);
        console.log("Document Cookie:", document.cookie);
    });

    // Apply the theme based on the cookie value on page load
    let themeFromCookie = document.cookie.split('; ').find(row => row.startsWith('theme='));
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
});
