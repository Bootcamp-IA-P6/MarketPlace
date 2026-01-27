document.addEventListener("DOMContentLoaded", () => {
    // Swiper root element
    const el = document.querySelector(".mySwiper");
    if (!el) return;

    // We always render a fixed number of slides (products + placeholders)
    const totalSlides = el.querySelectorAll(".swiper-slide").length;

    // Init Swiper (single instance)
    new Swiper(".mySwiper", {
        // 3D coverflow look
        effect: "coverflow",
        grabCursor: true,
        centeredSlides: true,

        // Visible slides
        slidesPerView: 3,
        spaceBetween: 30,

        // Move one slide at a time
        slidesPerGroup: 1,

        // Infinite loop
        loop: true,
        loopedSlides: totalSlides,
        loopAdditionalSlides: totalSlides,

        // Auto move every  5 seconds
        autoplay: {
            delay: 5000,
            disableOnInteraction: false,
            pauseOnMouseEnter: true,
        },

        // Allow clicking links inside slides
        preventClicks: false,
        preventClicksPropagation: false,

        // Transition speed
        speed: 650,

        // Coverflow settings
        coverflowEffect: {
            rotate: 0,
            stretch: 0,
            depth: 140,
            modifier: 1,
            slideShadows: false,
        },

        // Arrow navigation
        navigation: {
            nextEl: ".swiper-button-next",
            prevEl: ".swiper-button-prev",
        },

        // Responsive layout
        breakpoints: {
            0: { slidesPerView: 1, spaceBetween: 20 },
            768: { slidesPerView: 2, spaceBetween: 25 },
            1024: { slidesPerView: 3, spaceBetween: 30 },
        },
    });
});
