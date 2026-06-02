"use client";

import { useRef } from "react";
import { motion } from "framer-motion";
import { ArrowRight } from "lucide-react";
import useGsapScroll from "../hooks/useGsapScroll";
import { gsap } from "gsap";
import MagneticButton from "./MagneticButton";

export default function ImmersiveHero({ title, subtitle, eyebrow, colors, primary_cta, motion_config }) {
  const containerRef = useRef(null);
  const blob1Ref = useRef(null);
  const blob2Ref = useRef(null);

  const transition = {
    type: "spring",
    stiffness: motion_config?.stiffness || 120,
    damping: motion_config?.damping || 14,
    duration: motion_config?.duration || 1.2,
  };

  // Perform parallax movement on background decorative gradient blobs as user scrolls down
  useGsapScroll(containerRef, {
    trigger: containerRef,
    start: "top top",
    end: "bottom top",
    scrub: 1.2,
    animate: () => {
      const tl = gsap.timeline();
      tl.to(blob1Ref.current, { y: 180, x: -60, scale: 1.15 }, 0)
        .to(blob2Ref.current, { y: -180, x: 60, scale: 0.85 }, 0);
      return tl;
    }
  });

  return (
    <section ref={containerRef} className="relative min-h-screen w-full flex flex-col justify-center items-center px-6 overflow-hidden bg-background">
      {/* Background Decorative Gradient Blobs */}
      <div className="absolute inset-0 z-0 pointer-events-none opacity-20">
        <div 
          ref={blob1Ref}
          className="absolute top-1/4 left-1/4 w-[40vw] h-[40vw] rounded-full bg-accent filter blur-[120px] animate-pulse" 
        />
        <div 
          ref={blob2Ref}
          className="absolute bottom-1/4 right-1/4 w-[30vw] h-[30vw] rounded-full bg-muted filter blur-[100px]" 
        />
      </div>

      {/* Hero content container */}
      <div className="relative z-10 max-w-5xl w-full text-center flex flex-col items-center">
        {eyebrow && (
          <motion.span
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
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
          className="text-5xl md:text-8xl font-header font-bold tracking-tight text-foreground leading-[1.05] mb-6"
        >
          {title}
        </motion.h1>

        {subtitle && (
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ ...transition, delay: 0.4 }}
            className="text-lg md:text-2xl font-body font-light text-foreground/70 max-w-2xl mb-10 leading-relaxed"
          >
            {subtitle}
          </motion.p>
        )}

        {primary_cta && primary_cta.text && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ ...transition, delay: 0.6 }}
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

      {/* Decorative Elegant Grid Border bottom */}
      <div className="absolute bottom-0 left-0 w-full h-[1px] bg-gradient-to-r from-transparent via-borderColor to-transparent" />
    </section>
  );
}
