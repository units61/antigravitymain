"use client";

import React, { useRef } from "react";
import useGsapScroll from "../hooks/useGsapScroll";
import { gsap } from "gsap";

/**
 * ParallaxGallery Component
 * 
 * Adapted from Aceternity UI Hero Parallax design.
 * Uses GSAP ScrollTrigger via useGsapScroll hook to translate three rows of cards 
 * horizontally in opposite directions, linked seamlessly to scroll progress.
 */
export default function ParallaxGallery({ title, subtitle, items = [], colors, motion_config }) {
  const containerRef = useRef(null);
  const row1Ref = useRef(null);
  const row2Ref = useRef(null);
  const row3Ref = useRef(null);

  const defaultItems = [
    { title: "Metaverse Spatial", image: "https://images.unsplash.com/photo-1614741118887-7a4ee193a5fa?q=80&w=600&auto=format&fit=crop" },
    { title: "Cyber Architecture", image: "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?q=80&w=600&auto=format&fit=crop" },
    { title: "Quantum Computing", image: "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?q=80&w=600&auto=format&fit=crop" },
    { title: "Neo Futurist", image: "https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?q=80&w=600&auto=format&fit=crop" },
    { title: "Synapse Synthesis", image: "https://images.unsplash.com/photo-1507679799987-c73779587ccf?q=80&w=600&auto=format&fit=crop" },
    { title: "Aesthetic Core", image: "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=600&auto=format&fit=crop" },
    { title: "Tactile Glass", image: "https://images.unsplash.com/photo-1634017839464-5c339ebe3cb4?q=80&w=600&auto=format&fit=crop" },
    { title: "Dark Matter", image: "https://images.unsplash.com/photo-1541701494587-cb58502866ab?q=80&w=600&auto=format&fit=crop" },
    { title: "Neural Networks", image: "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?q=80&w=600&auto=format&fit=crop" },
    { title: "Deep Oceans", image: "https://images.unsplash.com/photo-1518156677180-95a2893f3e9f?q=80&w=600&auto=format&fit=crop" },
    { title: "Cosmic Glow", image: "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?q=80&w=600&auto=format&fit=crop" },
    { title: "Atmosphere Alpha", image: "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=600&auto=format&fit=crop" }
  ];

  const galleryItems = items && items.length >= 6 ? items : defaultItems;

  // Split galleryItems into 3 equal rows
  const rowCount = Math.ceil(galleryItems.length / 3);
  const row1 = galleryItems.slice(0, rowCount);
  const row2 = galleryItems.slice(rowCount, rowCount * 2);
  const row3 = galleryItems.slice(rowCount * 2);

  // Initialize GSAP scroll animation on rows
  useGsapScroll(containerRef, {
    trigger: containerRef,
    start: "top bottom",
    end: "bottom top",
    scrub: 1.5,
    animate: () => {
      const tl = gsap.timeline();
      tl.to(row1Ref.current, { x: "-20%" }, 0)
        .to(row2Ref.current, { x: "20%" }, 0)
        .to(row3Ref.current, { x: "-20%" }, 0);
      return tl;
    }
  });

  return (
    <section 
      ref={containerRef}
      className="relative w-full bg-background border-b border-borderColor py-24 md:py-32 overflow-hidden flex flex-col items-center"
    >
      {/* Editorial Header */}
      <div className="max-w-5xl w-full px-6 mb-16 text-center z-10">
        {title && (
          <h2 className="text-4xl md:text-7xl font-header font-black tracking-tight text-foreground uppercase mb-6 leading-none">
            {title}
          </h2>
        )}
        {subtitle && (
          <p className="text-lg md:text-2xl font-body font-light text-foreground/60 max-w-2xl mx-auto leading-relaxed">
            {subtitle}
          </p>
        )}
      </div>

      {/* Row Containers with opposite translation directions */}
      <div className="w-full flex flex-col gap-6 md:gap-10 pointer-events-none select-none relative z-10">
        {/* Row 1 - Moves Left */}
        <div className="w-full overflow-hidden flex">
          <div 
            ref={row1Ref} 
            className="flex gap-6 md:gap-10 px-10 will-change-transform shrink-0"
            style={{ transform: "translateX(0%)" }}
          >
            {row1.map((item, idx) => (
              <div 
                key={`row1-${idx}`} 
                className="w-[280px] h-[180px] md:w-[400px] md:h-[260px] relative rounded-custom overflow-hidden border border-borderColor/40 shadow-2xl"
              >
                <div 
                  className="absolute inset-0 bg-cover bg-center" 
                  style={{ backgroundImage: `url(${item.image || item.image_prompt})` }} 
                />
                <div className="absolute inset-0 bg-gradient-to-t from-background/90 via-transparent to-transparent z-10" />
                <span className="absolute bottom-4 left-4 z-20 font-header text-sm md:text-lg font-bold text-foreground">
                  {item.title}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Row 2 - Moves Right */}
        <div className="w-full overflow-hidden flex justify-end">
          <div 
            ref={row2Ref} 
            className="flex gap-6 md:gap-10 px-10 will-change-transform shrink-0"
            style={{ transform: "translateX(-20%)" }}
          >
            {row2.map((item, idx) => (
              <div 
                key={`row2-${idx}`} 
                className="w-[280px] h-[180px] md:w-[400px] md:h-[260px] relative rounded-custom overflow-hidden border border-borderColor/40 shadow-2xl"
              >
                <div 
                  className="absolute inset-0 bg-cover bg-center" 
                  style={{ backgroundImage: `url(${item.image || item.image_prompt})` }} 
                />
                <div className="absolute inset-0 bg-gradient-to-t from-background/90 via-transparent to-transparent z-10" />
                <span className="absolute bottom-4 left-4 z-20 font-header text-sm md:text-lg font-bold text-foreground">
                  {item.title}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Row 3 - Moves Left */}
        <div className="w-full overflow-hidden flex">
          <div 
            ref={row3Ref} 
            className="flex gap-6 md:gap-10 px-10 will-change-transform shrink-0"
            style={{ transform: "translateX(0%)" }}
          >
            {row3.map((item, idx) => (
              <div 
                key={`row3-${idx}`} 
                className="w-[280px] h-[180px] md:w-[400px] md:h-[260px] relative rounded-custom overflow-hidden border border-borderColor/40 shadow-2xl"
              >
                <div 
                  className="absolute inset-0 bg-cover bg-center" 
                  style={{ backgroundImage: `url(${item.image || item.image_prompt})` }} 
                />
                <div className="absolute inset-0 bg-gradient-to-t from-background/90 via-transparent to-transparent z-10" />
                <span className="absolute bottom-4 left-4 z-20 font-header text-sm md:text-lg font-bold text-foreground">
                  {item.title}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
