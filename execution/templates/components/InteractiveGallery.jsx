"use client";

import { useRef } from "react";
import { motion } from "framer-motion";
import useGsapScroll from "../hooks/useGsapScroll";
import { gsap } from "gsap";

export default function InteractiveGallery({ title, subtitle, items, motion_config }) {
  const sectionRef = useRef(null);
  const scrollContainerRef = useRef(null);

  // Setup GSAP horizontal scroll pin animation
  useGsapScroll(sectionRef, {
    trigger: sectionRef,
    start: "top top",
    end: () => `+=${scrollContainerRef.current?.scrollWidth - window.innerWidth + 300}`,
    pin: true,
    scrub: 1.2,
    animate: () => {
      if (!scrollContainerRef.current) return;
      return gsap.to(scrollContainerRef.current, {
        x: () => -(scrollContainerRef.current.scrollWidth - window.innerWidth + 150),
        ease: "none"
      });
    }
  });

  const defaultItems = [
    { title: "Quantum Cipher", description: "Securing modern communication vectors using physical lattice key protocols." },
    { title: "Synthetic Mind", description: "Neural network intelligence structures operating autonomously on local node clusters." },
    { title: "Spatial Web", description: "Immersive three-dimensional semantic applications projecting spatial user interfaces." }
  ];

  const galleryItems = items && items.length > 0 ? items : defaultItems;

  return (
    <section 
      ref={sectionRef} 
      className="relative w-full min-h-screen bg-background overflow-hidden flex items-center border-b border-borderColor"
    >
      {/* Editorial horizontal track */}
      <div 
        ref={scrollContainerRef}
        className="flex items-center gap-12 md:gap-16 px-8 md:px-24 h-full py-12 shrink-0 will-change-transform"
      >
        {/* Editorial Header (Slides first) */}
        <div className="w-[300px] md:w-[450px] flex flex-col justify-center shrink-0">
          <span className="text-xs uppercase tracking-[0.4em] font-medium text-accent mb-6 block">
            GALLERY / WORK
          </span>
          <h2 className="text-4xl md:text-7xl font-header font-black tracking-tight text-foreground uppercase mb-6 leading-none">
            {title}
          </h2>
          {subtitle && (
            <p className="text-base md:text-lg font-body font-light text-foreground/60 leading-relaxed max-w-sm">
              {subtitle}
            </p>
          )}
          
          <div className="mt-8 text-xs text-foreground/30 font-mono tracking-widest uppercase flex items-center gap-2">
            <span>SCROLL DOWN TO PROGRESS</span>
            <span className="animate-pulse">→</span>
          </div>
        </div>

        {/* Gallery items in horizontal track */}
        {galleryItems.map((item, index) => (
          <div
            key={index}
            className="group relative rounded-custom bg-card border border-borderColor hover:border-accent/40 overflow-hidden shadow-2xl transition-all duration-500 w-[280px] md:w-[400px] h-[380px] md:h-[500px] shrink-0 flex flex-col justify-end p-8"
          >
            {/* Visual background decoration */}
            <div className="absolute inset-0 bg-gradient-to-t from-background via-background/30 to-transparent z-10" />
            
            {/* Abstract visual background grid glow */}
            <div className="absolute inset-0 bg-gradient-to-br from-accent/5 via-transparent to-muted/10 group-hover:scale-105 transition-transform duration-700 ease-out z-0" />
            
            {item.image && (
              <div 
                className="absolute inset-0 bg-cover bg-center transition-transform duration-700 group-hover:scale-105 pointer-events-none z-0" 
                style={{ backgroundImage: `url(${item.image})` }} 
              />
            )}

            {/* Glowing top active sign */}
            <div className="absolute top-6 right-6 w-8 h-8 rounded-full border border-borderColor flex justify-center items-center opacity-0 group-hover:opacity-100 transition-opacity duration-500 z-20">
              <div className="w-2 h-2 rounded-full bg-accent animate-ping" />
            </div>

            {/* Item detail texts */}
            <div className="relative z-20">
              <span className="text-[10px] font-mono tracking-widest text-accent uppercase block mb-3">
                PRODUCT {String(index + 1).padStart(2, "0")}
              </span>
              
              <h3 className="text-xl md:text-2xl font-header font-bold text-foreground mb-3 group-hover:text-accent transition-colors duration-300">
                {item.title}
              </h3>
              
              <p className="text-sm font-body font-light text-foreground/60 leading-relaxed translate-y-4 group-hover:translate-y-0 transition-transform duration-500">
                {item.description}
              </p>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
