export function nav() {

const nav = document.getElementById("nav");
    const toggle = document.getElementById("nav-toggle");
    const navLinks = nav.querySelectorAll("a");
    const symbol = document.getElementById("symbol")

    function openNav() {
        nav.classList.add("show");
        nav.removeAttribute("aria-hidden");
        toggle.setAttribute("aria-expanded", "true");
        toggle.setAttribute("aria-label", "Close menu");
        navLinks.forEach(link => link.removeAttribute("tabindex"));
        symbol.classList.add("rotated");
    }

    function closeNav() {
        nav.classList.remove("show");
        nav.setAttribute("aria-hidden", "true");
        toggle.setAttribute("aria-expanded", "false");
        toggle.setAttribute("aria-label", "Open menu");
        navLinks.forEach(link => link.setAttribute("tabindex", "-1"));
        symbol.classList.remove("rotated");
    }
    function toggleNav() {
        if (nav.classList.contains("show")) {
        closeNav();
        } else {
        openNav();
        }
    }

    // Toggle via the hamburger button (mouse, keyboard, and screen readers all work natively on a <button>)
    toggle.addEventListener("click", (e) => {
        e.stopPropagation();
        toggleNav();
    });

    // Prevent clicks inside the open menu from bubbling and closing it
    nav.addEventListener("click", (e) => {
        e.stopPropagation();
    });

    // Close when clicking anywhere else
    document.addEventListener("click", () => {
        if (nav.classList.contains("show")) closeNav();
    });

    // Close on Escape, and return focus to the toggle button
    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape" && nav.classList.contains("show")) {
        closeNav();
        toggle.focus();
        }
    });

}