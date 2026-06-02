"use client";

import React, { useRef, useState } from "react";
import { motion } from "framer-motion";

/**
 * GlowCard Component
 * 
 * A premium card that features a dynamic glowing gradient border
 * that follows the user's mouse cursor.
 */
export default function GlowCard({
  children,
  className = "",
  glowColor = "rgba(255, 255, 255, 0.15)",
}) {
  const cardRef = useRef(null);
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  const [isHovered, setIsHovered] = useState(false);

  const handleMouseMove = (e) => {
    if (!cardRef.current) return;
    const rect = cardRef.current.getBoundingClientRect();
    setMousePosition({
      x: e.clientX - rect.left,
      y: e.clientY - rect.top,
    });
  };

  return (
    <div
      ref={cardRef}
      onMouseMove={handleMouseMove}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      className={`relative rounded-2xl border border-white/5 bg-background overflow-hidden ${className}`}
    >
      {/* Background Glow Effect */}
      <motion.div
        className="pointer-events-none absolute -inset-px rounded-2xl opacity-0 transition-opacity duration-300"
        animate={{ opacity: isHovered ? 1 : 0 }}
        style={{
          background: `radial-gradient(600px circle at ${mousePosition.x}px ${mousePosition.y}px, ${glowColor}, transparent 40%)`,
        }}
      />
      
      {/* Inner Content Wrapper to ensure glow stays behind content */}
      <div className="relative h-full w-full rounded-2xl bg-background/90 p-6 backdrop-blur-sm">
        {children}
      </div>
    </div>
  );
}
