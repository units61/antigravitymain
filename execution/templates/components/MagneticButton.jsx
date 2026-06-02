"use client";

import React, { useRef, useState } from "react";
import { motion, useMotionValue, useSpring } from "framer-motion";

/**
 * MagneticButton Component
 * 
 * Adapted from React Bits Magnet component physics.
 * Implements a premium fluid physical button that tracks mouse position when hovered,
 * pulling itself toward the mouse pointer and snapping back to center with spring simulation.
 */
export default function MagneticButton({ children, text, onClick, variant = "accent", className = "" }) {
  const ref = useRef(null);
  const [isHovered, setIsHovered] = useState(false);

  // Framer motion physical values
  const x = useMotionValue(0);
  const y = useMotionValue(0);

  // Soft elastic spring physics simulation
  const springConfig = { damping: 12, stiffness: 140, mass: 0.15 };
  const springX = useSpring(x, springConfig);
  const springY = useSpring(y, springConfig);

  const handleMouseMove = (e) => {
    if (!ref.current) return;
    const { clientX, clientY } = e;
    const { left, top, width, height } = ref.current.getBoundingClientRect();
    
    // Find center point of button
    const centerX = left + width / 2;
    const centerY = top + height / 2;

    // Offset of mouse from button center
    const distanceX = clientX - centerX;
    const distanceY = clientY - centerY;

    // Pull intensity factor (0.35 = button follows mouse 35% of the way)
    const pullForce = 0.35; 
    x.set(distanceX * pullForce);
    y.set(distanceY * pullForce);
  };

  const handleMouseLeave = () => {
    setIsHovered(false);
    // Snap back to original center position
    x.set(0);
    y.set(0);
  };

  const handleMouseEnter = () => {
    setIsHovered(true);
  };

  // Modern minimal palette mappings
  const variantStyles = {
    accent: "bg-accent text-background hover:shadow-[0_0_30px_rgba(var(--color-accent-rgb),0.35)] border border-accent",
    outline: "bg-transparent text-foreground border border-borderColor hover:bg-foreground hover:text-background hover:border-foreground",
    ghost: "bg-transparent text-foreground hover:bg-foreground/5"
  };

  return (
    <motion.button
      ref={ref}
      onMouseEnter={handleMouseEnter}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      style={{ x: springX, y: springY }}
      onClick={onClick}
      className={`relative px-8 py-4 rounded-custom font-body font-semibold tracking-wide transition-all duration-300 outline-none select-none focus-visible:ring-2 focus-visible:ring-accent ${variantStyles[variant] || variantStyles.accent} ${className}`}
    >
      {/* Visual background ripple focus layer */}
      <span 
        className="absolute inset-0 rounded-custom bg-foreground/5 opacity-0 active:opacity-100 transition-opacity duration-150 pointer-events-none" 
      />

      <span 
        className="relative z-10 block pointer-events-none transition-transform duration-200" 
        style={{ transform: isHovered ? "scale(1.02)" : "scale(1)" }}
      >
        {text || children}
      </span>
    </motion.button>
  );
}
