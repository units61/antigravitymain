"use client";

import { useRef } from "react";
import { motion } from "framer-motion";
import useGsapScroll from "../hooks/useGsapScroll";
import { gsap } from "gsap";

export default function FeatureGrid({ title, subtitle, items, motion_config }) {
  const containerRef = useRef(null);
  const cardsRef = useRef([]);

  // High fidelity GSAP stagger reveal when the feature grid enters viewport
  useGsapScroll(containerRef, {
    trigger: containerRef,
    start: "top 85%",
    scrub: false,
    once: true,
    animate: () => {
      const cards = cardsRef.current.filter(Boolean);
      return gsap.fromTo(
        cards,
        { opacity: 0, y: 60 },
        {
          opacity: 1,
          y: 0,
          duration: 1.0,
          stagger: 0.12,
          ease: "power2.out"
        }
      );
    }
  });

  return (
    <section id="benefits" ref={containerRef} className="relative py-24 md:py-32 px-6 bg-background">
      <div className="max-w-7xl mx-auto">
        {/* Header Block */}
        <div className="text-center max-w-3xl mx-auto mb-16 md:mb-24">
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-100px" }}
            transition={{ duration: 0.6 }}
            className="text-3xl md:text-5xl font-header font-bold text-foreground mb-6"
          >
            {title}
          </motion.h2>
          
          {subtitle && (
            <motion.p
              initial={{ opacity: 0, y: 15 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-100px" }}
              transition={{ duration: 0.6, delay: 0.1 }}
              className="text-base md:text-lg font-body font-light text-foreground/60 leading-relaxed"
            >
              {subtitle}
            </motion.p>
          )}
        </div>

        {/* Feature Grid */}
        {items && items.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 md:gap-8">
            {items.map((item, index) => (
              <div
                key={index}
                ref={(el) => {
                  if (el) cardsRef.current[index] = el;
                }}
                className="group relative p-8 md:p-10 rounded-custom bg-card border border-borderColor hover:border-accent/40 shadow-lg hover:shadow-[0_15px_40px_rgba(0,0,0,0.3)] transition-all duration-500 overflow-hidden opacity-0"
              >
                {/* Visual Glow Layer */}
                <div className="absolute inset-0 bg-gradient-to-b from-transparent to-accent/[0.02] opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none" />
                
                {/* Floating index */}
                <span className="text-4xl md:text-5xl font-header font-extrabold text-accent/10 group-hover:text-accent/20 transition-colors duration-500 block mb-6 select-none">
                  {String(index + 1).padStart(2, "0")}
                </span>

                <h3 className="text-xl font-header font-bold text-foreground mb-4 group-hover:text-accent transition-colors duration-300">
                  {item.title}
                </h3>
                
                <p className="text-sm md:text-base font-body font-light text-foreground/60 leading-relaxed">
                  {item.description}
                </p>
              </div>
            ))}
          </div>
        )}
      </div>
    </section>
  );
}
