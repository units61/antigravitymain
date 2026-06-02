"use client";

import React from "react";

/**
 * Marquee Component
 * 
 * Adapted from Magic UI Marquee & Aceternity Infinite Moving Cards.
 * Implements a high-performance horizontal infinite text/logo ticker using pure CSS.
 */
export default function Marquee({ title, subtitle, items = [], colors, motion_config }) {
  const defaultItems = [
    "AESTHETIC EXCELLENCE",
    "MOTION GRAPHICS",
    "USER EXPERIENCE",
    "GSAP INTERACTIONS",
    "NEXT GENERATION WEB",
    "MINIMALIST LUXURY"
  ];
  
  const displayItems = items && items.length > 0 ? items : defaultItems;
  const speed = motion_config?.duration || 30; // seconds for one loop

  return (
    <section className="relative py-12 md:py-20 w-full overflow-hidden bg-background border-b border-borderColor flex flex-col justify-center">
      {/* Dynamic Style Block for unique speed parameters */}
      <style dangerouslySetInnerHTML={{ __html: `
        @keyframes marquee-scroll {
          0% { transform: translateX(0%); }
          100% { transform: translateX(-100%); }
        }
        .animate-marquee-track {
          display: flex;
          flex-shrink: 0;
          gap: 3rem;
          white-space: nowrap;
          animation: marquee-scroll ${speed}s linear infinite;
        }
        .animate-marquee-track:hover {
          animation-play-state: paused;
        }
      `}} />

      {(title || subtitle) && (
        <div className="max-w-6xl mx-auto px-6 mb-8 text-center">
          {title && (
            <h2 className="text-2xl md:text-4xl font-header font-bold text-foreground mb-3">
              {title}
            </h2>
          )}
          {subtitle && (
            <p className="text-sm md:text-base font-body text-foreground/60 max-w-xl mx-auto">
              {subtitle}
            </p>
          )}
        </div>
      )}

      {/* Marquee Wrapper */}
      <div className="relative flex w-full overflow-x-hidden py-4">
        {/* Soft Vignettes */}
        <div className="absolute left-0 top-0 bottom-0 w-20 md:w-40 bg-gradient-to-r from-background to-transparent z-10 pointer-events-none" />
        <div className="absolute right-0 top-0 bottom-0 w-20 md:w-40 bg-gradient-to-l from-background to-transparent z-10 pointer-events-none" />

        {/* Track 1 */}
        <div className="animate-marquee-track">
          {displayItems.map((item, idx) => {
            const text = typeof item === "string" ? item : item.title || item.label || "";
            return (
              <span
                key={`marquee-1-${idx}`}
                className="text-4xl md:text-7xl font-header font-extrabold uppercase tracking-widest text-transparent stroke-text"
                style={{
                  WebkitTextStroke: "1px rgba(var(--color-foreground-rgb, 255, 255, 255), 0.25)",
                  color: "transparent",
                  fontFamily: "var(--font-header)",
                  transition: "color 0.3s ease, -webkit-text-stroke 0.3s ease",
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.color = "var(--color-accent)";
                  e.currentTarget.style.WebkitTextStroke = "1px var(--color-accent)";
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.color = "transparent";
                  e.currentTarget.style.WebkitTextStroke = "1px rgba(var(--color-foreground-rgb, 255, 255, 255), 0.25)";
                }}
              >
                {text}
              </span>
            );
          })}
        </div>

        {/* Track 2 (Clone for infinite seamless scroll) */}
        <div className="animate-marquee-track" aria-hidden="true">
          {displayItems.map((item, idx) => {
            const text = typeof item === "string" ? item : item.title || item.label || "";
            return (
              <span
                key={`marquee-2-${idx}`}
                className="text-4xl md:text-7xl font-header font-extrabold uppercase tracking-widest text-transparent stroke-text"
                style={{
                  WebkitTextStroke: "1px rgba(var(--color-foreground-rgb, 255, 255, 255), 0.25)",
                  color: "transparent",
                  fontFamily: "var(--font-header)",
                  transition: "color 0.3s ease, -webkit-text-stroke 0.3s ease",
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.color = "var(--color-accent)";
                  e.currentTarget.style.WebkitTextStroke = "1px var(--color-accent)";
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.color = "transparent";
                  e.currentTarget.style.WebkitTextStroke = "1px rgba(var(--color-foreground-rgb, 255, 255, 255), 255)";
                }}
              >
                {text}
              </span>
            );
          })}
        </div>
      </div>
    </section>
  );
}
