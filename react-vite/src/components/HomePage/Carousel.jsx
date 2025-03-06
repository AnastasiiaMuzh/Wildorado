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
            setShowText(false); // Hide text before switching to the next image
            setIndex((prevIndex) => (prevIndex + 1) % images.length); // carousel
        }, 6000);
        return () => clearInterval(interval); // Cleanup interval on unmount
    }, []);

    useEffect(() => {
        // Show text after 1 second
        const showTextTimer = setTimeout(() => {
            setShowText(true);
        }, 1000);
        
        // Hide text after 5 seconds (1s delay + 4s display)
        const hideTextTimer = setTimeout(() => {
            setShowText(false);
        }, 5000); 
        
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
                    initial={{ opacity: 0, scale: 1.1 }} 
                    animate={{ opacity: 1, scale: 1 }} 
                    exit={{ opacity: 0, scale: 1.1 }} 
                    transition={{ duration: 4, ease: "easeInOut" }} 
                />
            </AnimatePresence>
            {/* Animated text appearing after 1 second and disappearing after 5 seconds */}
            <AnimatePresence>
                {showText && (
                    <motion.div
                        className={`carousel-text ${index === images.length - 1 ? "center-text" : ""}`}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -20 }}
                        transition={{ duration: 0.5 }}
                    >
                        {images[index].text}
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
};

export default Carousel;