"use client";

import { useRef } from "react";
import { motion } from "framer-motion";
import { ArrowRight } from "lucide-react";
import useGsapScroll from "../hooks/useGsapScroll";
import { gsap } from "gsap";
import MagneticButton from "./MagneticButton";

export default function SplitSectionHero({ title, subtitle, eyebrow, colors, primary_cta, motion_config }) {
  const containerRef = useRef(null);
  const leftColRef = useRef(null);
  const rightColRef = useRef(null);

  const transition = {
    type: "spring",
    stiffness: motion_config?.stiffness || 120,
    damping: motion_config?.damping || 14,
    duration: motion_config?.duration || 1.2,
  };

  // Perform differential parallax on split panels as user scrolls
  useGsapScroll(containerRef, {
    trigger: containerRef,
    start: "top top",
    end: "bottom top",
    scrub: 1.2,
    animate: () => {
      const tl = gsap.timeline();
      // Slide right card upwards faster, and pull left column slightly downwards for depth
      tl.to(rightColRef.current, { y: -100, scale: 1.05, ease: "none" }, 0)
        .to(leftColRef.current, { y: 50, ease: "none" }, 0);
      return tl;
    }
  });

  return (
    <section ref={containerRef} className="relative min-h-screen w-full flex flex-col md:flex-row px-6 md:px-12 items-stretch overflow-hidden bg-background">
      {/* Left Text Column */}
      <div ref={leftColRef} className="flex-1 flex flex-col justify-center py-20 pr-0 md:pr-12 z-10 will-change-transform">
        {eyebrow && (
          <motion.span
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ ...transition, delay: 0.1 }}
            className="text-xs uppercase tracking-[0.3em] font-medium text-accent mb-4 block"
          >
            {eyebrow}
          </motion.span>
        )}

        <motion.h1
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ ...transition, delay: 0.2 }}
          className="text-4xl md:text-6xl lg:text-7xl font-header font-bold tracking-tight text-foreground leading-[1.1] mb-6"
        >
          {title}
        </motion.h1>

        {subtitle && (
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ ...transition, delay: 0.4 }}
            className="text-base md:text-lg lg:text-xl font-body font-light text-foreground/70 max-w-lg mb-8 leading-relaxed"
          >
            {subtitle}
          </motion.p>
        )}

        {primary_cta && primary_cta.text && (
          <motion.div
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ ...transition, delay: 0.5 }}
          >
            <MagneticButton
              onClick={() => {
                const target = document.getElementById("benefits") || 
                               document.getElementById("gallery") || 
                               document.getElementById("bento-showcase") || 
                               document.getElementById("marquee");
                if (target) target.scrollIntoView({ behavior: "smooth" });
              }}
              variant="accent"
              className="group flex items-center gap-3"
            >
              <span>{primary_cta.text}</span>
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform duration-300 pointer-events-none" />
            </MagneticButton>
          </motion.div>
        )}
      </div>

      {/* Right Visual/Splitting Column */}
      <div className="flex-1 min-h-[40vh] md:min-h-0 relative flex justify-center items-center overflow-hidden">
        {/* Dynamic artistic visual frame */}
        <motion.div
          ref={rightColRef}
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ ...transition, delay: 0.3 }}
          className="absolute inset-4 md:inset-8 rounded-custom bg-card border border-borderColor shadow-2xl overflow-hidden flex justify-center items-center will-change-transform"
        >
          <div className="absolute inset-0 bg-gradient-to-tr from-accent/10 via-muted/30 to-background/50" />
          
          {/* Subtle Abstract Geometry representing Luxury/Rebel split */}
          <div className="relative w-48 h-48 md:w-64 md:h-64 border-[0.5px] border-borderColor rounded-full flex justify-center items-center animate-spin [animation-duration:30s]">
            <div className="w-32 h-32 border-[0.5px] border-borderColor rounded-full border-dashed" />
            <div className="absolute w-2 h-2 rounded-full bg-accent -top-1" />
          </div>

          <div className="absolute font-header text-9xl font-extrabold opacity-[0.03] select-none uppercase tracking-widest text-foreground">
            {title ? title.substring(0, 3) : "NDP"}
          </div>
        </motion.div>
      </div>
    </section>
  );
}
