"use client";

import React, { useRef } from "react";
import useGsapScroll from "../hooks/useGsapScroll";
import { gsap } from "gsap";

/**
 * ScrollPinSection Component
 * 
 * Adapted from standard GSAP ScrollTrigger pin + scrub pattern.
 * Viewport is pinned in place while the user scrolls down, causing cards in the 
 * right panel to stack and reveal sequentially while updating active progress indicators.
 */
export default function ScrollPinSection({ title, subtitle, eyebrow, items = [], colors, motion_config }) {
  const containerRef = useRef(null);
  const cardsRef = useRef([]);

  const defaultItems = [
    {
      step_number: "01",
      title: "Strategic Discovery",
      description: "We deep dive into your brand's core values, target demographics, and market opportunities to define an unshakeable design vision."
    },
    {
      step_number: "02",
      title: "High-Fidelity Prototyping",
      description: "We translate insights into tangible wireframes and premium interactive visual structures that define the digital product flow."
    },
    {
      step_number: "03",
      title: "Motion & Engineering Integration",
      description: "We fuse the visual mockups with high-performance physical scripts, smooth scrolling systems, and production-grade responsive React code."
    }
  ];

  const steps = items && items.length > 0 ? items : defaultItems;

  // Drive sequential card overlays using GSAP ScrollTrigger on container
  useGsapScroll(containerRef, {
    trigger: containerRef,
    start: "top top",
    end: `+=${steps.length * 100}%`, // Scroll duration proportional to step count
    pin: true,
    scrub: 1,
    animate: () => {
      const tl = gsap.timeline();
      const cards = cardsRef.current.filter(Boolean);
      
      // Animate each card into view sequentially
      cards.forEach((card, idx) => {
        if (idx === 0) return; // First card starts visible
        
        tl.fromTo(
          card,
          { 
            yPercent: 100, 
            opacity: 0,
            scale: 0.9
          },
          { 
            yPercent: 0, 
            opacity: 1,
            scale: 1,
            ease: "power2.inOut"
          },
          idx - 0.5 // staggered start times on scroll timeline
        );
      });
      return tl;
    }
  });

  return (
    <div ref={containerRef} className="relative w-full min-h-screen bg-background border-b border-borderColor flex items-center justify-center overflow-hidden">
      {/* Visual background ambient details */}
      <div className="absolute top-1/4 left-1/4 w-[40vw] h-[40vw] rounded-full bg-accent/5 filter blur-[120px] pointer-events-none" />

      <div className="max-w-6xl w-full mx-auto px-6 grid grid-cols-1 md:grid-cols-2 gap-12 md:gap-20 items-center min-h-[80vh]">
        
        {/* Left Column - Typographic Header & Progress Tracker */}
        <div className="flex flex-col justify-center h-full max-w-md relative z-10 py-10">
          {eyebrow && (
            <span className="text-xs uppercase tracking-[0.4em] font-medium text-accent mb-6 block">
              {eyebrow}
            </span>
          )}
          
          <h2 className="text-4xl md:text-6xl font-header font-black tracking-tight text-foreground uppercase mb-6 leading-none">
            {title || "Our Process"}
          </h2>
          
          <p className="text-base md:text-lg font-body font-light text-foreground/70 leading-relaxed mb-10">
            {subtitle || "A disciplined, holistic approach to crafting outstanding, award-winning interactive interfaces."}
          </p>

          {/* Graphical Step Indicators */}
          <div className="flex flex-col gap-4 border-l border-borderColor/40 pl-6">
            {steps.map((step, idx) => (
              <div key={`step-indicator-${idx}`} className="flex items-center gap-3">
                <span className="text-sm font-header font-bold text-accent">
                  {step.step_number || `0${idx + 1}`}
                </span>
                <span className="text-sm font-body text-foreground/80">
                  {step.title}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Right Column - Absolute Card Stacking Deck */}
        <div className="relative w-full h-[350px] md:h-[450px] flex items-center justify-center z-10">
          <div className="relative w-full h-full">
            {steps.map((step, idx) => (
              <div
                key={`card-step-${idx}`}
                ref={(el) => {
                  if (el) cardsRef.current[idx] = el;
                }}
                className="absolute inset-0 w-full h-full bg-card border border-borderColor/80 rounded-custom p-8 md:p-10 flex flex-col justify-between shadow-2xl transition-shadow duration-300 hover:shadow-[0_20px_50px_rgba(0,0,0,0.3)]"
                style={{ 
                  zIndex: idx + 10,
                  transformOrigin: "bottom center"
                }}
              >
                {/* Large step watermark in card background */}
                <span className="absolute top-4 right-6 text-7xl md:text-9xl font-header font-black text-foreground/[0.03] select-none pointer-events-none">
                  {step.step_number || `0${idx + 1}`}
                </span>

                <div className="flex flex-col h-full justify-between">
                  <div className="flex items-center gap-3">
                    <span className="px-3 py-1 text-xs font-header font-bold rounded-full bg-accent/10 text-accent uppercase tracking-wider">
                      Step {step.step_number || `0${idx + 1}`}
                    </span>
                  </div>

                  <div className="mt-8">
                    <h3 className="text-2xl md:text-3xl font-header font-extrabold text-foreground mb-4">
                      {step.title}
                    </h3>
                    <p className="text-sm md:text-base font-body text-foreground/75 leading-relaxed font-light">
                      {step.description}
                    </p>
                  </div>

                  <div className="mt-auto pt-6 border-t border-borderColor/20 flex items-center justify-between text-xs text-foreground/40 font-mono">
                    <span>STATUS: ACTIVE PROTOCOL</span>
                    <span>ANDIP PROCESS GRID</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

      </div>
    </div>
  );
}
