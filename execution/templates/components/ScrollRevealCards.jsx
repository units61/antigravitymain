"use client";

import { motion } from "framer-motion";
import { Check } from "lucide-react";

export default function ScrollRevealCards({ title, subtitle, eyebrow, items, motion_config }) {
  const transition = {
    type: "spring",
    stiffness: motion_config?.stiffness || 150,
    damping: motion_config?.damping || 15,
  };

  return (
    <section id="pricing" className="relative py-24 md:py-32 px-6 bg-background">
      <div className="max-w-7xl mx-auto">
        {/* Header Block */}
        <div className="text-center max-w-3xl mx-auto mb-16 md:mb-24">
          {eyebrow && (
            <span className="text-xs uppercase tracking-[0.2em] font-semibold text-accent mb-4 block">
              {eyebrow}
            </span>
          )}
          
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="text-3xl md:text-5xl font-header font-bold text-foreground mb-6"
          >
            {title}
          </motion.h2>
          
          {subtitle && (
            <motion.p
              initial={{ opacity: 0, y: 15 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: 0.1 }}
              className="text-base md:text-lg font-body font-light text-foreground/60 leading-relaxed"
            >
              {subtitle}
            </motion.p>
          )}
        </div>

        {/* Pricing/Feature cards */}
        {items && items.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto items-stretch">
            {items.map((item, index) => {
              const isPopular = index === 1; // Middle card represents the flagship luxury rebel choice
              return (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 50 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true, margin: "-50px" }}
                  transition={{ ...transition, delay: index * 0.15 }}
                  className={`group relative p-8 md:p-10 rounded-custom border flex flex-col justify-between shadow-custom transition-all duration-500 overflow-hidden ${
                    isPopular
                      ? "bg-cardBg border-accent scale-100 md:scale-105 z-10"
                      : "bg-cardBg/40 border-borderColor hover:border-accent/30 scale-100"
                  }`}
                >
                  {isPopular && (
                    <div className="absolute top-0 right-0 bg-accent text-background font-mono text-[9px] uppercase tracking-widest font-bold py-1.5 px-4 rounded-bl-custom shadow-md">
                      Flagship
                    </div>
                  )}

                  <div>
                    <h3 className="text-xl md:text-2xl font-header font-bold text-foreground mb-4 group-hover:text-accent transition-colors duration-300">
                      {item.title}
                    </h3>
                    
                    <p className="text-sm font-body font-light text-foreground/60 leading-relaxed mb-8">
                      {item.description}
                    </p>
                    
                    {/* Simulated price to fulfill standard pricing design expectation */}
                    <div className="flex items-baseline gap-2 mb-8">
                      <span className="text-3xl md:text-4xl font-header font-bold text-foreground">
                        {index === 0 ? "$999" : index === 1 ? "$2,499" : "Custom"}
                      </span>
                      <span className="text-xs font-body font-light text-foreground/50">
                        {index !== 2 ? "/ edition" : "/ tailored"}
                      </span>
                    </div>

                    <ul className="space-y-4 border-t border-borderColor/60 pt-8 mb-10">
                      <li className="flex items-center gap-3 text-xs md:text-sm font-body text-foreground/70">
                        <Check className="w-4 h-4 text-accent flex-shrink-0" />
                        <span>Premium Handcrafted Materials</span>
                      </li>
                      <li className="flex items-center gap-3 text-xs md:text-sm font-body text-foreground/70">
                        <Check className="w-4 h-4 text-accent flex-shrink-0" />
                        <span>Limited Edition Release</span>
                      </li>
                      <li className="flex items-center gap-3 text-xs md:text-sm font-body text-foreground/70">
                        <Check className="w-4 h-4 text-accent flex-shrink-0" />
                        <span>Dynamic Interaction Framework</span>
                      </li>
                    </ul>
                  </div>

                  <button
                    className={`w-full py-3.5 px-6 rounded-custom font-body font-semibold text-center text-xs md:text-sm tracking-wide transition-all duration-300 transform active:scale-95 outline-none ${
                      isPopular
                        ? "bg-accent text-background hover:shadow-[0_0_20px_var(--color-accent)]"
                        : "bg-muted text-foreground hover:bg-accent hover:text-background"
                    }`}
                  >
                    Acquire Now
                  </button>
                </motion.div>
              );
            })}
          </div>
        )}
      </div>
    </section>
  );
}
