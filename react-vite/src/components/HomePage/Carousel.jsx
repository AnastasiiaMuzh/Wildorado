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
    const [currentImageIndex, setCurrentImageIndex] = useState(0);
    const [index, setIndex] = useState(0);
    

    useEffect(() => {
        const interval = setInterval(() => {
        setIndex((prevIndex) => (prevIndex + 1) % images.length);
        }, 4000);
        return () => clearInterval(interval);
    }, []);

    
    return (
        <div className="carousel-container">
        <AnimatePresence mode="wait">
            <motion.img
            key={images[index].src}
            src={images[index].src}
            alt=""
            className="carousel-image" 
            initial={{ opacity: 0, scale: 1.1 }} // Начальный масштаб чуть больше
            animate={{ opacity: 1, scale: 1 }} // Плавное уменьшение
            exit={{ opacity: 0, scale: 1.1 }} // При уходе снова увеличивается
            transition={{ duration: 4, ease: "easeInOut" }} // Увеличена длительность
            />
        </AnimatePresence>
        <div className="carousel-text">{images[index].text}</div>
        </div>
    );
    };

export default Carousel;
