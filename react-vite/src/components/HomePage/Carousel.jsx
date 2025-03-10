import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import "./Carousel.css"; 

const images = [
    { src: "/images/summer2.png", text: "Explore the best outdoor adventures!" },
    { src: "/images/fall.png", text: "Find your next thrilling location!" },
    { src: "/images/winter5.png", text: "Discover hidden gems in nature!" },
    { src: "/images/spring.png", text: "Explore with WILDORADO!" }
]

const Carousel = () => {
    const [index, setIndex] = useState(0); // State to track the current image index
    const [showText, setShowText] = useState(false); // State to control text visibility
    

    useEffect(() => {
        // Interval to change the image every 6 seconds
        const interval = setInterval(() => {
            // setShowText(false); 
            setIndex((prevIndex) => (prevIndex + 1) % images.length); // carousel
        }, 8000);
        return () => clearInterval(interval); // Cleanup interval on unmount
    }, []);

    useEffect(() => {
        // Show text after 1 second
        const showTextTimer = setTimeout(() => {
            setShowText(true);
        }, 2000);
        
        // Hide text after 5 seconds (1s delay + 4s display)
        const hideTextTimer = setTimeout(() => {
            setShowText(false);
        }, 7000); 
        
        return () => {
            clearTimeout(showTextTimer); // Cleanup timers
            clearTimeout(hideTextTimer);
        };
    }, [index]); // Runs when the image index changes

    return (
        <div className="carousel-container">
            <AnimatePresence mode="sync">
                {/* Animated image transition */}
                <motion.img
                    key={images[index].src}
                    src={images[index].src}
                    alt=""
                    className="carousel-image" 
                    initial={{ opacity: 0, scale: 1.1 }} //когда картинка только появляется, она невидимая и чуть-чуть увеличена.
                    animate={{ opacity: 1, scale: 1 }} //затем она становится видимой и принимает нормальный размер.
                    exit={{ opacity: 0, scale: 1.1 }} //когда настаёт время исчезнуть, она снова становится невидимой и увеличивается.
                    transition={{ duration: 8, ease: "easeInOut" }} //все эти изменения происходят плавно в течение 6 секунд.
                />
            </AnimatePresence>
            {/* Animated text appearing after 1 second and disappearing after 5 seconds */}
            <AnimatePresence>
                {showText && (
                    <motion.div
                        className={`carousel-text ${index === images.length - 1 ? "center-text" : ""}`}
                        initial={{ opacity: 0, y: 20 }}   // Начинаем с 0 прозрачности и немного ниже
                        animate={{ opacity: 1, y: 0 }}   // Делаем текст полностью видимым и ставим на место
                        exit={{ opacity: 0, y: -20 }}   // Исчезает, уходя вверх
                        transition={{ duration: 0.5 }} // Вся анимация длится 0.5 секунды
                    >
                        {images[index].text}
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
};

export default Carousel;