"use client";

import React from "react";
import { motion } from "framer-motion";
import * as Icons from "lucide-react";

/**
 * BentoGrid Component
 * 
 * Adapted from Aceternity UI Bento Grid design pattern.
 * Creates an asymmetric grid card layout using responsive CSS grid spans.
 */
export default function BentoGrid({ title, subtitle, items = [], colors, motion_config }) {
  const defaultItems = [
    {
      title: "Decentralized Speed",
      description: "Our distributed content delivery network ensures sub-millisecond response times around the globe.",
      icon: "Zap",
      span: "md:col-span-2 md:row-span-1",
      image: "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=800&auto=format&fit=crop"
    },
    {
      title: "Total Sovereignty",
      description: "Own your data entirely. Complete cryptographic proof structures on-chain.",
      icon: "Shield",
      span: "md:col-span-1 md:row-span-1",
      image: "https://images.unsplash.com/photo-1634017839464-5c339ebe3cb4?q=80&w=800&auto=format&fit=crop"
    },
    {
      title: "Interactive Analytics",
      description: "Realtime user behaviour logs streamed directly through our web sockets visualization dashboard.",
      icon: "BarChart3",
      span: "md:col-span-1 md:row-span-2",
      image: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=800&auto=format&fit=crop"
    },
    {
      title: "Quantum Protocols",
      description: "Pre-quantum secure tunnel layers protecting key exchange APIs.",
      icon: "KeyRound",
      span: "md:col-span-2 md:row-span-1",
      image: "https://images.unsplash.com/photo-1639762681485-074b7f938ba0?q=80&w=800&auto=format&fit=crop"
    }
  ];

  const gridItems = items && items.length > 0 ? items : defaultItems;

  const transition = {
    type: "spring",
    stiffness: motion_config?.stiffness || 150,
    damping: motion_config?.damping || 16,
  };

  return (
    <section className="relative py-24 px-6 md:px-12 w-full bg-background border-b border-borderColor overflow-hidden">
      {/* Background radial highlight */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[60vw] h-[60vw] rounded-full bg-accent/5 filter blur-[140px] pointer-events-none" />

      <div className="max-w-6xl mx-auto relative z-10">
        {(title || subtitle) && (
          <div className="mb-16 text-center max-w-2xl mx-auto">
            {title && (
              <h2 className="text-4xl md:text-6xl font-header font-extrabold tracking-tight text-foreground mb-4">
                {title}
              </h2>
            )}
            {subtitle && (
              <p className="text-lg font-body font-light text-foreground/75 leading-relaxed">
                {subtitle}
              </p>
            )}
          </div>
        )}

        {/* CSS Bento Grid layout */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 auto-rows-[250px] md:auto-rows-[280px]">
          {gridItems.map((item, index) => {
            const IconComponent = Icons[item.icon] || Icons.HelpCircle;
            const spanClass = item.span || "md:col-span-1 md:row-span-1";

            return (
              <motion.div
                key={`bento-${index}`}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: "-100px" }}
                transition={{ ...transition, delay: index * 0.1 }}
                whileHover={{ y: -6 }}
                className={`group relative rounded-custom border border-borderColor overflow-hidden flex flex-col justify-end p-6 bg-card transition-all duration-300 hover:shadow-[0_12px_40px_rgba(0,0,0,0.4)] ${spanClass}`}
              >
                {/* Background image preview if exists */}
                {item.image && (
                  <>
                    <div 
                      className="absolute inset-0 bg-cover bg-center z-0 transition-transform duration-700 group-hover:scale-105"
                      style={{ backgroundImage: `url(${item.image})` }}
                    />
                    {/* Shadow overlay to read text clearly */}
                    <div className="absolute inset-0 bg-gradient-to-t from-background via-background/70 to-background/20 z-10 transition-opacity duration-300 group-hover:via-background/80" />
                  </>
                )}

                {/* Subtle Border Glow hover effect */}
                <div className="absolute inset-0 z-20 pointer-events-none opacity-0 group-hover:opacity-100 transition-opacity duration-500 rounded-custom border border-accent/40 shadow-[inset_0_0_15px_rgba(var(--color-accent-rgb),0.15)]" />

                {/* Icon & Details */}
                <div className="relative z-30 flex flex-col h-full justify-between items-start">
                  <div className="p-3 rounded-xl bg-background/50 backdrop-blur-md border border-borderColor text-accent group-hover:scale-110 transition-transform duration-300">
                    <IconComponent className="w-6 h-6" />
                  </div>
                  
                  <div className="mt-4">
                    <h3 className="text-xl font-header font-bold text-foreground mb-2 flex items-center gap-2">
                      {item.title}
                    </h3>
                    <p className="text-sm font-body text-foreground/70 leading-relaxed font-light group-hover:text-foreground/90 transition-colors duration-300">
                      {item.description || item.subtitle}
                    </p>
                  </div>
                </div>
              </motion.div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
