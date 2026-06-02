"use client";

import React, { useEffect, useRef } from "react";
import { motion, useMotionValue, useSpring, useInView } from "framer-motion";

/**
 * NumberTicker Sub-component
 * 
 * Adapted from Magic UI Number Ticker interpolator.
 * Animates integer counting using spring physics directly on DOM textContent.
 */
function NumberTicker({ value, delay = 0 }) {
  const ref = useRef(null);
  const motionValue = useMotionValue(0);
  
  // Spring configuration for buttery smooth counting
  const springValue = useSpring(motionValue, {
    damping: 50,
    stiffness: 90,
  });
  
  const isInView = useInView(ref, { once: true, margin: "-100px" });

  useEffect(() => {
    if (isInView) {
      const timer = setTimeout(() => {
        motionValue.set(value);
      }, delay * 1000);
      return () => clearTimeout(timer);
    }
  }, [motionValue, isInView, value, delay]);

  useEffect(() => {
    return springValue.on("change", (latest) => {
      if (ref.current) {
        ref.current.textContent = Intl.NumberFormat("en-US").format(
          Math.round(latest)
        );
      }
    });
  }, [springValue]);

  return <span ref={ref} className="tabular-nums font-extrabold" />;
}

/**
 * StatsCounter Component
 * 
 * Lays out numerical success metrics. Animates count up on scroll view triggers.
 */
export default function StatsCounter({ title, subtitle, items = [], colors, motion_config }) {
  const defaultItems = [
    { value: 99.9, label: "Platform Uptime", suffix: "%", prefix: "" },
    { value: 140, label: "Global Nodes", suffix: "K+", prefix: "" },
    { value: 15, label: "Response Latency", suffix: "ms", prefix: "<" },
    { value: 450, label: "Enterprise Projects", suffix: "+", prefix: "" }
  ];

  const statItems = items && items.length > 0 ? items : defaultItems;

  return (
    <section className="relative py-24 px-6 md:px-12 w-full bg-background border-b border-borderColor overflow-hidden">
      {/* Decorative lines */}
      <div className="absolute inset-0 z-0 pointer-events-none opacity-5">
        <div className="absolute left-1/4 top-0 bottom-0 w-[1px] bg-foreground" />
        <div className="absolute right-1/4 top-0 bottom-0 w-[1px] bg-foreground" />
      </div>

      <div className="max-w-6xl mx-auto relative z-10">
        {(title || subtitle) && (
          <div className="mb-16 text-center max-w-2xl mx-auto">
            {title && (
              <h2 className="text-3xl md:text-5xl font-header font-extrabold tracking-tight text-foreground mb-4">
                {title}
              </h2>
            )}
            {subtitle && (
              <p className="text-base md:text-lg font-body font-light text-foreground/75 leading-relaxed">
                {subtitle}
              </p>
            )}
          </div>
        )}

        <div className="grid grid-cols-2 md:grid-cols-4 gap-8 md:gap-12">
          {statItems.map((item, index) => {
            // Treat value as a number. Extract decimals if float.
            const rawValue = typeof item.value === "string" ? parseFloat(item.value) : item.value;
            const numericValue = isNaN(rawValue) ? 100 : rawValue;

            return (
              <motion.div
                key={`stat-${index}`}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: "-80px" }}
                transition={{ duration: 0.8, delay: index * 0.1 }}
                className="flex flex-col items-center justify-center p-6 bg-card border border-borderColor rounded-custom hover:border-accent/40 shadow-lg hover:shadow-xl transition-all duration-300"
              >
                {/* Metric Value Banner */}
                <div className="text-3xl md:text-6xl font-header font-black text-foreground mb-2 flex items-baseline tracking-tighter">
                  {item.prefix && (
                    <span className="text-2xl md:text-4xl text-accent font-light mr-1">
                      {item.prefix}
                    </span>
                  )}
                  
                  <NumberTicker value={numericValue} delay={index * 0.1} />
                  
                  {item.suffix && (
                    <span className="text-2xl md:text-4xl text-accent font-light ml-1">
                      {item.suffix}
                    </span>
                  )}
                </div>

                {/* Metric Title Label */}
                <p className="text-xs md:text-sm font-body text-foreground/60 uppercase tracking-widest text-center mt-2 font-medium">
                  {item.label || item.title}
                </p>
              </motion.div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
