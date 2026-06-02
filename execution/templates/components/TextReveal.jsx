"use client";

import React, { useRef } from "react";
import { motion, useScroll, useTransform } from "framer-motion";

/**
 * TextReveal Component
 * 
 * Splits a paragraph of text into individual words and reveals them
 * sequentially as the user scrolls, creating a highly engaging typographic effect.
 */
export default function TextReveal({ 
  text,
  title, 
  className = "" 
}) {
  const containerRef = useRef(null);
  
  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ["start 80%", "end 50%"]
  });

  const content = text || title || "";
  const words = content.split(" ");

  return (
    <div ref={containerRef} className={`relative max-w-5xl mx-auto ${className}`}>
      <p className="flex flex-wrap gap-x-[0.5em] gap-y-[0.2em] text-3xl md:text-5xl lg:text-7xl font-header font-bold text-foreground/20 leading-tight">
        {words.map((word, i) => {
          // Calculate opacity range for each word based on its index
          const start = i / words.length;
          const end = start + (1 / words.length);
          
          return (
            <Word key={i} progress={scrollYProgress} range={[start, end]}>
              {word}
            </Word>
          );
        })}
      </p>
    </div>
  );
}

const Word = ({ children, progress, range }) => {
  const opacity = useTransform(progress, range, [0.1, 1]);
  
  return (
    <span className="relative">
      <span className="absolute opacity-10">{children}</span>
      <motion.span style={{ opacity }} className="text-foreground">
        {children}
      </motion.span>
    </span>
  );
};
