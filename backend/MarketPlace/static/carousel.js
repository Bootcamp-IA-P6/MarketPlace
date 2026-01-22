document.addEventListener("DOMContentLoaded", () => {
    new Swiper(".mySwiper", {
        effect: "coverflow",
        grabCursor: true,
        centeredSlides: true,

        /* 🔥 CLAVE */
        slidesPerView: 1.4,     // ❌ NO "auto"
        spaceBetween: 40,

        loop: true,

        autoplay: {
            delay: 3000,
            disableOnInteraction: false,
        },

        speed: 900,

        coverflowEffect: {
            rotate: 0,
            stretch: 0,         // ❌ quitar stretch
            depth: 220,
            modifier: 1.1,
            slideShadows: false,
        },

        navigation: {
            nextEl: ".swiper-button-next",
            prevEl: ".swiper-button-prev",
        },

        /* Responsive limpio */
        breakpoints: {
            768: {
                slidesPerView: 1.8,
            },
            1024: {
                slidesPerView: 2.2,
            },
        },
    });
});




